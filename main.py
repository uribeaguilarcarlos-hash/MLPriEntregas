from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from routers import actualizar, mensaje, ocr

app = FastAPI(title="Resumen Contenedores")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(actualizar.router)
app.include_router(mensaje.router)
app.include_router(ocr.router)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})