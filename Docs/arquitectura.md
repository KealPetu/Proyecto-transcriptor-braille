# Diseño de Arquitectura de Software - Proyecto Braille

## 1\. Visión General

El sistema es una aplicación web **Full Stack** diseñada para la transcripción bidireccional entre español y el sistema Braille, así como la generación de recursos accesibles (señalética en PDF e imágenes).

La arquitectura sigue el patrón de **Microservicios (simulado)** mediante contenedores Docker, desacoplando completamente el Frontend del Backend para permitir escalabilidad independiente y mantenimiento modular.

## 2\. Diagrama de Arquitectura (Alto Nivel)

graph TD
    User[Usuario Final] -->|Interactúa vía Browser| Frontend[Contenedor Frontend (React)]
    Frontend -->|HTTP Requests (JSON/Blob)| Backend[Contenedor Backend (FastAPI)]
    
    subgraph "Backend Core"
        Backend --> Router[API Router]
        Router --> ServiceT[Servicio Traducción]
        Router --> ServiceG[Servicio Generación]
        ServiceT --> Logic[Lógica Braille (Reglas de Negocio)]
        ServiceG --> Libs[ReportLab / Pillow]
    end
    
    subgraph "Infraestructura & DevOps"
        Docker[Docker Compose] --> Frontend
        Docker --> Backend
        GitHub[GitHub Actions] -->|CI/CD| Tests[Pytest & Build Checks]
    end

## 3\. Componentes del Sistema

### 3.1. Frontend (Capa de Presentación)

Responsable de la interacción con el usuario y la visualización del sistema Braille.

  * **Tecnología:** React 18, Vite, TypeScript.
  * **Componentes Clave:**
      * `BrailleDisplay`: Orquestador de la visualización.
      * `BrailleCell`: Componente visual que renderiza el "Símbolo Generador" de 6 puntos usando CSS Grid.
      * `api.ts`: Capa de servicio para comunicación con el Backend.
  * **Comunicación:** Consume la REST API del backend para enviar texto y recibir matrices de puntos o archivos binarios (Blobs).

### 3.2. Backend (Capa de Lógica y Datos)

Expone la lógica de negocio a través de una API RESTful documentada automáticamente.

  * **Tecnología:** Python 3.10, FastAPI, Uvicorn.
  * **Módulos Principales:**
      * [cite\_start]**Core Logic (`braille_logic.py`):** Implementación pura de las reglas de traducción (Series 1, 2, 3, prefijos numéricos y mayúsculas) basada en el documento de requisitos [cite: 32-136].
      * **Translation Service:** Gestiona el estado y contexto (modo numérico) durante la traducción.
      * **Generation Service:** Utiliza `ReportLab` y `Pillow` para dibujar vectores y generar archivos descargables.

### 3.3. Infraestructura (DevOps)

El entorno está completamente "containerizado" para garantizar consistencia entre desarrollo y producción.

  * **Docker:** Contenedores aislados para Frontend (Node Alpine) y Backend (Python Slim).
  * **Docker Compose:** Orquestación de servicios, gestión de red interna (`braille_network`) y volúmenes para *Hot Reload* en desarrollo.
  * **CI/CD:** Pipeline de GitHub Actions que ejecuta pruebas unitarias (`pytest`) y verifica la compilación del frontend en cada *Push* o *Pull Request*.

## 4\. Flujo de Datos

1.  **Entrada:** El usuario ingresa texto en español en la interfaz web.
2.  **Procesamiento:**
      * El Frontend envía un `POST` con el texto.
      * El Backend recibe el JSON y lo valida con **Pydantic**.
      * El servicio de traducción descompone el texto, aplica las reglas de las Series Braille y genera una matriz de enteros (ej: `[[1,2], [1,5]]`).
3.  **Salida Visual:** El Frontend recibe la matriz y "pinta" los puntos correspondientes en la grilla CSS.
4.  **Generación de Archivos:**
      * Para PDFs/Imágenes, el Backend genera el archivo en memoria (`BytesIO`) y lo transmite como un `StreamingResponse`.
      * El Frontend recibe el flujo binario, crea un `Blob` y fuerza la descarga en el navegador.

## 5\. Decisiones Técnicas y Justificación

| Componente | Elección | Justificación |
| :--- | :--- | :--- |
| **Lenguaje Backend** | **Python** | Facilidad para manejo de strings y librerías robustas de generación de archivos (ReportLab). |
| **Framework API** | **FastAPI** | Velocidad, tipado estático y generación automática de documentación (Swagger) requerida por el proyecto. |
| **Frontend** | **React** | Arquitectura basada en componentes ideal para reutilizar la celda Braille (`BrailleCell`). |
| **Estrategia Git** | **GitFlow** | Requerimiento explícito para organizar el desarrollo (`main`, `develop`, `feature/*`). |
| **Despliegue** | **Docker** | Garantiza que el proyecto funcione en cualquier máquina sin configurar entornos locales complejos. |
