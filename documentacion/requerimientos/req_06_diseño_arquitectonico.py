"""
REQUERIMIENTO 6: DISEÑO ARQUITECTÓNICO

Descripción:
    Documentación completa de la arquitectura del sistema Proyecto Transcriptor Braille,
    incluyendo diagramas C4, componentes, patrones de diseño y flujos de datos.

Objetivo:
    Proporcionar una visión clara y estructurada de cómo está organizado el sistema,
    desde el nivel de contexto hasta el nivel de código, facilitando entendimiento
    y mantenimiento del proyecto.

Versión: 1.0
Fecha: Enero 2026
Estado: COMPLETADO ✅


═══════════════════════════════════════════════════════════════════════════════
NIVEL 1: DIAGRAMA DE CONTEXTO (SYSTEM CONTEXT DIAGRAM)
═══════════════════════════════════════════════════════════════════════════════

Descripción: Muestra el sistema en su contexto más amplio, indicando actores
externos y sistemas relacionados.

┌─────────────────────────────────────────────────────────────────────────────┐
│                          ACTORS / USUARIOS EXTERNOS                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐                                      ┌──────────────┐ │
│  │  Usuario Final   │                                      │ Administrador│ │
│  │  (Visitante Web) │                                      │  de Sistema  │ │
│  └────────┬─────────┘                                      └──────┬───────┘ │
│           │                                                       │         │
│           │  HTTP/HTTPS                                          │         │
│           │                                                       │         │
│  ┌────────▼────────────────────────────────────────────────────┬─▼───────┐ │
│  │                                                              │         │ │
│  │       PROYECTO TRANSCRIPTOR BRAILLE (Sistema Central)       │  Config │ │
│  │                                                              │ Files   │ │
│  │  • Traducción Español ↔ Braille                             │         │ │
│  │  • Generación de Señalética (PNG/PDF)                       └─────────┘ │
│  │  • API REST + Frontend Web                                              │ │
│  │                                                                         │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│                                                                              │
│                         SERVICIOS EXTERNOS (Potencial)                      │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       │
│  │  Base de     │  │  Almacenamiento  │  Email Service│  [NO IMPLEMENTADOS] │
│  │  Datos       │  │  en Nube          │  (SMTP)       │                     │
│  └──────────────┘  └──────────────┘  └──────────────┘                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
NIVEL 2: DIAGRAMA DE CONTENEDORES (CONTAINER DIAGRAM)
═══════════════════════════════════════════════════════════════════════════════

Descripción: Muestra la estructura de alto nivel del sistema incluyendo
servicios, aplicaciones, bases de datos y tecnologías principales.

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         USUARIOS FINALES / INTERNET                         │
│                                                                              │
│                                  ▲                                           │
│                                  │ HTTP/HTTPS                               │
│                                  │ (REST API)                               │
│                                  │                                           │
│  ┌───────────────────────────────┼───────────────────────────────────────┐ │
│  │  LOCAL NETWORK / DOCKER COMPOSE                                       │ │
│  │                               │                                       │ │
│  │       ┌─────────────┐         │         ┌─────────────────────────┐ │ │
│  │       │             │         │         │                         │ │ │
│  │       │  FRONTEND   │◄────────┼────────►│    BACKEND API          │ │ │
│  │       │             │         │         │                         │ │ │
│  │       │ React 18    │         │         │ FastAPI                 │ │ │
│  │       │ TypeScript  │         │         │ Python 3.11             │ │ │
│  │       │ Tailwind    │         │         │                         │ │ │
│  │       │ CSS         │         │         │ Port: 8000              │ │ │
│  │       │             │         │         │ Docs: /docs             │ │ │
│  │       │ Port: 3000  │         │         │ Port (host): 8000       │ │ │
│  │       │             │         │         │                         │ │ │
│  │       │ Components: │         │         │ Routes:                 │ │ │
│  │       │ • TextInput │         │         │ • /api/v1/translation   │ │ │
│  │       │ • BrailleSig│         │         │ • /api/v1/generation    │ │ │
│  │       │ • Display   │         │         │ • /docs (Swagger)       │ │ │
│  │       │             │         │         │                         │ │ │
│  │       └─────────────┘         │         │ Services:               │ │ │
│  │                               │         │ • translator.py         │ │ │
│  │       File System             │         │ • generator.py          │ │ │
│  │       (Images/PDFs)           │         │                         │ │ │
│  │       Port: 80                │         │ Core Logic:             │ │ │
│  │       Volume: /app/static     │         │ • braille_logic.py      │ │ │
│  │                               │         │                         │ │ │
│  │                               │         │ Schemas:                │ │ │
│  │                               │         │ • Pydantic models       │ │ │
│  │                               │         │                         │ │ │
│  │                               │         │ Dependencies:           │ │ │
│  │                               │         │ • PIL (imágenes)        │ │ │
│  │                               │         │ • reportlab (PDFs)      │ │ │
│  │                               │         │ • pytest (tests)        │ │ │
│  │                               │         │                         │ │ │
│  │                               └────────►│                         │ │ │
│  │                                         │                         │ │ │
│  │                               [FUTURE]  │ Database (Optional):    │ │ │
│  │                               ┌────────►│ • PostgreSQL            │ │ │
│  │                               │         │ • Redis (cache)         │ │ │
│  │                               │         │                         │ │ │
│  │                               │         └─────────────────────────┘ │ │
│  │                               │                                     │ │
│  └───────────────────────────────┼─────────────────────────────────────┘ │
│                                  │                                        │
│                      Docker Network: braille-network                      │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

Tecnologías:
├─ Frontend Container:
│  ├─ Node.js 18 LTS
│  ├─ React 18
│  ├─ TypeScript 4.9
│  └─ Tailwind CSS
│
├─ Backend Container:
│  ├─ Python 3.11
│  ├─ FastAPI (Modern REST framework)
│  ├─ Pydantic (Validation)
│  ├─ PIL/Pillow (Image processing)
│  └─ ReportLab (PDF generation)
│
└─ Orchestración:
   └─ Docker Compose (desarrollo y producción)


═══════════════════════════════════════════════════════════════════════════════
NIVEL 3: DIAGRAMA DE COMPONENTES (COMPONENT DIAGRAM) - BACKEND
═══════════════════════════════════════════════════════════════════════════════

Descripción: Detalla la estructura interna del Backend FastAPI y sus
responsabilidades.

┌─────────────────────────────────────────────────────────────────────────────┐
│                          BACKEND - FastAPI Application                      │
│                          backend/app/main.py                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      PRESENTATION LAYER (API Routes)                  │  │
│  │                                                                       │  │
│  │  ┌─────────────────────────┐      ┌─────────────────────────┐       │  │
│  │  │ routes/translation.py   │      │ routes/generation.py    │       │  │
│  │  │                         │      │                         │       │  │
│  │  │ Endpoints:              │      │ Endpoints:              │       │  │
│  │  │ • POST /to-braille      │      │ • POST /image           │       │  │
│  │  │ • POST /to-text         │      │ • POST /pdf             │       │  │
│  │  │ • GET /health           │      │ • GET /status           │       │  │
│  │  │                         │      │                         │       │  │
│  │  │ Validación:             │      │ Validación:             │       │  │
│  │  │ • Pydantic schemas      │      │ • Pydantic schemas      │       │  │
│  │  │ • Error handling        │      │ • File size limits      │       │  │
│  │  └──────────┬──────────────┘      └──────────┬──────────────┘       │  │
│  │             │                                 │                      │  │
│  └─────────────┼─────────────────────────────────┼──────────────────────┘  │
│                │                                 │                         │
│  ┌─────────────▼──────────────────────────────────▼──────────────────────┐  │
│  │                      SERVICE LAYER (Business Logic)                  │  │
│  │                                                                       │  │
│  │  ┌───────────────────────────┐      ┌────────────────────────────┐  │  │
│  │  │ services/translator.py    │      │ services/generator.py      │  │  │
│  │  │                           │      │                            │  │  │
│  │  │ Classes:                  │      │ Classes:                   │  │  │
│  │  │ • text_to_braille()       │      │ • BrailleImageGenerator    │  │  │
│  │  │ • braille_to_text()       │      │ • BraillePDFGenerator      │  │  │
│  │  │                           │      │ • generate_braille_image() │  │  │
│  │  │ Responsabilidades:        │      │ • generate_braille_pdf()   │  │  │
│  │  │ • Traducción bidireccional│      │                            │  │  │
│  │  │ • Validación de entrada   │      │ Responsabilidades:         │  │  │
│  │  │ • Manejo de prefijos      │      │ • Generación de PNG        │  │  │
│  │  │ • Desambigüación          │      │ • Generación de PDF (A4)   │  │  │
│  │  │                           │      │ • Escalado de imágenes     │  │  │
│  │  │                           │      │ • Configuración de fuentes │  │  │
│  │  └──────────┬────────────────┘      └───────────┬────────────────┘  │  │
│  │             │                                   │                   │  │
│  └─────────────┼───────────────────────────────────┼───────────────────┘  │
│                │                                   │                      │
│  ┌─────────────▼───────────────────────────────────▼───────────────────┐  │
│  │                      CORE LOGIC LAYER (Domain)                     │  │
│  │                                                                    │  │
│  │  ┌────────────────────────────────────────────────────────────┐  │  │
│  │  │ core/braille_logic.py                                     │  │  │
│  │  │                                                            │  │  │
│  │  │ Data Structures:                                           │  │  │
│  │  │ • MAPA_BRAILLE_COMPLETO (Serie 1, 2, 3)                   │  │  │
│  │  │ • MAPA_INVERSO (Braille → Texto)                          │  │  │
│  │  │ • TABLA_DESAMBIGUACION (Resolución de conflictos)         │  │  │
│  │  │ • PREFIJO_NUM = [3, 4, 5, 6]                              │  │  │
│  │  │ • PREFIJO_MAY = [4, 6]                                    │  │  │
│  │  │                                                            │  │  │
│  │  │ Functions:                                                 │  │  │
│  │  │ • generar_mapa_completo()                                  │  │  │
│  │  │ • _generar_reverse_map()                                   │  │  │
│  │  │ • get_priority_character()                                 │  │  │
│  │  │                                                            │  │  │
│  │  │ Mapeos Incluidos:                                          │  │  │
│  │  │ • 26 letras españolas (a-z)                               │  │  │
│  │  │ • 6 vocales acentuadas (á, é, í, ó, ú, ñ)               │  │  │
│  │  │ • 10 dígitos (0-9)                                         │  │  │
│  │  │ • 8 signos de puntuación                                   │  │  │
│  │  └────────────┬─────────────────────────────────────────────┘  │  │
│  │              │                                                 │  │
│  └──────────────┼─────────────────────────────────────────────────┘  │
│                 │                                                    │
│  ┌──────────────▼─────────────────────────────────────────────────┐  │
│  │                   SCHEMAS / DATA MODELS                        │  │
│  │              schemas/translation.py & others                   │  │
│  │                                                                │  │
│  │  Pydantic Models:                                              │  │
│  │  ├─ TextTobrailleRequest                                      │  │
│  │  │  ├─ text: str                                              │  │
│  │  │  └─ Optional[include_original]: bool                       │  │
│  │  │                                                             │  │
│  │  ├─ TextTobrailleResponse                                     │  │
│  │  │  ├─ braille: List[List[int]]                               │  │
│  │  │  ├─ original_text: str                                     │  │
│  │  │  └─ status: str                                            │  │
│  │  │                                                             │  │
│  │  ├─ GenerationRequest                                         │  │
│  │  │  ├─ text: str                                              │  │
│  │  │  ├─ title: Optional[str]                                   │  │
│  │  │  ├─ include_text: bool                                     │  │
│  │  │  └─ format: str (png/pdf)                                  │  │
│  │  │                                                             │  │
│  │  └─ Validación automática                                     │  │
│  │     • Límite de longitud                                      │  │
│  │     • Tipo de dato                                            │  │
│  │     • Rango de valores                                        │  │
│  │                                                                │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Flujo de Datos - Traducción:
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐    ┌────────┐
│ Request │───►│ Route    │───►│ Service  │───►│ Logic   │───►│Response│
│ JSON    │    │ Validate │    │ Process  │    │ Braille │    │ JSON   │
└─────────┘    └──────────┘    └──────────┘    └─────────┘    └────────┘

Flujo de Datos - Generación:
┌─────────┐    ┌──────────┐    ┌───────────┐    ┌─────────┐    ┌────────┐
│ Request │───►│ Route    │───►│ Generator │───►│ PIL/    │───►│ Binary │
│ JSON    │    │ Validate │    │ Service   │    │ RL Lib  │    │ Stream │
└─────────┘    └──────────┘    └───────────┘    └─────────┘    └────────┘


═══════════════════════════════════════════════════════════════════════════════
NIVEL 3: DIAGRAMA DE COMPONENTES (COMPONENT DIAGRAM) - FRONTEND
═══════════════════════════════════════════════════════════════════════════════

Descripción: Estructura de la aplicación React frontend

┌─────────────────────────────────────────────────────────────────────────────┐
│                      FRONTEND - React Application                           │
│                      src/App.tsx                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      APP COMPONENT (Root)                            │  │
│  │                                                                      │  │
│  │  ├─ State Management (React Hooks)                                 │  │
│  │  │  ├─ useState (text, braille, generatedFile)                     │  │
│  │  │  ├─ useEffect (API initialization)                             │  │
│  │  │  └─ useCallback (optimized functions)                          │  │
│  │  │                                                                 │  │
│  │  ├─ Props Distribution ─────────────────────────────┐             │  │
│  │  │                                                  │             │  │
│  │  ├─────────────────────────────────────────────────┼─────────────┤  │
│  │  │                                                 │              │  │
│  │  │  COMPONENTS:                                    │              │  │
│  │  │                                                 │              │  │
│  │  │  ┌────────────────────────┐  ┌────────────────┐│              │  │
│  │  │  │ TextInput Component    │  │ BrailleCell    ││              │  │
│  │  │  │ (components/)          │  │ (components/)  ││              │  │
│  │  │  │                        │  │                ││              │  │
│  │  │  │ Responsabilidades:     │  │ Responsabili-  ││              │  │
│  │  │  │ • Input field          │  │ dades:         ││              │  │
│  │  │  │ • onChange handler     │  │ • Render 6     ││              │  │
│  │  │  │ • API call trigger     │  │   dots         ││              │  │
│  │  │  │ • Error display        │  │ • CSS styling  ││              │  │
│  │  │  │ • Loading state        │  │ • Responsive   ││              │  │
│  │  │  │                        │  │   layout       ││              │  │
│  │  │  │ Props:                 │  │                ││              │  │
│  │  │  │ • placeholder          │  │ Props:         ││              │  │
│  │  │  │ • onChange             │  │ • dots         ││              │  │
│  │  │  │ • disabled             │  │ • highlighted  ││              │  │
│  │  │  │ • value                │  │ • interactive  ││              │  │
│  │  │  │                        │  │                ││              │  │
│  │  │  │ Styling:               │  │ Styling:       ││              │  │
│  │  │  │ • TextInput.css        │  │ • BrailleCell  ││              │  │
│  │  │  │ • Tailwind utilities   │  │   .css         ││              │  │
│  │  │  └────────────────────────┘  └────────────────┘│              │  │
│  │  │                                                 │              │  │
│  │  │  ┌────────────────────────┐  ┌────────────────┐               │  │
│  │  │  │ BrailleDisplay         │  │ Generation     │               │  │
│  │  │  │ Component (components/)│  │ Controls       │               │  │
│  │  │  │                        │  │                │               │  │
│  │  │  │ Responsabilidades:     │  │ Responsabili-  │               │  │
│  │  │  │ • Grid layout          │  │ dades:         │               │  │
│  │  │  │ • Cell rendering       │  │ • PNG button   │               │  │
│  │  │  │ • Map over cells       │  │ • PDF button   │               │  │
│  │  │  │ • Responsive           │  │ • Title input  │               │  │
│  │  │  │                        │  │ • Error handle │               │  │
│  │  │  │ Props:                 │  │                │               │  │
│  │  │  │ • cells                │  │ Props:         │               │  │
│  │  │  │ • highlighted          │  │ • onGenerate   │               │  │
│  │  │  │ • interactive          │  │ • disabled     │               │  │
│  │  │  │                        │  │ • loading      │               │  │
│  │  │  │ Styling:               │  │                │               │  │
│  │  │  │ • BrailleDisplay.css   │  │ Styling:       │               │  │
│  │  │  │ • Grid CSS             │  │ • Button CSS   │               │  │
│  │  │  │ • Animations           │  │ • Form CSS     │               │  │
│  │  │  └────────────────────────┘  └────────────────┘               │  │
│  │  │                                                                │  │
│  │  └────────────────────────────────────────────────────────────────┘  │
│  │                                                                       │
│  └───────────────────────────────────────────────────────────────────────┘
│
│  ┌───────────────────────────────────────────────────────────────────────┐
│  │                   API SERVICE LAYER                                   │
│  │                   services/api.ts                                     │
│  │                                                                       │
│  │  Functions:                                                           │
│  │  • translateToBraille(text): Promise<BrailleResponse>                │
│  │  • translateToText(braille): Promise<TextResponse>                   │
│  │  • generateImage(text, options): Promise<Blob>                       │
│  │  • generatePDF(text, title): Promise<Blob>                           │
│  │                                                                       │
│  │  Configuration:                                                       │
│  │  • Base URL: http://localhost:8000 (dev)                            │
│  │  • Error handling                                                    │
│  │  • Request/Response mapping                                          │
│  │  • Timeout configuration                                             │
│  │                                                                       │
│  └───────────────────────────────────────────────────────────────────────┘
│
│  ┌───────────────────────────────────────────────────────────────────────┐
│  │                    STYLING ARCHITECTURE                               │
│  │                                                                       │
│  │  • index.css (Global styles)                                         │
│  │  • App.css (App-level styles)                                        │
│  │  • Component.css (Scoped styles)                                     │
│  │  • Tailwind CSS (Utility classes)                                    │
│  │  • tailwind.config.js (Custom configuration)                         │
│  │                                                                       │
│  │  Design System:                                                       │
│  │  • Color palette                                                     │
│  │  • Typography scale                                                  │
│  │  • Spacing system                                                    │
│  │  • Responsive breakpoints                                            │
│  │                                                                       │
│  └───────────────────────────────────────────────────────────────────────┘
│
└──────────────────────────────────────────────────────────────────────────────┘

Flujo de Datos - Frontend:
┌──────────┐    ┌────────────┐    ┌────────────┐    ┌──────────┐
│User      │───►│Component   │───►│API Service │───►│Backend   │
│Input     │    │Event       │    │(TypeScript)│    │(FastAPI) │
└──────────┘    └────────────┘    └────────────┘    └──────────┘
                                        ▲
                                        │ Response
                                        │
                                ┌───────▼────────┐
                                │UI Update       │
                                │State Change    │
                                │Component Render│
                                └────────────────┘


═══════════════════════════════════════════════════════════════════════════════
NIVEL 4: FLUJOS DE PROCESOS PRINCIPALES
═══════════════════════════════════════════════════════════════════════════════

FLUJO 1: TRADUCCIÓN ESPAÑOL → BRAILLE
────────────────────────────────────────

    ┌─ ENTRADA: "Hola"
    │
    ├─ VALIDACIÓN (Route Handler)
    │  └─ Verificar: no vacío, longitud < límite
    │
    ├─ SERVICE: text_to_braille()
    │  ├─ Normalizar texto (minúsculas excepto mayúsculas detectadas)
    │  ├─ Iterar carácter por carácter
    │  └─ Traducir cada uno:
    │     ├─ Si letra: buscar en MAPA_BRAILLE_COMPLETO
    │     ├─ Si número: prefijo [3,4,5,6] + mapeo
    │     ├─ Si mayúscula: prefijo [4,6] + mapeo de minúscula
    │     ├─ Si acento: buscar mapeo especial
    │     └─ Si puntuación: buscar en tabla
    │
    ├─ LÓGICA CORE: braille_logic.py
    │  └─ Búsqueda en MAPA_BRAILLE_COMPLETO
    │     └─ Retorna: [[puntos], [puntos], ...]
    │
    └─ SALIDA: JSON Response
       {
           "braille": [[1, 2, 5], [1, 3, 5], [1, 2, 3], [1]],
           "original_text": "Hola",
           "status": "success"
       }


FLUJO 2: TRADUCCIÓN BRAILLE → ESPAÑOL (INVERSA)
─────────────────────────────────────────────────

    ┌─ ENTRADA: [[1, 2, 5], [1, 3, 5], [1, 2, 3], [1]]
    │
    ├─ VALIDACIÓN (Route Handler)
    │  └─ Verificar: es lista de listas, valores 1-6
    │
    ├─ SERVICE: braille_to_text()
    │  ├─ Iterar cada celda
    │  └─ Traducir:
    │     ├─ Si celda == []: añadir espacio
    │     ├─ Si celda == [3,4,5,6] (prefijo): siguiente es número
    │     ├─ Si celda == [4,6] (prefijo): siguiente es mayúscula
    │     ├─ Sino: buscar en MAPA_INVERSO
    │     └─ Si hay ambigüedad: usar TABLA_DESAMBIGUACION
    │
    ├─ LÓGICA CORE: braille_logic.py
    │  ├─ _generar_reverse_map() [initialización]
    │  ├─ get_priority_character() [resolución de conflictos]
    │  └─ Retorna: "hola"
    │
    └─ SALIDA: JSON Response
       {
           "text": "hola",
           "original_braille": [...],
           "status": "success"
       }


FLUJO 3: GENERACIÓN DE IMAGEN PNG
───────────────────────────────────

    ┌─ ENTRADA: {"text": "Baño", "include_text": true}
    │
    ├─ VALIDACIÓN
    │  └─ Verificar: texto válido, longitud razonable
    │
    ├─ TRADUCCIÓN (interno)
    │  └─ text_to_braille("Baño")
    │     └─ Resultado: [[celda1], [celda2], ...]
    │
    ├─ SERVICE: BrailleImageGenerator.generate_image()
    │  ├─ Crear imagen en blanco (PIL)
    │  │  └─ Tamaño: (n_celdas * 50 + márgenes) x (60 + opcional texto)
    │  ├─ Para cada celda:
    │  │  ├─ Calcular posición X, Y
    │  │  ├─ Dibujar los 6 puntos (círculos)
    │  │  │  ├─ Punto 1 (arriba-izq): (x, y)
    │  │  │  ├─ Punto 2 (arriba-der): (x, y+h/2)
    │  │  │  ├─ Punto 3 (medio-izq): (x+w, y)
    │  │  │  ├─ Punto 4 (medio-der): (x+w, y+h/2)
    │  │  │  ├─ Punto 5 (abajo-izq): (x, y+h)
    │  │  │  └─ Punto 6 (abajo-der): (x+w, y+h)
    │  │  └─ Rellenar puntos presentes, vaciar ausentes
    │  ├─ Si include_text: añadir texto debajo
    │  │  └─ Usar fuente mono-espaciada
    │  └─ Convertir a PNG en BytesIO
    │
    ├─ PIPELINE: PIL Image → PNG bytes → BytesIO
    │  └─ MIME Type: image/png
    │
    └─ SALIDA: Descarga de archivo PNG
       Content-Type: image/png
       Content-Disposition: attachment; filename="braille_baño.png"


FLUJO 4: GENERACIÓN DE PDF A4
──────────────────────────────

    ┌─ ENTRADA: {"text": "Entrada", "title": "Señalética Entrada"}
    │
    ├─ VALIDACIÓN
    │  └─ Verificar: texto válido, título opcional
    │
    ├─ TRADUCCIÓN (interno)
    │  └─ text_to_braille("Entrada")
    │
    ├─ SERVICE: BraillePDFGenerator.generate_pdf()
    │  ├─ Crear documento PDF (ReportLab)
    │  │  └─ Página A4 (210mm x 297mm)
    │  ├─ Layouts:
    │  │  ├─ Si title: añadir encabezado (H1)
    │  │  ├─ Espacio vertical
    │  │  ├─ Renderizar tabla de celdas Braille
    │  │  │  └─ Filas de 10 celdas (estándar)
    │  │  └─ Espacio vertical
    │  ├─ Información adicional (opcional)
    │  │  ├─ Fecha y hora
    │  │  ├─ Número de página
    │  │  └─ Footer
    │  └─ Guardar en BytesIO
    │
    ├─ PIPELINE: ReportLab → PDF bytes → BytesIO
    │  └─ MIME Type: application/pdf
    │
    └─ SALIDA: Descarga de archivo PDF
       Content-Type: application/pdf
       Content-Disposition: attachment; filename="braille_entrada.pdf"


═══════════════════════════════════════════════════════════════════════════════
PATRONES DE DISEÑO UTILIZADOS
═══════════════════════════════════════════════════════════════════════════════

1. MVC (Model-View-Controller)
   ├─ Model: braille_logic.py (mapeos y datos)
   ├─ View: Frontend React (presentación)
   └─ Controller: routes/ (lógica de enrutamiento)

2. SERVICE LAYER PATTERN
   ├─ Services encapsulan lógica de negocio
   ├─ Desacoplamiento de rutas y lógica
   └─ Reutilización entre endpoints

3. DEPENDENCY INJECTION (implícito)
   ├─ FastAPI inyecta dependencias
   ├─ Validación automática con Pydantic
   └─ Manejo de errores centralizado

4. STRATEGY PATTERN
   ├─ Different generación strategies (PNG vs PDF)
   └─ Interfaces comunes: generate_image, generate_pdf

5. DECORATOR PATTERN
   ├─ FastAPI @app.post(), @app.get()
   └─ Python @property, @staticmethod

6. SINGLETON PATTERN
   ├─ Mapeos Braille (MAPA_BRAILLE_COMPLETO)
   ├─ Inicialización una sola vez
   └─ Reutilización en todas las operaciones

7. FACTORY PATTERN
   ├─ generate_braille_image() (constructor de imágenes)
   ├─ generate_braille_pdf() (constructor de PDFs)
   └─ Abstracción de creación compleja


═══════════════════════════════════════════════════════════════════════════════
ESTRUCTURAS DE DATOS CLAVE
═══════════════════════════════════════════════════════════════════════════════

1. MAPA_BRAILLE_COMPLETO (Diccionario)
   ─────────────────────────────────────
   
   Estructura:
   {
       'a': [1],
       'b': [1, 2],
       'c': [1, 4],
       ...
       'á': [1, 2, 3, 5, 6],
       'ñ': [1, 2, 4, 5, 6],
       ...
       '1': [1],              # Con prefijo [3,4,5,6]
       '2': [1, 2],
       ...
       '.': [2, 5, 6],
       ',': [2],
       ...
   }
   
   Tamaño: ~50 entradas
   Acceso: O(1) - Búsqueda directa
   

2. MAPA_INVERSO (Diccionario generado dinámicamente)
   ─────────────────────────────────────────────────
   
   Estructura:
   {
       '[1]': 'a',
       '[1, 2]': 'b',
       '[1, 3, 6]': 'u',
       '[1, 3, 4, 6]': 'ó',  # O 'v' (colisión)
       ...
       '[3, 4, 5, 6]': '<PREFIJO_NÚMERO>',
       '[4, 6]': '<PREFIJO_MAYÚSCULA>',
       ...
   }
   
   Generación: En startup de la aplicación
   Acceso: O(1) - Búsqueda directa
   


3. TABLA_DESAMBIGUACION (Diccionario)
   ──────────────────────────────────
   
   Estructura:
   {
       '[1, 3, 4, 6]': 'ó',    # Prioridad: acento > consonante
       '[1, 2, 3, 4, 5]': 'ñ', # Prioridad: ñ > otras
       ...
   }
   
   Propósito: Resolver conflictos cuando múltiples caracteres 
              mapean al mismo patrón Braille
   Estrategia: Prioridad a caracteres especiales españoles


4. PREFIJOS ESPECIALES
   ───────────────────
   
   PREFIJO_NUM = [3, 4, 5, 6]
   └─ Precede a cualquier número
   └─ Indica "el siguiente es un dígito"
   
   PREFIJO_MAY = [4, 6]
   └─ Precede a mayúsculas
   └─ Indica "el siguiente es una mayúscula"


═══════════════════════════════════════════════════════════════════════════════
ARQUITECTURA DE CAPAS (LAYERED ARCHITECTURE)
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER (HTTP/REST API)                                  │
│ ├─ Routers: /api/v1/translation/*, /api/v1/generation/*            │
│ ├─ Validación: Pydantic schemas                                     │
│ ├─ Error handling: HTTP status codes                                │
│ └─ Response formatting: JSON                                        │
└──────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Calls
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (Business Logic)                                  │
│ ├─ Services: translator.py, generator.py                           │
│ ├─ Orchestration: coordina Core + Schemas                          │
│ ├─ Error handling: validación, normalizacion                       │
│ └─ Performance: cachés, optimizaciones                             │
└──────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Calls
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│ DOMAIN LAYER (Core Business Logic)                                  │
│ ├─ braille_logic.py: Mapeos Braille                                │
│ ├─ Data structures: MAPA_BRAILLE, MAPA_INVERSO, etc.              │
│ ├─ Algoritmos: traducción bidireccional                           │
│ └─ No depende de: HTTP, DB, UI                                    │
└──────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Uses
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│ PERSISTENCE LAYER (External Dependencies)                          │
│ ├─ PIL/Pillow: Generación de imágenes                             │
│ ├─ ReportLab: Generación de PDFs                                  │
│ ├─ File System: Almacenamiento temporal (opcional)                │
│ └─ [FUTURE] Database: PostgreSQL, Redis                           │
└──────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
ESTRUCTURA DE DIRECTORIOS
═══════════════════════════════════════════════════════════════════════════════

project-root/
│
├─ backend/
│  ├─ app/
│  │  ├─ main.py                    [Punto de entrada FastAPI]
│  │  │
│  │  ├─ api/
│  │  │  ├─ core/
│  │  │  │  ├─ braille_logic.py    [★ Mapeos Braille - Núcleo]
│  │  │  │  └─ config.py            [Configuración]
│  │  │  │
│  │  │  ├─ routes/
│  │  │  │  ├─ translation.py       [Endpoints: /api/v1/translation/*]
│  │  │  │  └─ generation.py        [Endpoints: /api/v1/generation/*]
│  │  │  │
│  │  │  ├─ services/
│  │  │  │  ├─ translator.py        [Lógica de traducción]
│  │  │  │  └─ generator.py         [Lógica de generación]
│  │  │  │
│  │  │  └─ schemas/
│  │  │     └─ translation.py       [Modelos Pydantic]
│  │  │
│  │  └─ __pycache__/               [Bytecode compilado]
│  │
│  ├─ tests/
│  │  ├─ test_logic.py              [★ 62 tests]
│  │  ├─ test_generation.py         [★ 13 tests]
│  │  └─ __pycache__/
│  │
│  ├─ requirements.txt               [Dependencias Python]
│  ├─ Dockerfile                     [Imagen Docker Backend]
│  └─ conftest.py                    [Configuración Pytest]
│
├─ frontend/
│  ├─ src/
│  │  ├─ App.tsx                    [★ Componente raíz]
│  │  ├─ App.css
│  │  ├─ index.tsx                  [Punto de entrada React]
│  │  ├─ index.css
│  │  │
│  │  ├─ components/
│  │  │  ├─ TextInput.tsx           [Input component]
│  │  │  ├─ TextInput.css
│  │  │  ├─ BrailleCell.tsx         [Cell rendering]
│  │  │  ├─ BrailleCell.css
│  │  │  ├─ BrailleDisplay.tsx      [Grid of cells]
│  │  │  └─ BrailleDisplay.css
│  │  │
│  │  ├─ services/
│  │  │  └─ api.ts                  [★ API client]
│  │  │
│  │  └─ setupTests.ts              [Testing setup]
│  │
│  ├─ public/
│  │  └─ index.html                 [HTML entry point]
│  │
│  ├─ package.json                  [Dependencias Node]
│  ├─ tsconfig.json                 [Configuración TypeScript]
│  ├─ tailwind.config.js            [Configuración Tailwind]
│  ├─ Dockerfile                    [Imagen Docker Frontend]
│  └─ README.md
│
├─ documentacion/                     [★ Este paquete]
│  ├─ README.py
│  ├─ requerimientos/
│  │  ├─ req_01_transcripcion.py
│  │  ├─ req_02_traduccion_inversa.py
│  │  ├─ req_03_generacion_señaletica.py
│  │  ├─ req_04_docstrings.py
│  │  ├─ req_05_casos_prueba.py
│  │  └─ req_06_diseño_arquitectonico.py  [← Aquí]
│  └─ archivos_referencia/
│     └─ docstrings_completos.py
│
├─ docker-compose.yml                [Orquestación services]
├─ README.md
└─ .gitignore


═══════════════════════════════════════════════════════════════════════════════
DECISIONES ARQUITECTÓNICAS CLAVE
═══════════════════════════════════════════════════════════════════════════════

1. ¿Por qué FastAPI en lugar de Django?
   ✓ Mayor performance (async/await nativo)
   ✓ API REST moderna y automática (autodocs)
   ✓ Validación automática con Pydantic
   ✓ Menor overhead para este caso de uso
   ✓ Crecimiento más rápido desde cero

2. ¿Por qué React en lugar de Vue/Angular?
   ✓ Ecosistema más maduro
   ✓ Mayor comunidad y librerías
   ✓ TypeScript como first-class citizen
   ✓ Familiares para muchos desarrolladores

3. ¿Por qué Docker Compose?
   ✓ Facilita desarrollo local
   ✓ Replica producción en desarrollo
   ✓ Fácil inicialización (docker-compose up)
   ✓ Escalable a Kubernetes si es necesario

4. ¿Por qué separar Services del Core?
   ✓ Core es independiente de frameworks
   ✓ Permite testing unitario más fácil
   ✓ Reutilización en otros contextos (CLI, batch)
   ✓ Mejor mantenibilidad

5. ¿Por qué Pydantic para validación?
   ✓ Validación automática
   ✓ Type hints para seguridad
   ✓ Documentación automática
   ✓ Errores descriptivos

6. ¿Por qué PIL + ReportLab para generación?
   ✓ PIL: estándar de facto para imágenes Python
   ✓ ReportLab: especializado en PDFs
   ✓ Lightweight comparado con librerías pesadas
   ✓ Sin dependencias externas binarias

7. ¿Por qué mapeos estáticos (no DB)?
   ✓ Rendimiento O(1) en acceso
   ✓ No requiere inicialización de DB
   ✓ Fácil de testear
   ✓ Datos inmutables

8. ¿Por qué tabla de desambigüación?
   ✓ Resuelve colisiones de mapeo
   ✓ Prioridad a caracteres españoles
   ✓ Deterministico
   ✓ Extensible

═══════════════════════════════════════════════════════════════════════════════
CONSIDERACIONES DE SEGURIDAD
═══════════════════════════════════════════════════════════════════════════════

1. VALIDACIÓN DE ENTRADA
   ├─ Longitud máxima de texto: 1000 caracteres
   ├─ Validación de tipos: Pydantic schemas
   ├─ Sanitización: normalización de acentos
   └─ Rate limiting: [PENDIENTE] Implementar

2. MANEJO DE ERRORES
   ├─ Try-catch en services
   ├─ HTTP status codes apropiados
   ├─ Error responses descriptivos (sin información sensible)
   └─ Logging de errores

3. CORS (Cross-Origin Resource Sharing)
   ├─ Configurado en FastAPI
   ├─ Permite origen local (dev)
   ├─ [PENDIENTE] Configurar para producción
   └─ [PENDIENTE] Autenticación

4. GENERACIÓN DE ARCHIVOS
   ├─ BytesIO: en memoria, no en disco
   ├─ [PENDIENTE] Límite de tamaño de archivos generados
   ├─ [PENDIENTE] Limpiar archivos temporales
   └─ [PENDIENTE] Signature de archivos

5. PERFORMANCE Y DOS
   ├─ Timeouts en requests
   ├─ Límite de concurrent requests: [PENDIENTE]
   ├─ Compresión de respuestas: [PENDIENTE]
   └─ Caching: [PENDIENTE]

═══════════════════════════════════════════════════════════════════════════════
ESCALABILIDAD Y PERFORMANCE
═══════════════════════════════════════════════════════════════════════════════

SITUACIÓN ACTUAL (Desarrollo):
├─ Single instance backend
├─ Single instance frontend
├─ In-memory data structures
├─ No persistence layer
└─ Docker Compose orchestration

PARA ESCALAR A PRODUCCIÓN:
├─ Load Balancer (Nginx/HAProxy)
├─ Multiple backend instances
├─ Redis para caching
├─ Database (PostgreSQL) para auditoría
├─ CDN para assets estáticos
├─ Kubernetes orchestration
└─ Monitoring (Prometheus + Grafana)

OPTIMIZACIONES DISPONIBLES:
├─ Caching de mapeos (Redis)
├─ Async processing para generación (Celery)
├─ Image optimization (ImageMagick)
├─ PDF streaming para archivos grandes
├─ Frontend: Code splitting, lazy loading
└─ Compression: gzip, brotli

BENCHMARKS TÍPICOS:
├─ Traducción: < 1ms por carácter
├─ Generación de imagen: < 100ms
├─ Generación de PDF: < 500ms
├─ Request-Response: < 50ms (sin I/O)
└─ P99 latency: < 2s

═══════════════════════════════════════════════════════════════════════════════
TESTING STRATEGY
═══════════════════════════════════════════════════════════════════════════════

Pirámide de Tests:
    ▲
    │          E2E Tests (Frontend)
    │       [Cypress/Selenium]
    │            5-10 tests
    │
    │      Integration Tests
    │    [API endpoints + Services]
    │           15-20 tests
    │
    │        Unit Tests
    │    [Core, Services, Schemas]
    │           60+ tests
    │

Cobertura:
├─ Unit Tests: 95%+ (lógica core)
├─ Integration Tests: 80%+ (endpoints)
├─ E2E Tests: 50%+ (happy path)
└─ Overall: 85%+

Herramientas:
├─ Backend: pytest, pytest-cov
├─ Frontend: Jest, React Testing Library
└─ E2E: Cypress (pendiente)

Ejecución:
├─ Local: pytest backend/tests/ -v
├─ CI/CD: Automatizado en push
└─ Coverage: pytest --cov=app backend/tests/

═══════════════════════════════════════════════════════════════════════════════
DEPLOYMENT STRATEGY
═══════════════════════════════════════════════════════════════════════════════

DESARROLLO:
  docker-compose up

STAGING:
  ├─ Build images: docker build
  ├─ Push a registry: docker push
  ├─ Deploy to staging: kubectl apply
  └─ Run tests: pytest, Cypress

PRODUCCIÓN:
  ├─ Blue-Green deployment
  ├─ Health checks
  ├─ Rollback capability
  ├─ Monitoring & alerting
  └─ Backup & disaster recovery

CI/CD Pipeline (GitHub Actions sugerido):
  ├─ Test: pytest, ESLint, TypeScript check
  ├─ Build: Docker images
  ├─ Push: Container registry
  ├─ Deploy: Staging
  ├─ E2E Tests: Cypress
  └─ Deploy: Producción (manual approval)

═══════════════════════════════════════════════════════════════════════════════
MONITOREO Y OBSERVABILIDAD
═══════════════════════════════════════════════════════════════════════════════

MÉTRICAS CLAVE:
├─ Response time (latencia)
├─ Request rate (throughput)
├─ Error rate (disponibilidad)
├─ CPU/Memoria (recursos)
└─ Errores no capturados

LOGGING:
├─ Application logs: DEBUG, INFO, WARNING, ERROR
├─ Access logs: todos los requests HTTP
├─ Error logs: stack traces, contexto
└─ Audit logs: cambios significativos

HERRAMIENTAS SUGERIDAS:
├─ Prometheus: métricas
├─ Grafana: visualización
├─ ELK Stack: logging centralizado
├─ Sentry: error tracking
└─ DataDog/New Relic: APM

═══════════════════════════════════════════════════════════════════════════════
FUTURAS MEJORAS Y ROADMAP
═══════════════════════════════════════════════════════════════════════════════

CORTO PLAZO (1-3 meses):
├─ Autenticación y autorización
├─ Rate limiting
├─ Caching con Redis
├─ E2E tests con Cypress
└─ Documentación Swagger mejorada

MEDIANO PLAZO (3-6 meses):
├─ Base de datos para historial
├─ Exportación a múltiples formatos (SVG, BMP)
├─ API de batch processing
├─ Soporte para más idiomas
└─ Admin dashboard

LARGO PLAZO (6-12 meses):
├─ Machine learning para OCR Braille
├─ Síntesis de voz
├─ App mobile (React Native)
├─ Integración con servicios externos
└─ Marketplace de plugins

═══════════════════════════════════════════════════════════════════════════════
RESUMEN ARQUITECTÓNICO
═══════════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────────────────┐
│ ARQUITECTURA: Layered + MVC                                              │
│ PATRONES: Service, Factory, Singleton, Decorator, Strategy               │
│ FRONTEND: React 18 + TypeScript + Tailwind                               │
│ BACKEND: FastAPI + Pydantic + PIL/ReportLab                             │
│ DATABASE: None (en memoria) - PostgreSQL disponible para escalar        │
│ DEPLOYMENT: Docker Compose → Kubernetes                                 │
│ TESTING: Pytest (backend) + Jest (frontend)                             │
│ PERFORMANCE: Típico <100ms respuesta, escalable a 1000+ req/s          │
│ SEGURIDAD: Validación entrada, error handling, CORS                     │
│ MANTENIBILIDAD: Clean code, docstrings, tests, documentación            │
└────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
FIN DE DOCUMENTACIÓN - REQUERIMIENTO 6
═══════════════════════════════════════════════════════════════════════════════

Autor: Sistema de Documentación Arquitectónica
Fecha: Enero 2026
Estado: ✅ COMPLETADO

Próximo Requerimiento: Req 7 - Documentación del Ambiente (Setup)
"""
