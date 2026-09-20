#!/usr/bin/env python3
"""
Genera los informes financieros de Berts Solutions SL a partir de los CSV en /datos/.
Uso: python3 generar_informes.py
No requiere librerías externas (solo Python 3 estándar).
"""
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / "datos"
INFORMES = BASE / "informes"
INFORMES.mkdir(exist_ok=True)

HOY = datetime.now().strftime("%Y-%m-%d")


def leer(nombre):
    path = DATOS / nombre
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    # Descarta las filas de plantilla/ejemplo para no mezclarlas con datos reales.
    return [f for f in filas if "FILA DE EJEMPLO" not in (f.get("notas") or "")]


def num(fila, campo):
    try:
        return float(fila.get(campo) or 0)
    except ValueError:
        return 0.0


def mes_de(fila, campo_fecha="fecha_emision"):
    fecha = fila.get(campo_fecha) or ""
    return fecha[:7] if len(fecha) >= 7 else "sin_fecha"


def trimestre_de(fila, campo_fecha="fecha_emision"):
    mes = mes_de(fila, campo_fecha)
    if mes == "sin_fecha":
        return "sin_fecha"
    anio, mm = mes.split("-")
    t = (int(mm) - 1) // 3 + 1
    return f"{anio}-T{t}"


def cabecera(titulo):
    return (
        f"# {titulo}\n\n"
        f"_Generado automáticamente el {HOY}. No editar a mano — se sobrescribe al volver a ejecutar el script._\n\n"
    )


def generar_cuenta_resultados():
    ing = leer("facturas_emitidas.csv")
    gas = leer("facturas_recibidas.csv")

    out = cabecera("Cuenta de Resultados (simplificada)")

    if not ing and not gas:
        out += (
            "Todavía no hay datos reales cargados en `facturas_emitidas.csv` ni `facturas_recibidas.csv`.\n"
            "Añade filas reales (borrando las marcadas como FILA DE EJEMPLO) y vuelve a ejecutar este script.\n"
        )
    else:
        ing_total = sum(num(f, "base_imponible_eur") for f in ing)
        gas_total = sum(num(f, "base_imponible_eur") for f in gas)
        resultado = ing_total - gas_total

        out += "## Resumen global\n\n"
        out += f"- **Ingresos (base imponible)**: {ing_total:,.2f} €\n"
        out += f"- **Gastos (base imponible)**: {gas_total:,.2f} €\n"
        out += f"- **Resultado antes de impuestos**: {resultado:,.2f} €\n\n"

        lineas = sorted({f.get("linea_negocio", "") for f in ing} | {f.get("linea_negocio", "") for f in gas})
        if lineas:
            out += "## Por línea de negocio\n\n"
            out += "| Línea | Ingresos € | Gastos € | Resultado € |\n|---|---|---|---|\n"
            for linea in lineas:
                i = sum(num(f, "base_imponible_eur") for f in ing if f.get("linea_negocio") == linea)
                g = sum(num(f, "base_imponible_eur") for f in gas if f.get("linea_negocio") == linea)
                out += f"| {linea} | {i:,.2f} | {g:,.2f} | {i - g:,.2f} |\n"
            out += "\n"

        trimestres = sorted({trimestre_de(f) for f in ing} | {trimestre_de(f) for f in gas})
        if trimestres:
            out += "## Por trimestre\n\n"
            out += "| Trimestre | Ingresos € | Gastos € | Resultado € |\n|---|---|---|---|\n"
            for t in trimestres:
                i = sum(num(f, "base_imponible_eur") for f in ing if trimestre_de(f) == t)
                g = sum(num(f, "base_imponible_eur") for f in gas if trimestre_de(f) == t)
                out += f"| {t} | {i:,.2f} | {g:,.2f} | {i - g:,.2f} |\n"
            out += "\n"

        meses = sorted({mes_de(f) for f in ing} | {mes_de(f) for f in gas})
        if meses:
            out += "## Por mes\n\n"
            out += "| Mes | Ingresos € | Gastos € | Resultado € |\n|---|---|---|---|\n"
            for mes in meses:
                i = sum(num(f, "base_imponible_eur") for f in ing if mes_de(f) == mes)
                g = sum(num(f, "base_imponible_eur") for f in gas if mes_de(f) == mes)
                out += f"| {mes} | {i:,.2f} | {g:,.2f} | {i - g:,.2f} |\n"

    (INFORMES / "cuenta_resultados.md").write_text(out, encoding="utf-8")


def generar_iva():
    ing = leer("facturas_emitidas.csv")
    gas = leer("facturas_recibidas.csv")

    out = cabecera("IVA repercutido vs soportado, por trimestre")
    out += (
        "Esto es una estimación para contrastar con el modelo 303 que presente la gestoría "
        "(el IVA en España se liquida por trimestres), no sustituye la declaración oficial.\n\n"
    )

    if not ing and not gas:
        out += "Todavía no hay datos reales cargados.\n"
    else:
        trimestres = sorted({trimestre_de(f) for f in ing} | {trimestre_de(f) for f in gas})
        out += "| Trimestre | IVA repercutido € | IVA soportado € | A ingresar / (a compensar) € |\n|---|---|---|---|\n"
        for t in trimestres:
            rep = sum(num(f, "cuota_iva_eur") for f in ing if trimestre_de(f) == t)
            sop = sum(num(f, "cuota_iva_eur") for f in gas if trimestre_de(f) == t)
            out += f"| {t} | {rep:,.2f} | {sop:,.2f} | {rep - sop:,.2f} |\n"

        iva_repercutido = sum(num(f, "cuota_iva_eur") for f in ing)
        iva_soportado = sum(num(f, "cuota_iva_eur") for f in gas)
        out += f"\n**Total acumulado**: repercutido {iva_repercutido:,.2f} € — soportado {iva_soportado:,.2f} € — diferencia {iva_repercutido - iva_soportado:,.2f} €\n"

    (INFORMES / "iva.md").write_text(out, encoding="utf-8")


def generar_rentabilidad_vehiculos():
    ing = [f for f in leer("facturas_emitidas.csv") if f.get("vehiculo_id")]
    gas = [f for f in leer("facturas_recibidas.csv") if f.get("vehiculo_id")]
    inv = leer("inversiones_vehiculos.csv")

    out = cabecera("Rentabilidad por vehículo")
    out += "Se calcula a partir de las facturas emitidas/recibidas que tienen `vehiculo_id` relleno.\n\n"

    if not ing and not gas:
        out += "Todavía no hay facturas con `vehiculo_id` relleno.\n"
    else:
        vehiculos = sorted({f.get("vehiculo_id") for f in ing} | {f.get("vehiculo_id") for f in gas})
        coste_por_vehiculo = {f.get("vehiculo_id"): num(f, "coste_total_eur") for f in inv}
        nombre_por_vehiculo = {f.get("vehiculo_id"): f.get("marca_modelo", "") for f in inv}

        out += "## Ingresos, gastos y resultado por vehículo (acumulado)\n\n"
        out += "| Vehículo | Ingresos € | Gastos € | Resultado € | Inversión € | % recuperado |\n|---|---|---|---|---|---|\n"
        for vid in vehiculos:
            i = sum(num(f, "base_imponible_eur") for f in ing if f.get("vehiculo_id") == vid)
            g = sum(num(f, "base_imponible_eur") for f in gas if f.get("vehiculo_id") == vid)
            resultado = i - g
            coste = coste_por_vehiculo.get(vid)
            pct = f"{(resultado / coste * 100):,.1f}%" if coste else "—"
            nombre = nombre_por_vehiculo.get(vid, "")
            out += f"| {nombre} ({vid}) | {i:,.2f} | {g:,.2f} | {resultado:,.2f} | {coste or 0:,.2f} | {pct} |\n"

    (INFORMES / "rentabilidad_vehiculos.md").write_text(out, encoding="utf-8")


def generar_balance_resumen():
    apo = leer("aportaciones_capital.csv")
    inv = leer("inversiones_vehiculos.csv")

    out = cabecera("Resumen patrimonial simplificado")

    if not apo and not inv:
        out += "Todavía no hay datos reales en `aportaciones_capital.csv` ni `inversiones_vehiculos.csv`.\n"
    else:
        if apo:
            out += "## Aportaciones por socio\n\n"
            out += "| Socio | Total aportado € | De la cual préstamo a devolver € |\n|---|---|---|\n"
            socios = defaultdict(lambda: {"total": 0.0, "prestamo": 0.0})
            for f in apo:
                s = socios[f.get("socio", "")]
                importe = num(f, "importe_eur")
                s["total"] += importe
                if (f.get("pendiente_de_devolucion_si_no") or "").strip().lower() == "si":
                    s["prestamo"] += importe
            for socio, s in sorted(socios.items()):
                out += f"| {socio} | {s['total']:,.2f} | {s['prestamo']:,.2f} |\n"
            out += "\n"

        if inv:
            out += "## Inversión en vehículos (activo)\n\n"
            total_invertido = sum(num(f, "coste_total_eur") for f in inv)
            out += f"- **Total invertido en vehículos**: {total_invertido:,.2f} €\n\n"
            out += "| Vehículo | Coste total € | Aportado por | Estado |\n|---|---|---|---|\n"
            for f in inv:
                out += (
                    f"| {f.get('marca_modelo','')} ({f.get('vehiculo_id','')}) "
                    f"| {num(f, 'coste_total_eur'):,.2f} "
                    f"| {f.get('aportado_por','')} "
                    f"| {f.get('estado_actual','')} |\n"
                )

    (INFORMES / "balance_resumen.md").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    generar_cuenta_resultados()
    generar_iva()
    generar_rentabilidad_vehiculos()
    generar_balance_resumen()
    print(f"Informes generados en {INFORMES}")
