from pydantic import BaseModel, EmailStr

# Schema para recibir datos al crear un usuario
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema para devolver los datos de un usuario (sin la contraseña)
class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# Schema para recibir la URL a analizar
class URLRequest(BaseModel):
    url: str

# Schema para la respuesta del analizador de URLs
class AnalysisResponse(BaseModel):
    url_analizada: str
    antiguedad_dominio_dias: int | None
    tiene_https: bool
    evaluacion: str
    tecnologias: list[str] = [] 

# Schema para la respuesta del token
class Token(BaseModel):
    access_token: str
    token_type: str

# AÑADE ESTAS NUEVAS CLASES AL FINAL
class HistoryBase(BaseModel):
    url: str
    result: str

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True # Renombramos orm_mode como nos sugirió la advertencia
