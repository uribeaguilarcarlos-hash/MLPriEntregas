from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI(title="API de Gestión y Horarios CEDIS")

# Esto es súper importante para que tu frontend (web) pueda hablar con este backend sin bloqueos de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ruta_raiz():
    return {"mensaje": "¡El backend está funcionando al 100%!"}

# 1. Endpoint para procesar el Excel y devolver el texto
@app.post("/generar-reporte/")
async def generar_reporte(archivo: UploadFile = File(...)):
    # Leemos el Excel que el usuario suba desde la página web
    contenido = await archivo.read()
    df = pd.read_excel(io.BytesIO(contenido))
    
    # Aquí vamos a meter la lógica de extracción de datos. 
    # Justo en esta parte es donde aplicaremos la regla para que el reporte le dé prioridad al campo "BROKER" sobre "CONSIGNATARIO".
    
    # [Lógica de transformación de datos en construcción]
    
    texto_final = "Aquí irá el texto estructurado listo para que lo muestres en la ventana emergente y lo copien."
    
    return {"texto_generado": texto_final}

# 2. Endpoint para el OCR de los horarios
@app.post("/agregar-horarios-ocr/")
async def agregar_horarios(imagen: UploadFile = File(...)):
    # Recibiremos la imagen pegada en la web
    contenido_imagen = await imagen.read()
    
    # [Aquí irá la conexión con Azure AI para leer la imagen]
    # [Luego tomaremos ese texto y lo agregaremos al archivo Excel de Horarios Cedis]
    
    return {"mensaje": "Imagen recibida. Los horarios se están procesando y agregando al Excel..."}