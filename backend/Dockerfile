# 1. Usar una imagen base oficial de Python
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar solo el archivo de requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- NUEVA LÍNEA ---
COPY ../frontend ./frontend

# 4. Copiar el resto del código de la aplicación
COPY ./app ./app
