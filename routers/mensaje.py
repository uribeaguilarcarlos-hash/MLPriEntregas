from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.mensaje_builder import construir_mensaje

router = APIRouter(prefix="/api")

class MensajeRequest(BaseModel):
    fecha_key: str          # "20260630"
    checklist: list         # filas del día

@router.post("/mensaje")
def generar_mensaje(req: MensajeRequest):
    texto = construir_mensaje(req.fecha_key, req.checklist)
    return JSONResponse({"texto": texto})