from datetime import date

MESES_ES = {1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",
            7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
DIAS_ES = {0:"lunes",1:"martes",2:"miércoles",3:"jueves",4:"viernes",5:"sábado",6:"domingo"}

def construir_mensaje(fecha_key: str, checklist: list) -> str:
    y, m, d = int(fecha_key[:4]), int(fecha_key[4:6]), int(fecha_key[6:])
    fecha = date(y, m, d)
    fecha_str = f"{DIAS_ES[fecha.weekday()]} {d} de {MESES_ES[m]}"

    calzado, ropa, otras = [], [], []
    for item in checklist:
        cont  = item.get("cont", "")
        linea = item.get("linea", "").upper()
        nota  = ""
        if "," in linea:
            parts = [p.strip().capitalize() for p in linea.split(",")]
            nota  = f" *Consolidado {'-'.join(parts)}*"
        
        entrada = cont + nota
        if "CALZADO" in linea:
            calzado.append(entrada)
        elif "ROPA" in linea:
            ropa.append(entrada)
        else:
            otras.append(entrada)

    lines = [
        "Buen dia",
        f"Les informo las entregas del dia {fecha_str}",
        "TULTITLAN",
    ]
    if calzado:
        lines.append("Calzado")
        lines.extend(calzado)
    if ropa:
        lines.append("Ropa")
        lines.extend(ropa)
    if otras:
        lines.append("Otras lineas")
        lines.extend(otras)

    return "\n".join(lines)