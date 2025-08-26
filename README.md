# Analizador de Confianza Web 🕵️

Una aplicación web full-stack construida con FastAPI y Docker que permite a los usuarios analizar la confiabilidad de una URL, registrarse y guardar un historial de sus búsquedas.

## Demo

*(Aquí podrás pegar un GIF o un enlace a la aplicación una vez que esté desplegada en Render)*

## Funcionalidades Clave

* **Análisis de URL:** Extrae la antigüedad del dominio, el estado de HTTPS y las tecnologías web utilizadas.
* **Sistema de Usuarios Seguro:** Registro y login de usuarios con hashing de contraseñas (bcrypt) y autenticación basada en tokens JWT.
* **Rutas Protegidas:** El historial de análisis es privado y solo accesible para usuarios autenticados.
* **Persistencia de Datos:** El historial y los datos de usuario se guardan en una base de datos PostgreSQL.
* **Interfaz Reactiva:** Frontend construido con JavaScript puro que interactúa con la API sin recargar la página.

## Stack Tecnológico

* **Backend:** Python 3.11, FastAPI, SQLAlchemy
* **Base de Datos:** PostgreSQL
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)
* **Infraestructura y Despliegue:** Docker, Docker Compose, Render

## ¿Cómo Correr el Proyecto Localmente?

1.  Clona este repositorio.
2.  Asegúrate de tener Docker y Docker Compose instalados.
3.  Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
    ```
    POSTGRES_DB=analizador_db
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=supersecret
    ```
4.  Ejecuta el siguiente comando para construir y levantar los contenedores:
    ```bash
    docker-compose up --build
    ```
5.  Abre tu navegador en `http://localhost:8000`.
