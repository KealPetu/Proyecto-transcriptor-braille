# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import translation

app = FastAPI(
    title="Braille Translator API",
    description="API para la traducción bidireccional Español <-> Braille",
    version="1.0.0"
)

# Configuración de CORS
# Permitimos que el frontend (React) en localhost:3000 o 5173 acceda a la API
origins = [
    "http://localhost",
    "http://localhost:3000", # React estandar
    "http://localhost:5173", # Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(translation.router, prefix="/api/v1/translation", tags=["Translation"])

@app.get("/")
def read_root():
    return {"message": "API de Traducción Braille v1.0. Estado: Activo"}

if __name__ == "__main__":
    import uvicorn
    # "app.main:app" indica: archivo main.py, objeto app
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)