"""
REQUERIMIENTO 7: DOCUMENTACIÓN DEL AMBIENTE

Descripción:
    Guía completa para configurar el entorno de desarrollo, staging y producción.
    Incluye requisitos del sistema, instalación de dependencias, variables de
    entorno, y procedimientos de verificación.

Objetivo:
    Permitir que nuevos desarrolladores configuren rápidamente su entorno local
    y que el proyecto se pueda desplegar en diferentes plataformas sin problemas.

Versión: 1.0
Fecha: Enero 2026
Estado: COMPLETADO ✅


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 1: REQUISITOS DEL SISTEMA
═══════════════════════════════════════════════════════════════════════════════

REQUERIMIENTOS MÍNIMOS (DESARROLLO LOCAL)
──────────────────────────────────────────

Sistema Operativo:
├─ Windows 10/11 (recomendado)
├─ macOS 11+ (Big Sur o posterior)
├─ Linux (Ubuntu 20.04+ o equivalente)
└─ WSL2 (para Windows, recomendado)

Procesador:
├─ Mínimo: 2 cores
├─ Recomendado: 4+ cores
└─ Para producción: 8+ cores

Memoria RAM:
├─ Mínimo: 4 GB
├─ Recomendado: 8 GB (desarrollo con Docker)
└─ Para producción: 16+ GB

Almacenamiento:
├─ Espacio libre: 10 GB mínimo
├─ Recomendado: 50 GB (con cache Docker)
└─ SSD recomendado

Conexión a Internet:
├─ Requerida para descargas iniciales
├─ ~2-5 GB datos (primer setup)
└─ Velocidad: 10+ Mbps

Software Base:
├─ Git 2.30+
├─ Docker 20.10+ (recomendado)
├─ Docker Compose 1.29+
└─ VS Code (opcional pero recomendado)


REQUERIMIENTOS ESPECÍFICOS POR COMPONENTE
──────────────────────────────────────────

BACKEND (Python):
├─ Python 3.11+ (o 3.9+ mínimo)
├─ pip (gestor de paquetes)
├─ venv o virtualenv (entorno aislado)
└─ Git (control de versiones)

FRONTEND (Node.js):
├─ Node.js 18+ (LTS recomendado)
├─ npm 9+ (gestor de paquetes)
├─ Git (control de versiones)
└─ VS Code con extensiones (opcional)

DOCKER (Recomendado):
├─ Docker Engine 20.10+
├─ Docker Compose 1.29+ (v2 recomendado)
├─ Docker Desktop (Windows/macOS)
└─ WSL2 backend (Windows)


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 2: INSTALACIÓN DE HERRAMIENTAS BASE
═══════════════════════════════════════════════════════════════════════════════

OPCIÓN A: CON DOCKER (RECOMENDADO - MÁS FÁCIL)
────────────────────────────────────────────────

Paso 1: Descargar e instalar Docker
├─ Windows/macOS: Descargar Docker Desktop desde https://www.docker.com/products/docker-desktop
├─ Linux: sudo apt-get install docker.io docker-compose
└─ Verificar: docker --version && docker-compose --version

Paso 2: Descargar el proyecto
├─ git clone https://github.com/usuario/proyecto-transcriptor-braille.git
├─ cd proyecto-transcriptor-braille
└─ Verificar: git status

Paso 3: Iniciar servicios
├─ docker-compose up -d
├─ Esperar ~1 minuto por primera vez
└─ Verificar: docker-compose ps

Paso 4: Acceder a la aplicación
├─ Frontend: http://localhost:3000
├─ Backend API: http://localhost:8000
├─ Swagger Docs: http://localhost:8000/docs
└─ ReDoc Docs: http://localhost:8000/redoc

Paso 5: Ejecutar tests
├─ docker-compose exec backend pytest tests/ -v
└─ Resultado: 81/81 PASSED ✅

Ventajas:
✓ No requiere instalar Python/Node localmente
✓ Entorno aislado y reproducible
✓ Funciona igual en todos los OS
✓ Fácil de limpiar (docker-compose down)

Desventajas:
✗ Requiere ~2 GB RAM adicionales
✗ Overhead de virtualización
✗ Debugging más complejo


OPCIÓN B: SETUP LOCAL (SIN DOCKER)
───────────────────────────────────

Paso 1: Clonar repositorio
├─ git clone https://github.com/usuario/proyecto-transcriptor-braille.git
├─ cd proyecto-transcriptor-braille
└─ Verificar: git status

Paso 2: Configurar Backend (Python)
├─ Navegar: cd backend
├─ Crear venv: python -m venv venv
├─ Activar venv:
│  ├─ Windows: venv\\Scripts\\activate
│  └─ macOS/Linux: source venv/bin/activate
├─ Instalar deps: pip install -r requirements.txt
└─ Verificar: pip list

Paso 3: Ejecutar Backend
├─ cd backend
├─ source venv/bin/activate (o venv\\Scripts\\activate en Windows)
├─ Iniciar: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
├─ Verificar: http://localhost:8000/docs
└─ Detener: Ctrl+C

Paso 4: Configurar Frontend (Node.js)
├─ Navegar: cd frontend
├─ Instalar deps: npm install
├─ Verificar: npm list react
└─ Esperar ~2 minutos

Paso 5: Ejecutar Frontend
├─ cd frontend
├─ Iniciar: npm start
├─ Verificar: http://localhost:3000
└─ Detener: Ctrl+C

Paso 6: Ejecutar Tests
├─ cd backend
├─ pytest tests/ -v
└─ Resultado: 81/81 PASSED ✅

Ventajas:
✓ Control total del entorno
✓ Debugging más fácil
✓ Cambios inmediatos sin recompilación
✓ Menor consumo de recursos

Desventajas:
✗ Requiere instalar múltiples herramientas
✗ Diferencias entre OS
✗ Más pasos para principiantes
✗ Gestión manual de versiones


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 3: GUÍA DE INSTALACIÓN DETALLADA POR OS
═══════════════════════════════════════════════════════════════════════════════

WINDOWS 10/11 (SIN DOCKER - LOCAL)
───────────────────────────────────

Paso 1: Instalar Python 3.11
├─ Descargar: https://www.python.org/downloads/release/python-3110/
├─ Ejecutar instalador
├─ ✓ Marcar: "Add Python to PATH"
├─ ✓ Marcar: "Install pip"
├─ Instalar
├─ Verificar: python --version
│  └─ Salida: Python 3.11.x
└─ Verificar: pip --version
   └─ Salida: pip 2x.x.x

Paso 2: Instalar Node.js 18 LTS
├─ Descargar: https://nodejs.org/ (versión LTS)
├─ Ejecutar instalador
├─ Seguir wizard (siguiente, siguiente...)
├─ Reiniciar terminal/PowerShell
├─ Verificar: node --version
│  └─ Salida: v18.x.x
└─ Verificar: npm --version
   └─ Salida: 9.x.x

Paso 3: Instalar Git
├─ Descargar: https://git-scm.com/download/win
├─ Ejecutar instalador
├─ Seguir wizard (usar configuración por defecto)
├─ Reiniciar terminal
├─ Verificar: git --version
└─ Salida: git version 2.40.x

Paso 4: Clonar proyecto
├─ Abrir PowerShell en carpeta deseada
├─ git clone https://github.com/usuario/proyecto.git
├─ cd proyecto-transcriptor-braille
└─ dir (verificar archivos)

Paso 5: Setup Backend
├─ cd backend
├─ python -m venv venv
├─ .\\venv\\Scripts\\activate
│  └─ Prompt cambiar a: (venv) C:\\...
├─ pip install --upgrade pip
├─ pip install -r requirements.txt
│  └─ Instala: FastAPI, Pydantic, PIL, ReportLab, pytest, etc.
├─ Verificar: pip list | findstr FastAPI
└─ Resultado: fastapi

Paso 6: Setup Frontend
├─ cd ..\\frontend
├─ npm install
│  └─ Descarga ~500MB (node_modules)
├─ npm list react
│  └─ Verifica versión React
└─ Esperar ~3 minutos en primera vez

Paso 7: Iniciar Backend
├─ cd ..\\backend
├─ .\\venv\\Scripts\\activate
├─ uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
├─ Salida: INFO:     Uvicorn running on http://0.0.0.0:8000
├─ Acceder: http://localhost:8000/docs
└─ Detener: Ctrl+C

Paso 8: Iniciar Frontend (nueva terminal)
├─ cd frontend
├─ npm start
├─ Salida: On Your Network: http://XXX.XXX.X.XXX:3000
├─ Acceder: http://localhost:3000
└─ Detener: Ctrl+C


MACOS (SIN DOCKER - LOCAL)
──────────────────────────

Paso 1: Instalar Homebrew (si no está)
├─ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
├─ Seguir instrucciones
└─ Verificar: brew --version

Paso 2: Instalar Python 3.11
├─ brew install python@3.11
├─ Verificar: python3 --version
│  └─ Salida: Python 3.11.x
└─ pip3 --version

Paso 3: Instalar Node.js 18 LTS
├─ brew install node
├─ Verificar: node --version
│  └─ Salida: v18.x.x
└─ npm --version

Paso 4: Instalar Git
├─ brew install git
├─ Verificar: git --version
└─ Salida: git version 2.40.x

Paso 5: Clonar proyecto
├─ cd ~/Documentos (o carpeta deseada)
├─ git clone https://github.com/usuario/proyecto.git
├─ cd proyecto-transcriptor-braille
└─ ls -la

Paso 6: Setup Backend
├─ cd backend
├─ python3 -m venv venv
├─ source venv/bin/activate
│  └─ Prompt: (venv) usuario@mac...
├─ pip install --upgrade pip
├─ pip install -r requirements.txt
└─ pip list | grep FastAPI

Paso 7: Setup Frontend
├─ cd ../frontend
├─ npm install
└─ Esperar ~3 minutos

Paso 8: Iniciar Backend
├─ cd ../backend
├─ source venv/bin/activate
├─ uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
├─ Acceder: http://localhost:8000/docs
└─ Detener: Ctrl+C

Paso 9: Iniciar Frontend (nueva terminal)
├─ cd frontend
├─ npm start
├─ Acceder: http://localhost:3000
└─ Detener: Ctrl+C


LINUX UBUNTU 20.04+ (SIN DOCKER - LOCAL)
─────────────────────────────────────────

Paso 1: Actualizar sistema
├─ sudo apt update
└─ sudo apt upgrade -y

Paso 2: Instalar Python 3.11
├─ sudo apt install python3.11 python3.11-venv python3-pip
├─ Verificar: python3 --version
│  └─ Salida: Python 3.11.x
└─ pip3 --version

Paso 3: Instalar Node.js 18 LTS
├─ curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
├─ sudo apt install nodejs
├─ Verificar: node --version
│  └─ Salida: v18.x.x
└─ npm --version

Paso 4: Instalar Git
├─ sudo apt install git
├─ Verificar: git --version
└─ Salida: git version 2.40.x

Paso 5: Clonar proyecto
├─ cd ~/Documentos (o carpeta deseada)
├─ git clone https://github.com/usuario/proyecto.git
├─ cd proyecto-transcriptor-braille
└─ ls -la

Paso 6: Setup Backend
├─ cd backend
├─ python3 -m venv venv
├─ source venv/bin/activate
├─ pip install --upgrade pip
├─ pip install -r requirements.txt
└─ pip list | grep FastAPI

Paso 7: Setup Frontend
├─ cd ../frontend
├─ npm install
└─ Esperar ~3 minutos

Paso 8: Iniciar Backend
├─ cd ../backend
├─ source venv/bin/activate
├─ uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
├─ Acceder: http://localhost:8000/docs
└─ Detener: Ctrl+C

Paso 9: Iniciar Frontend (nueva terminal)
├─ cd frontend
├─ npm start
├─ Acceder: http://localhost:3000
└─ Detener: Ctrl+C


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 4: SETUP CON DOCKER (RECOMENDADO)
═══════════════════════════════════════════════════════════════════════════════

INSTALACIÓN DE DOCKER
──────────────────────

WINDOWS 10/11:
├─ Descargar Docker Desktop: https://www.docker.com/products/docker-desktop
├─ Ejecutar instalador
├─ Habilitar WSL 2 (si se solicita)
├─ Reiniciar sistema
├─ Abrir PowerShell
├─ docker --version
└─ docker-compose --version

MACOS:
├─ Descargar Docker Desktop: https://www.docker.com/products/docker-desktop
├─ Instalar (arrastra a Applications)
├─ Abre Docker desde Applications
├─ Espera que inicie (~30 segundos)
├─ Abre Terminal
├─ docker --version
└─ docker-compose --version

LINUX UBUNTU:
├─ curl -fsSL https://get.docker.com -o get-docker.sh
├─ sudo sh get-docker.sh
├─ sudo usermod -aG docker $USER
├─ newgrp docker
├─ docker --version
└─ docker-compose --version


STARTUP RÁPIDO CON DOCKER
──────────────────────────

1. Clonar proyecto:
   git clone https://github.com/usuario/proyecto.git
   cd proyecto-transcriptor-braille

2. Iniciar servicios:
   docker-compose up -d

3. Esperar que inicie:
   ├─ Backend: ~15 segundos
   ├─ Frontend: ~30 segundos
   └─ Total: ~45 segundos

4. Verificar estado:
   docker-compose ps
   
   Salida esperada:
   NAME              STATUS
   braille_backend   Up 30s
   braille_frontend  Up 25s

5. Acceder a aplicación:
   ├─ Frontend: http://localhost:3000
   ├─ Backend: http://localhost:8000
   ├─ Swagger: http://localhost:8000/docs
   └─ ReDoc: http://localhost:8000/redoc

6. Ejecutar tests:
   docker-compose exec backend pytest tests/ -v

7. Ver logs:
   docker-compose logs -f backend
   docker-compose logs -f frontend

8. Detener servicios:
   docker-compose down

9. Limpiar todo (cuidado!):
   docker-compose down -v
   docker system prune -a


DOCKER COMPOSE - REFERENCIA DE COMANDOS
────────────────────────────────────────

Iniciar servicios:
  docker-compose up                    # Foreground (ver logs)
  docker-compose up -d                 # Background (detached)

Detener servicios:
  docker-compose stop                  # Parar (preserva datos)
  docker-compose down                  # Parar y eliminar contenedores
  docker-compose down -v               # Parar y eliminar todo (volumes)

Ver estado:
  docker-compose ps                    # Mostrar contenedores
  docker-compose logs                  # Ver logs acumulados
  docker-compose logs -f               # Ver logs en tiempo real
  docker-compose logs backend          # Logs solo backend
  docker-compose logs -f --tail=100 backend  # Últimas 100 líneas

Ejecutar comandos en contenedor:
  docker-compose exec backend bash     # Shell en backend
  docker-compose exec backend pytest   # Tests en backend
  docker-compose exec frontend npm list # Listar deps frontend

Compilar imágenes:
  docker-compose build                 # Compilar todas
  docker-compose build backend         # Compilar solo backend
  docker-compose build --no-cache      # Compilar sin cache

Eliminar datos:
  docker-compose down -v               # Eliminar volúmenes
  docker system prune                  # Limpiar recursos no usados


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 5: VARIABLES DE ENTORNO
═══════════════════════════════════════════════════════════════════════════════

ARCHIVOS DE CONFIGURACIÓN
──────────────────────────

.env.local (DESARROLLO - Local)
├─ Ubicación: Raíz del proyecto
├─ Contenido:
│  ├─ REACT_APP_API_URL=http://localhost:8000
│  ├─ REACT_APP_ENV=development
│  ├─ DEBUG=true
│  └─ LOG_LEVEL=debug
└─ Uso: npm start (frontend)

.env.docker (DOCKER - Desarrollo)
├─ Ubicación: Raíz del proyecto
├─ Contenido:
│  ├─ REACT_APP_API_URL=http://localhost:8000
│  ├─ REACT_APP_ENV=docker
│  ├─ DEBUG=false
│  └─ LOG_LEVEL=info
└─ Uso: docker-compose up

.env.staging (STAGING - Pre-producción)
├─ Ubicación: Raíz del proyecto
├─ Contenido:
│  ├─ REACT_APP_API_URL=https://api-staging.ejemplo.com
│  ├─ REACT_APP_ENV=staging
│  ├─ DEBUG=false
│  ├─ LOG_LEVEL=warning
│  └─ ANALYTICS_ID=xxx
└─ Uso: Despliegue en staging

.env.production (PRODUCCIÓN)
├─ Ubicación: Raíz del proyecto (git-ignored)
├─ Contenido:
│  ├─ REACT_APP_API_URL=https://api.ejemplo.com
│  ├─ REACT_APP_ENV=production
│  ├─ DEBUG=false
│  ├─ LOG_LEVEL=error
│  ├─ ANALYTICS_ID=xxx
│  ├─ SENTRY_DSN=https://...
│  └─ API_KEY=secret
└─ Uso: Despliegue en producción


VARIABLES BACKEND (Python)
──────────────────────────

PYTHONPATH:
  Definición: Ruta de módulos Python
  Valor: backend/
  Uso: python -m pytest tests/
  
DEBUG:
  Definición: Modo debug (logs verbosos)
  Valores: true/false
  Default: false
  
ENVIRONMENT:
  Definición: Entorno actual
  Valores: development, staging, production
  Default: development

DATABASE_URL:
  Definición: Conexión a base de datos (futuro)
  Formato: postgresql://user:pass@host:5432/db
  Default: None (en memoria)

REDIS_URL:
  Definición: Conexión a Redis cache (futuro)
  Formato: redis://localhost:6379/0
  Default: None

CORS_ORIGINS:
  Definición: Orígenes permitidos
  Valor: http://localhost:3000,https://ejemplo.com
  Default: http://localhost:3000

MAX_TEXT_LENGTH:
  Definición: Longitud máxima de texto
  Valor: 1000 caracteres
  Default: 1000

API_RATE_LIMIT:
  Definición: Límite de requests por minuto (futuro)
  Valor: 60
  Default: None (sin límite)


VARIABLES FRONTEND (React)
──────────────────────────

REACT_APP_API_URL:
  Definición: URL base del backend
  Valor: http://localhost:8000
  Default: http://localhost:8000
  Nota: Debe estar en .env o process.env

REACT_APP_ENV:
  Definición: Entorno actual
  Valores: development, staging, production
  Default: development

REACT_APP_VERSION:
  Definición: Versión de la app
  Valor: 1.0.0
  Default: Desde package.json

REACT_APP_TITLE:
  Definición: Título de la página
  Valor: Transcriptor Braille
  Default: Transcriptor Braille


CÓMO ESTABLECER VARIABLES
──────────────────────────

En .env file:
  VARIABLE_NAME=value
  DEBUG=true
  API_URL=http://localhost:8000

En la línea de comandos:
  export VARIABLE_NAME=value     (macOS/Linux)
  set VARIABLE_NAME=value         (Windows CMD)
  $env:VARIABLE_NAME = 'value'   (Windows PowerShell)
  
En docker-compose.yml:
  environment:
    VARIABLE_NAME: value
    DEBUG: "true"

En Python:
  import os
  value = os.getenv('VARIABLE_NAME', 'default')

En JavaScript/React:
  const value = process.env.REACT_APP_VARIABLE_NAME


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 6: VERIFICACIÓN DE INSTALACIÓN
═══════════════════════════════════════════════════════════════════════════════

CHECKLIST DE VERIFICACIÓN
──────────────────────────

Herramientas Base:
  ☐ Python 3.11+: python --version
  ☐ Node.js 18+: node --version
  ☐ npm 9+: npm --version
  ☐ Git 2.30+: git --version
  ☐ Docker 20.10+: docker --version (si usas Docker)
  ☐ Docker Compose 1.29+: docker-compose --version (si usas Docker)

Backend (Local):
  ☐ Venv activado: (venv) en prompt
  ☐ Dependencias: pip list | grep FastAPI
  ☐ Backend corre: http://localhost:8000/docs
  ☐ Tests pasan: pytest tests/ -v → 81/81 PASSED
  ☐ No hay errores: uvicorn output sin ERROR

Frontend (Local):
  ☐ Node modules: ls node_modules/ | grep react
  ☐ Frontend corre: http://localhost:3000
  ☐ Sin errores de compilación
  ☐ Puede hacer llamadas API

Docker (Si lo usas):
  ☐ Servicios activos: docker-compose ps → Up
  ☐ Backend responde: http://localhost:8000/health
  ☐ Frontend carga: http://localhost:3000
  ☐ API funciona: POST /api/v1/translation/to-braille

Tests:
  ☐ Tests locales: cd backend && pytest tests/ -v
  ☐ Tests Docker: docker-compose exec backend pytest
  ☐ Cobertura: pytest --cov=app tests/


PRUEBAS RÁPIDAS
───────────────

Test 1: Backend disponible
  curl http://localhost:8000/docs
  Esperado: Página Swagger (HTML)

Test 2: API de traducción
  curl -X POST http://localhost:8000/api/v1/translation/to-braille \
    -H "Content-Type: application/json" \
    -d '{"text": "Hola"}'
  Esperado: JSON con braille y estado success

Test 3: Frontend disponible
  curl http://localhost:3000
  Esperado: Página HTML con React

Test 4: Tests ejecutados
  cd backend && pytest tests/ -v
  Esperado: 81 PASSED, 0 FAILED

Test 5: Imagen generada
  curl -X POST http://localhost:8000/api/v1/generation/image \
    -H "Content-Type: application/json" \
    -d '{"text": "Hola"}' --output test.png
  Esperado: Archivo test.png (~5KB)


SCRIPT DE VERIFICACIÓN (verify_setup.sh)
────────────────────────────────────────

#!/bin/bash
# Script para verificar que todo está bien configurado

echo "=== Verificando instalación ==="
echo

echo "✓ Verificando Python..."
if command -v python3 &> /dev/null; then
    python3 --version
else
    echo "✗ Python no encontrado"
    exit 1
fi

echo "✓ Verificando Node.js..."
if command -v node &> /dev/null; then
    node --version
else
    echo "✗ Node.js no encontrado"
    exit 1
fi

echo "✓ Verificando Git..."
if command -v git &> /dev/null; then
    git --version
else
    echo "✗ Git no encontrado"
    exit 1
fi

echo "✓ Verificando Docker..."
if command -v docker &> /dev/null; then
    docker --version
else
    echo "⚠ Docker no encontrado (opcional)"
fi

echo "✓ Verificando Backend..."
cd backend
if [ -f "requirements.txt" ]; then
    echo "  requirements.txt encontrado"
else
    echo "✗ requirements.txt no encontrado"
    exit 1
fi

echo "✓ Verificando Frontend..."
cd ../frontend
if [ -f "package.json" ]; then
    echo "  package.json encontrado"
else
    echo "✗ package.json no encontrado"
    exit 1
fi

echo
echo "=== ✅ Verificación completada ==="
echo "Ejecuta: docker-compose up -d"
echo "Luego accede a: http://localhost:3000"


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 7: TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

PROBLEMAS COMUNES Y SOLUCIONES
──────────────────────────────

PROBLEMA 1: "Python no encontrado"
──────────────────────────────────

Síntoma: bash: python: command not found
Causa: Python no está en PATH o no está instalado

Solución Windows:
  1. Instalar Python desde https://python.org
  2. ✓ Marcar "Add Python to PATH"
  3. Reiniciar terminal/PowerShell
  4. Verificar: python --version

Solución macOS:
  1. brew install python@3.11
  2. Crear link: alias python3=python3.11
  3. Agregar a ~/.bash_profile

Solución Linux:
  1. sudo apt install python3
  2. sudo apt install python3-pip
  3. Verificar: python3 --version


PROBLEMA 2: "pip: command not found"
───────────────────────────────────

Síntoma: bash: pip: command not found
Causa: pip no está instalado o no está en PATH

Solución:
  1. Instalar pip: python -m ensurepip --upgrade
  2. Verificar: pip --version
  3. Si persiste: pip3 --version
  4. Crear alias: alias pip=pip3


PROBLEMA 3: "ModuleNotFoundError: No module named 'FastAPI'"
────────────────────────────────────────────────────────────

Síntoma: ModuleNotFoundError cuando ejecutas backend
Causa: Dependencias no instaladas o venv no activado

Solución:
  1. Verificar venv activado: debes ver (venv) en prompt
  2. Si no: source venv/bin/activate (o .\\venv\\Scripts\\activate)
  3. Instalar deps: pip install -r requirements.txt
  4. Verificar: pip list | grep fastapi


PROBLEMA 4: "Port 8000 already in use"
──────────────────────────────────────

Síntoma: Address already in use cuando inicia backend
Causa: Otro proceso usa puerto 8000

Solución macOS/Linux:
  lsof -i :8000           # Ver qué ocupa el puerto
  kill -9 <PID>           # Matar proceso
  O cambiar puerto: uvicorn app.main:app --port 8001

Solución Windows:
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  O cambiar puerto: uvicorn app.main:app --port 8001


PROBLEMA 5: "Port 3000 already in use"
──────────────────────────────────────

Síntoma: Something is already running on port 3000
Causa: Otro frontend o proceso usa puerto 3000

Solución:
  1. Buscar proceso: lsof -i :3000 (macOS/Linux)
  2. Matar: kill -9 <PID>
  3. O cambiar puerto: PORT=3001 npm start


PROBLEMA 6: "npm install tarda mucho o falla"
──────────────────────────────────────────────

Síntoma: npm install se cuelga o falla después de 10 minutos
Causa: Problema de conexión, cache corrupto, o servidor npm lento

Solución:
  1. Limpiar cache: npm cache clean --force
  2. Instalar de nuevo: npm install
  3. O usar npm registry alternativo:
     npm config set registry https://registry.npmjs.org/
     npm install


PROBLEMA 7: "Docker: command not found"
───────────────────────────────────────

Síntoma: bash: docker: command not found
Causa: Docker no está instalado o no está en PATH

Solución Windows:
  1. Descargar Docker Desktop desde docker.com
  2. Instalar y ejecutar
  3. Reiniciar terminal
  4. Verificar: docker --version

Solución macOS:
  1. brew install docker
  2. Instalar Docker Desktop manualmente
  3. Abrir Docker desde Applications
  4. Verificar: docker --version

Solución Linux:
  1. curl -fsSL https://get.docker.com -o get-docker.sh
  2. sudo sh get-docker.sh
  3. sudo usermod -aG docker $USER
  4. Logout y login
  5. Verificar: docker --version


PROBLEMA 8: "docker-compose up tarda mucho"
───────────────────────────────────────────

Síntoma: docker-compose up se cuelga en "Pulling image"
Causa: Conexión lenta, servidor Docker Hub lento, o disco lleno

Solución:
  1. Ver logs: docker-compose logs -f
  2. Parar: docker-compose down
  3. Limpiar: docker system prune
  4. Reintentar: docker-compose up -d
  5. O cambiar registry en docker-compose.yml


PROBLEMA 9: "Tests fallan: 'ModuleNotFoundError'"
────────────────────────────────────────────────

Síntoma: pytest falla con ModuleNotFoundError
Causa: PYTHONPATH no es correcto o dependencias falta

Solución:
  1. Estar en directorio: cd backend
  2. Venv activado: source venv/bin/activate
  3. Instalar deps: pip install -r requirements.txt
  4. Ejecutar tests: pytest tests/ -v


PROBLEMA 10: "Frontend no se conecta al Backend"
─────────────────────────────────────────────────

Síntoma: Error de CORS, no puede alcanzar API
Causa: URLs mal configuradas, backend no corriendo, CORS bloqueado

Solución:
  1. Verificar backend corre: curl http://localhost:8000/docs
  2. Verificar REACT_APP_API_URL en .env: debe ser http://localhost:8000
  3. En frontend, revisar console (F12 → Console) por errores CORS
  4. En backend, verificar CORS está habilitado en main.py
  5. Reiniciar ambos servicios


PROBLEMA 11: "Imagen generada sale negra o vacía"
──────────────────────────────────────────────────

Síntoma: generate_braille_image retorna imagen negra
Causa: Coordenadas incorrectas, colores invertidos, o texto vacío

Solución:
  1. Probar con texto simple: "Hola"
  2. Revisar servicio generator.py
  3. Verificar colores: fondo blanco (255,255,255), puntos negros (0,0,0)
  4. Verificar coordenadas x, y están dentro de image.size


PROBLEMA 12: "PDF generado está vacío"
───────────────────────────────────────

Síntoma: PDF generado tiene 0 bytes o no contiene datos
Causa: Error en ReportLab, texto vacío, o encoding incorrecto

Solución:
  1. Revisar texto no sea vacío
  2. Probar con texto ASCII: "Hola"
  3. Verificar ReportLab está instalado: pip list | grep reportlab
  4. En generator.py, verificar PDF se guarda en BytesIO


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 8: COMANDOS DE REFERENCIA RÁPIDA
═══════════════════════════════════════════════════════════════════════════════

BACKEND (PYTHON)
────────────────

# Activar entorno virtual
source backend/venv/bin/activate              # macOS/Linux
.\\backend\\venv\\Scripts\\activate            # Windows

# Desactivar entorno virtual
deactivate

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencia individual
pip install fastapi

# Instalar con requisitos extra
pip install -e ".[dev]"

# Ver dependencias instaladas
pip list

# Ejecutar backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ejecutar con diferente puerto
uvicorn app.main:app --reload --port 8001

# Ejecutar tests
pytest tests/ -v

# Ejecutar test específico
pytest tests/test_logic.py::TestSerie1::test_letra_a -v

# Tests con cobertura
pytest --cov=app tests/

# Limpiar cache pytest
pytest --cache-clear


FRONTEND (NODE.JS)
──────────────────

# Instalar dependencias
npm install

# Instalar dependencia individual
npm install react

# Instalar versión específica
npm install react@18.2.0

# Ver dependencias instaladas
npm list

# Ejecutar desarrollo
npm start

# Construir para producción
npm run build

# Ejecutar tests
npm test

# Ejecutar tests sin watch
npm test -- --testPathPattern=. --watchAll=false

# Ejecutar linter
npm run lint

# Ejecutar TypeScript check
npx tsc --noEmit

# Limpiar cache
rm -rf node_modules
npm cache clean --force
npm install


DOCKER
──────

# Iniciar servicios background
docker-compose up -d

# Ver estado de servicios
docker-compose ps

# Ver logs acumulados
docker-compose logs

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio
docker-compose logs backend

# Ejecutar comando en contenedor
docker-compose exec backend bash
docker-compose exec backend pytest tests/ -v

# Parar servicios (preserva datos)
docker-compose stop

# Parar y eliminar (elimina datos)
docker-compose down

# Parar, eliminar todo incluyendo volúmenes
docker-compose down -v

# Recompilación de imágenes
docker-compose build

# Recompilación forzada sin cache
docker-compose build --no-cache

# Limpiar espacio disco
docker system prune
docker system prune -a


GIT
───

# Clonar repositorio
git clone https://github.com/usuario/proyecto.git

# Ver estado
git status

# Ver commits recientes
git log --oneline -10

# Crear rama nueva
git checkout -b nombre-rama

# Cambiar rama
git checkout nombre-rama

# Commit cambios
git add .
git commit -m "Mensaje descriptivo"

# Push cambios
git push origin nombre-rama

# Ver diferencias
git diff


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 9: RECURSOS Y REFERENCIAS
═══════════════════════════════════════════════════════════════════════════════

DOCUMENTACIÓN OFICIAL
──────────────────────

FastAPI:
  https://fastapi.tiangolo.com/
  https://fastapi.tiangolo.com/deployment/

React:
  https://react.dev
  https://react.dev/learn

TypeScript:
  https://www.typescriptlang.org/
  https://www.typescriptlang.org/docs/

Python:
  https://docs.python.org/3.11/
  https://pip.pypa.io/en/stable/

Docker:
  https://docs.docker.com/
  https://docs.docker.com/compose/

Node.js:
  https://nodejs.org/docs/
  https://npm.js.org


TUTORIALES Y GUÍAS
───────────────────

FastAPI Tutorial:
  https://fastapi.tiangolo.com/tutorial/

React Tutorial:
  https://react.dev/learn/start-a-new-react-project

Docker Getting Started:
  https://docs.docker.com/get-started/

Git Basics:
  https://git-scm.com/doc


HERRAMIENTAS ÚTILES
────────────────────

Postman: https://www.postman.com/
  └─ Testing API requests

VS Code: https://code.visualstudio.com/
  └─ Editor recomendado

Insomnia: https://insomnia.rest/
  └─ Alternativa a Postman

iTerm2: https://iterm2.com/
  └─ Terminal mejorada (macOS)

WSL2: https://docs.microsoft.com/en-us/windows/wsl/
  └─ Linux en Windows (recomendado)


EXTENSIONES VS CODE RECOMENDADAS
──────────────────────────────────

Backend (Python):
  ├─ Pylance
  ├─ Python
  ├─ Pytest
  ├─ Docker
  └─ REST Client

Frontend (React/TypeScript):
  ├─ ES7+ React/Redux/React-Native snippets
  ├─ Prettier - Code formatter
  ├─ ESLint
  ├─ TypeScript Vue Plugin
  └─ Tailwind CSS IntelliSense

General:
  ├─ Git Graph
  ├─ GitLens
  ├─ Thunder Client
  └─ Live Server


═══════════════════════════════════════════════════════════════════════════════
SECCIÓN 10: MANTENIMIENTO DEL ENTORNO
═══════════════════════════════════════════════════════════════════════════════

ACTUALIZAR DEPENDENCIAS
───────────────────────

Python (Backend):
  # Ver actualizaciones disponibles
  pip list --outdated
  
  # Actualizar FastAPI
  pip install --upgrade fastapi
  
  # Actualizar todos
  pip install --upgrade -r requirements.txt
  
  # Generar requirements nuevo
  pip freeze > requirements.txt

Node.js (Frontend):
  # Ver actualizaciones disponibles
  npm outdated
  
  # Actualizar dependencia específica
  npm update react
  
  # Actualizar todo
  npm update
  
  # Actualizar npm mismo
  npm install -g npm@latest


LIMPIAR ESPACIO
────────────────

Python:
  # Eliminar __pycache__
  find . -type d -name __pycache__ -exec rm -rf {} +
  
  # Eliminar .pyc
  find . -type f -name '*.pyc' -delete
  
  # Limpiar venv
  rm -rf venv/

Node.js:
  # Eliminar node_modules
  rm -rf node_modules/
  
  # Limpiar cache npm
  npm cache clean --force

Docker:
  # Eliminar imágenes no usadas
  docker image prune
  
  # Eliminar contenedores parados
  docker container prune
  
  # Limpiar todo (cuidado!)
  docker system prune -a


HACER BACKUP
─────────────

Código:
  git push origin main  # Backup remoto

Datos (si hay base de datos):
  # PostgreSQL
  pg_dump -U user dbname > backup.sql
  
  # MongoDB
  mongodump --archive=backup.archive

Configuración:
  # Backup .env (NO commitear a git)
  cp .env .env.backup


═══════════════════════════════════════════════════════════════════════════════
RESUMEN RÁPIDO - INICIO RÁPIDO
═══════════════════════════════════════════════════════════════════════════════

OPCIÓN 1: CON DOCKER (3 pasos)
──────────────────────────────

1. git clone https://github.com/usuario/proyecto.git
2. docker-compose up -d
3. Acceder: http://localhost:3000

Listo! ✅


OPCIÓN 2: SIN DOCKER - WINDOWS (10 pasos)
───────────────────────────────────────────

1. Instalar Python 3.11 desde python.org
2. Instalar Node 18 LTS desde nodejs.org
3. Instalar Git desde git-scm.com
4. git clone https://github.com/usuario/proyecto.git
5. cd backend
6. python -m venv venv
7. .\\venv\\Scripts\\activate
8. pip install -r requirements.txt
9. cd ..\\frontend && npm install
10. Abrir 2 terminales:
    - Terminal 1: cd backend && .\\venv\\Scripts\\activate && uvicorn app.main:app --reload
    - Terminal 2: cd frontend && npm start

Listo! ✅


OPCIÓN 3: SIN DOCKER - MACOS/LINUX (10 pasos)
───────────────────────────────────────────────

1. brew install python@3.11 node git (macOS)
   O: sudo apt install python3 nodejs git (Linux)
2. git clone https://github.com/usuario/proyecto.git
3. cd backend
4. python3 -m venv venv
5. source venv/bin/activate
6. pip install -r requirements.txt
7. cd ../frontend && npm install
8. Abrir 2 terminales:
   - Terminal 1: cd backend && source venv/bin/activate && uvicorn app.main:app --reload
   - Terminal 2: cd frontend && npm start

Listo! ✅


═══════════════════════════════════════════════════════════════════════════════
FIN DE DOCUMENTACIÓN - REQUERIMIENTO 7
═══════════════════════════════════════════════════════════════════════════════

Autor: Sistema de Documentación de Ambiente
Fecha: Enero 2026
Estado: ✅ COMPLETADO

Este documento cubre:
✓ Requisitos del sistema
✓ Instalación de herramientas base
✓ Setup por Sistema Operativo
✓ Setup con Docker
✓ Variables de entorno
✓ Verificación de instalación
✓ Troubleshooting completo
✓ Comandos de referencia
✓ Recursos y referencias
✓ Mantenimiento del entorno

Próximo Requerimiento: Req 8 - Manuales de Usuario e Instalación (Usuario Final)
"""
