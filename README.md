🛡️ URL Guardian: Analizador de Seguridad Web

📖 El Origen del Proyecto

Este proyecto nació de una experiencia real: un intento de estafa a través de una sofisticada página de phishing que suplantaba la identidad de una entidad bancaria. La capacidad de analizar metadatos del dominio, como su antigüedad, fue clave para detectar el fraude.

URL Guardian es la materialización de esa experiencia, una herramienta diseñada para empoderar a los usuarios, permitiéndoles verificar la legitimidad de un sitio web a través del análisis de su URL antes de interactuar con él.

✨ Características Principales

Análisis de Dominios: Proporciona información crucial de cualquier URL para ayudar a identificar sitios fraudulentos.

Autenticación Segura de Usuarios: Sistema de registro e inicio de sesión construido desde cero, con encriptación de contraseñas (hashing y salting) y gestión de sesiones mediante tokens JWT.

Historial de Búsquedas Personal: Cada usuario tiene un historial privado de las URLs que ha analizado, almacenado de forma segura en la base de datos.

Arquitectura Multi-contenedor: Utiliza Docker y docker-compose para orquestar los servicios de la aplicación, garantizando un entorno de desarrollo aislado y reproducible.

Evolución de MVP a Producto: El proyecto fue planificado y ejecutado en fases, comenzando con un MVP funcional y escalando hasta la versión actual con funcionalidades completas.

🚀 Demo en Vivo
La aplicación y la base de datos están completamente desplegadas en la nube utilizando Render.

Explora la Aplicación: https://analizador-confianza.onrender.com/

🧠 Desafíos y Soluciones de Ingeniería
Escalado de un MVP: El proyecto se inició con un analizador de URLs anónimo. El principal desafío fue refactorizar la arquitectura para soportar un sistema de usuarios multi-tenant, lo que implicó integrar una base de datos relacional y modificar todos los endpoints para que fueran dependientes de la sesión del usuario.

Implementación de Autenticación Segura: En lugar de depender de librerías de terceros, se construyó el flujo de autenticación desde cero. Esto requirió una investigación y aplicación cuidadosa de las mejores prácticas de seguridad, incluyendo el hashing seguro de contraseñas con passlib y la implementación de tokens de acceso JWT para proteger las rutas.

⚙️ Cómo Ejecutar el Proyecto Localmente
Para clonar y ejecutar este proyecto en tu propio entorno:

Clona el repositorio:

Bash

git clone https://github.com/Marcosnapo/analizador-confianza
cd url-guardian
Configura las variables de entorno:

Dentro de la carpeta raíz, crea un archivo llamado .env.

Añade las siguientes variables (usando tus propios valores):

DATABASE_URL="postgresql://usuario:contraseña@host:puerto/nombre_db"
SECRET_KEY="una_clave_secreta_muy_larga_y_segura"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
Levanta el entorno con Docker:

Este comando construirá y levantará los contenedores definidos en tu docker-compose.yml.

Bash

docker-compose up --build
La API estará disponible en http://localhost:8000 (o el puerto que hayas configurado).
