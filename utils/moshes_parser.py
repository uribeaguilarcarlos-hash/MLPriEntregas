from datetime import date, timedelta

MESES = {"ENE":1,"FEB":2,"MAR":3,"ABR":4,"MAY":5,"JUN":6,
          "JUL":7,"AGO":8,"SEP":9,"OCT":10,"NOV":11,"DIC":12}

def parsear_moshes(wb):
    ws = wb.active
    semanas = {}
    fechas = {}

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[1]:
            continue
        ref    = str(row[1]).strip()
        cont   = str(row[2]).strip()
        broker = str(row[3]).strip()
        linea  = str(row[6]).strip() if row[6] else ""
        coment = str(row[9]).upper().strip() if row[9] else ""

        # Prioridad
        if "SUPER URGENTE" in coment:
            prio = "SUPER URGENTE"
        elif "URGENTE" in coment:
            prio = "URGENTE"
        else:
            prio = ""

        # Posible entrega
        pos = coment.find("POSIBLE ENTREGA ")
        if pos == -1:
            continue
        rest = coment[pos+16:]
        parts = rest.split(".")
        if len(parts) < 2:
            continue
        mon_str = parts[0].strip()
        day_str = parts[1].strip().split()[0].split("|")[0]
        if mon_str not in MESES:
            continue
        try:
            fecha = date(2026, MESES[mon_str], int(day_str))
        except ValueError:
            continue

        fk = fecha.strftime("%Y%m%d")
        # Semana (lunes)
        lunes = fecha - timedelta(days=fecha.weekday())
        wk = lunes.strftime("%Y%m%d")

        # Semanas
        if wk not in semanas:
            semanas[wk] = []
        semanas[wk].append({"broker": broker, "fecha": fk, "ref": ref, "cont": cont})

        # Fechas/checklist
        if fk not in fechas:
            fechas[fk] = []
        fechas[fk].append({
            "broker": broker, "ref": ref, "cont": cont,
            "linea": linea, "prio": prio
        })

    return {"semanas": semanas, "fechas": fechas}