import requests
import whois
from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import auth
from .database import SessionLocal, engine
from .database import SessionLocal, engine, get_db
import builtwith
from sqlalchemy import text

# Importaciones de nuestros módulos locales
from . import crud, models, schemas
from .database import SessionLocal, engine

# Lógica para crear el esquema en la base de datos
with engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS analizador_schema"))
    connection.commit()# Le decimos a SQLAlchemy que cree las tablas si no existen

models.Base.metadata.create_all(bind=engine)

# --- 1. Inicialización y CORS ---
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Endpoints de la API ---

# Endpoint original del Analizador
@app.post("/analizar/", response_model=schemas.AnalysisResponse)
def analizar_url(request: schemas.URLRequest):
    url = request.url
    tiene_https = url.startswith("https://")
    antiguedad_dias = None
    tecnologias_detectadas = []
    try:
        tech = builtwith.parse(url)
        # Convertimos las claves del diccionario a una lista de nombres de tecnologías
        tecnologias_detectadas = list(tech.keys())
    except Exception as e:
        print(f"No se pudo detectar tecnologías: {e}")
    try:
        dominio_info = whois.whois(url)
        if dominio_info.creation_date:
            fecha_creacion = dominio_info.creation_date
            if isinstance(fecha_creacion, list):
                fecha_creacion = fecha_creacion[0]
            diferencia = datetime.now() - fecha_creacion
            antiguedad_dias = diferencia.days
    except Exception as e:
        print(f"No se pudo obtener la info del dominio: {e}")

    evaluacion = "ANÁLISIS COMPLETADO"
    if antiguedad_dias is not None and antiguedad_dias < 180:
        evaluacion = "PRECAUCIÓN: Dominio muy reciente."
    
    return schemas.AnalysisResponse(
        url_analizada=url,
        antiguedad_dominio_dias=antiguedad_dias,
        tiene_https=tiene_https,
        evaluacion=evaluacion,
        tecnologias=tecnologias_detectadas
    )

# Endpoint de Registro de Usuarios
@app.post("/auth/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Endpoint Protegido de Ejemplo
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

# AÑADE ESTOS DOS ENDPOINTS

@app.post("/history/", response_model=schemas.History)
def create_history_for_user(
    history: schemas.HistoryCreate,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_user_history(db=db, history=history, user_id=current_user.id)

@app.get("/history/", response_model=list[schemas.History])
def read_user_history(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    histories = crud.get_user_histories(db, user_id=current_user.id, skip=skip, limit=limit)
    return histories

# Endpoint de Login
@app.post("/auth/login/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- 5. Servir los archivos estáticos (el enfoque final) ---
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/", response_class=FileResponse)
def read_index():
    return FileResponse('../frontend/index.html')
