document.addEventListener('DOMContentLoaded', () => {

    // --- SELECTORES DE ELEMENTOS ---
    const analyzerView = document.getElementById('analyzer-view');
    const authView = document.getElementById('auth-view');
    const historyView = document.getElementById('history-view');
    const userSection = document.getElementById('user-section');
    
    const loginForm = document.getElementById('login-form-container');
    const registerForm = document.getElementById('register-form-container');

    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');

    const loginEmailInput = document.getElementById('login-email');
    const loginPasswordInput = document.getElementById('login-password');
    const loginBtn = document.getElementById('login-btn');
    
    const registerEmailInput = document.getElementById('register-email');
    const registerPasswordInput = document.getElementById('register-password');
    const registerBtn = document.getElementById('register-btn');

    const logoutBtn = document.getElementById('logout-btn');
    const welcomeMessage = document.getElementById('welcome-message');
    const authError = document.getElementById('auth-error');

    // --- NUEVO: Selectores del Analizador y del Historial ---
    const urlInput = document.getElementById('urlInput');
    const analizarBtn = document.getElementById('analizarBtn');
    const resultadoDiv = document.getElementById('resultado');
    const historyList = document.getElementById('history-list');

    // --- LÓGICA DE API ---

    // Función para registrar un usuario (sin cambios)
    async function registerUser() {
    const email = registerEmailInput.value;
    const password = registerPasswordInput.value;

    const response = await fetch('/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        alert('¡Registro exitoso! Por favor, inicia sesión.');
        showLoginLink.click(); // Cambiamos a la vista de login
        authError.textContent = '';
    } else {
        const errorData = await response.json();
        authError.textContent = errorData.detail || 'Error en el registro.';
    }
}
    // Función para iniciar sesión (sin cambios)
    async function loginUser() {
    const email = loginEmailInput.value;
    const password = loginPasswordInput.value;
    
    // Usamos el formato que espera OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch('/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
    });

    if (response.ok) {
        const data = await response.json();
        // Guardamos el token en el almacenamiento local del navegador
        localStorage.setItem('token', data.access_token);
        authError.textContent = '';
        updateView(); // Actualizamos la vista para mostrar la app
    } else {
        const errorData = await response.json();
        authError.textContent = errorData.detail || 'Error al iniciar sesión.';
    }
}
    // Función para cerrar sesión (sin cambios)
    function logoutUser() {
    localStorage.removeItem('token');
    updateView();
}
    // --- NUEVO: Funciones del Analizador y del Historial ---

    async function analyzeUrl() {
        const url = urlInput.value.trim();
        if (!url) {
            resultadoDiv.textContent = 'Por favor, ingresa una URL.';
            return;
        }
        resultadoDiv.textContent = 'Analizando...';
    
        const response = await fetch('/analizar/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url }),
        });
    
        if (response.ok) {
            const data = await response.json();
        let output = `
            URL Analizada: ${data.url_analizada}
            Antigüedad: ${data.antiguedad_dominio_dias !== null ? data.antiguedad_dominio_dias + ' días' : 'No disponible'}
            Usa HTTPS: ${data.tiene_https ? 'Sí' : 'No'}
            Evaluación: ${data.evaluacion}
        `;

        if (data.tecnologias && data.tecnologias.length > 0) {
            output += `\n        Tecnologías: ${data.tecnologias.join(', ')}`;
        }

        resultadoDiv.textContent = output.trim();
            // Guardamos el resultado en el historial
            saveHistory(url, JSON.stringify(data, null, 2));
        } else {
            resultadoDiv.textContent = 'Ocurrió un error al analizar la URL.';
        }
    }
    
    async function saveHistory(url, result) {
        const token = localStorage.getItem('token');
        if (!token) return; // No hacer nada si no hay token
    
        await fetch('/history/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // ¡Enviamos el token!
            },
            body: JSON.stringify({ url, result }),
        });
        
        // Refrescamos la lista del historial para que aparezca el nuevo item
        fetchAndDisplayHistory();
    }
    
    async function fetchAndDisplayHistory() {
        const token = localStorage.getItem('token');
        if (!token) return;
    
        const response = await fetch('/history/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            },
        });
    
        if (response.ok) {
            const histories = await response.json();
            historyList.innerHTML = ''; // Limpiamos la lista antes de llenarla
            histories.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>URL:</strong> ${item.url}<br><pre>${item.result}</pre>`;
                historyList.appendChild(li);
            });
        }
    }


    // --- LÓGICA DE VISUALIZACIÓN ---
    
    function updateView() {
        const token = localStorage.getItem('token');
    
        if (token) {
            authView.classList.add('hidden');
            analyzerView.classList.remove('hidden');
            historyView.classList.remove('hidden');
            userSection.classList.remove('hidden');
            
            // Decodificamos el token para obtener el email del usuario
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                welcomeMessage.textContent = `Hola, ${payload.sub}`;
            } catch (e) {
                welcomeMessage.textContent = 'Bienvenido';
            }

            fetchAndDisplayHistory(); // Mostramos el historial al iniciar sesión
        } else {
            authView.classList.remove('hidden');
            analyzerView.classList.add('hidden');
            historyView.classList.add('hidden');
            userSection.classList.add('hidden');
        }
    }

    // Lógica para cambiar entre formularios (sin cambios)
    showRegisterLink.addEventListener('click', (e) => { /* ... */ });
    showLoginLink.addEventListener('click', (e) => { /* ... */ });


    // --- ASIGNACIÓN DE EVENTOS ---
    registerBtn.addEventListener('click', registerUser);
    loginBtn.addEventListener('click', loginUser);
    logoutBtn.addEventListener('click', logoutUser);
    analizarBtn.addEventListener('click', analyzeUrl); // ¡Conectamos el botón de analizar!

    // --- INICIALIZACIÓN ---
    updateView();
});

// Nota: Para que el código anterior funcione, copia y pega las funciones registerUser, loginUser, y logoutUser
// del paso anterior en las secciones indicadas como "... (código existente)".
