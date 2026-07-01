from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os, io
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import openpyxl, time
from utils.horarios_parser import actualizar_horarios_excel

router = APIRouter(prefix="/api")

CV_KEY = os.environ["AZURE_CV_KEY"]
CV_ENDPOINT = os.environ["AZURE_CV_ENDPOINT"]
HORARIOS_PATH = "data/Horarios_Cedis.xlsx"

@router.post("/ocr")
async def ocr_imagen(imagen: UploadFile = File(...)):
    client = ComputerVisionClient(CV_ENDPOINT, CognitiveServicesCredentials(CV_KEY))
    
    img_bytes = await imagen.read()
    stream = io.BytesIO(img_bytes)
    
    result = client.read_in_stream(stream, raw=True)
    op_id = result.headers["Operation-Location"].split("/")[-1]
    
    while True:
        status = client.get_read_result(op_id)
        if status.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)
    
    lineas = []
    if status.status == OperationStatusCodes.succeeded:
        for page in status.analyze_result.read_results:
            for line in page.lines:
                lineas.append(line.text)
    
    filas = parsear_tabla_ocr(lineas)
    
    wb = openpyxl.load_workbook(HORARIOS_PATH)
    ws = wb.active
    filas_actualizadas = actualizar_horarios_excel(ws, filas)
    wb.save(HORARIOS_PATH)
    
    return JSONResponse({
        "ok": True,
        "filas_procesadas": filas_actualizadas,
        "preview": filas[:5]
    })

def parsear_tabla_ocr(lineas: list) -> list:
    """
    Extrae filas de datos ignorando encabezados y títulos.
    Detecta líneas que empiezan con un número (número de contenedor).
    """
    filas = []
    for linea in lineas:
        partes = linea.split()
        if not partes:
            continue
        if not partes[0].isdigit():
            continue
        # Formato esperado: NUM | FECHA... | HORA | [HORA_LLEGADA] | [FECHA_LLEGADA] | RUBRO | CONTENEDOR | [CORTINA]
        # Tomamos solo las columnas que necesitamos
        try:
            num = partes[0]
            # El contenedor tiene formato XXXX9999999 (4 letras + 7 dígitos)
            contenedor = next((p for p in partes if len(p)==11 and p[:4].isalpha() and p[4:].isdigit()), None)
            hora = next((p for p in partes if ":" in p and len(p)<=8), None)
            # Cortina: número de 1-2 dígitos al final
            cortina = partes[-1] if partes[-1].isdigit() and len(partes[-1]) <= 2 else None
            # Fecha: buscar "lunes,", "martes,", etc.
            dias = ["lunes","martes","miércoles","miercoles","jueves","viernes","sábado","sabado","domingo"]
            fecha_str = None
            for i, p in enumerate(partes):
                if p.lower().rstrip(",") in dias:
                    fecha_str = " ".join(partes[i:i+5])
                    break
            rubro_words = ["calzado","ropa","otras"]
            rubro = next((p.capitalize() for p in partes if p.lower() in rubro_words), "")
            
            if contenedor and hora:
                filas.append({
                    "numero": num,
                    "fecha": fecha_str or "",
                    "hora": hora,
                    "rubro": rubro,
                    "contenedor": contenedor,
                    "cortina": cortina or ""
                })
        except Exception:
            continue
    return filas