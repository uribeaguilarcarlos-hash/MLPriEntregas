import pandas as pd
import numpy as np
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Aquí inicializamos la aplicación
app = FastAPI(title="API de Gestión y Horarios CEDIS")

# Esto permite que tu página web se comunique con este backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AQUÍ ESTÁ EL ENDPOINT DEL QUE HABLAMOS ---
# Fíjate cómo /generar-reporte/ es solo la instrucción que le dice a la app 
# qué hacer cuando la página web llame a esta dirección.
@app.post("/generar-reporte/")
async def generar_reporte(archivo: UploadFile = File(...)):
    # Leemos el archivo que llega desde la página web
    contenido = await archivo.read()
    
    try:
        # Lo pasamos a un DataFrame de pandas
        df = pd.read_excel(io.BytesIO(contenido))
    except Exception as e:
        return {"error": "Hubo un problema leyendo el archivo. Asegúrate de que sea un Excel válido."}
    
    # Estandarizamos los nombres de las columnas
    df.columns = df.columns.str.strip().str.upper()

    # Lógica de prioridad: Tomar BROKER, si no hay, tomar CONSIGNATARIO
    if 'BROKER' in df.columns and 'CONSIGNATARIO' in df.columns:
        df['RESPONSABLE_REPORTE'] = df['BROKER'].fillna(df['CONSIGNATARIO'])
    elif 'BROKER' in df.columns:
        df['RESPONSABLE_REPORTE'] = df['BROKER']
    else:
        df['RESPONSABLE_REPORTE'] = df.get('CONSIGNATARIO', 'SIN ASIGNAR')

    # Reemplazamos espacios vacíos
    df = df.fillna("")

    # Armamos el texto plano
    texto_final = "--- REPORTE DE CONTENEDORES ---\n\n"
    
    for index, fila in df.iterrows():
        contenedor = fila.get('CONTENEDOR', 'N/A')
        responsable = fila.get('RESPONSABLE_REPORTE', 'N/A')
        texto_final += f"CONTENEDOR: {contenedor} | RESPONSABLE: {responsable}\n"
        
    texto_final += "\n---------------------------------"

    return {"texto_generado": texto_final}
