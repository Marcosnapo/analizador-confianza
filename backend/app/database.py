import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Render nos dará esta variable de entorno automáticamente.
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

# Si la variable no existe (porque estamos en local), la construimos
# con nuestro archivo .env como antes.
if not SQLALCHEMY_DATABASE_URL:
    DB_USER = os.environ.get("POSTG-RES_USER")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_HOST = "db"
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
