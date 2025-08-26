# Versión final del Dockerfile en la raíz del proyecto
FROM python:3.11-slim

WORKDIR /app

# Copia solo los requisitos del backend primero
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia ambas carpetas, frontend y backend, al contenedor
COPY ./frontend ./frontend
COPY ./backend ./backend

# Establece el directorio de trabajo final dentro del código del backend
WORKDIR /app/backend
