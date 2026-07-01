from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import openpyxl, io
from utils.moshes_parser import parsear_moshes
from utils.horarios_parser import parsear_horarios

router = APIRouter(prefix="/api")

@router.post("/actualizar")
async def actualizar(
    moshes: UploadFile = File(...),
    horarios: UploadFile = File(...)
):
    wb_m = openpyxl.load_workbook(io.BytesIO(await moshes.read()), data_only=True)
    wb_h = openpyxl.load_workbook(io.BytesIO(await horarios.read()), data_only=True)

    datos_moshes = parsear_moshes(wb_m)
    datos_horarios = parsear_horarios(wb_h)

    return JSONResponse({
        "resumen": datos_moshes["semanas"],
        "checklist": datos_moshes["fechas"],
        "horarios": datos_horarios
    })