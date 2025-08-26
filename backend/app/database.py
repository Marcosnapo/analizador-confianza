import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Leemos la única variable de entorno que nos dará Render
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

# Si estamos en local (Render no define esta URL), usamos nuestras variables .env
if not SQLALCHEMY_DATABASE_URL:
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_HOST = "db"
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para la Sesión de la Base de Datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
