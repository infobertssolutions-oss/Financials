#!/usr/bin/env python3
"""
Motor contable de Berts Solutions SL.

Lee los CSV de /datos/ y los convierte en asientos de partida doble según el
Plan General de Contabilidad de Pymes (PGC Pymes). A partir de esos asientos se
construyen el Balance de Situación y la Cuenta de Pérdidas y Ganancias.

Nadie tiene que saber contabilidad para alimentarlo: cada fila de los CSV
(una factura, una compra de vehículo, una aportación...) se traduce sola en su
asiento. Solo `asientos_manuales.csv` admite asientos escritos a mano, para lo
que no encaje en ningún otro sitio.

No requiere librerías externas.
"""
import calendar
import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / "datos"

# Primer ejercicio que se contabiliza aquí. Lo anterior entra como saldo de
# apertura (datos/saldos_apertura.csv), sacado de las cuentas de Fisama.
INICIO_EJERCICIO = date(2026, 1, 1)
FECHA_APERTURA = INICIO_EJERCICIO - timedelta(days=1)

CUENTA_BANCO = "5720"
CUENTA_PENDIENTE = "5550"  # Partidas pendientes de aplicación: dinero cuyo origen/destino aún no sabemos
CUENTA_SOCIOS = "5510"
CUENTA_APORTACIONES = "1180"
CUENTA_CLIENTES = "4300"
CUENTA_ACREEDORES = "4100"
CUENTA_PROVEEDORES = "4000"
CUENTA_IVA_SOPORTADO = "4720"
CUENTA_IVA_REPERCUTIDO = "4770"
CUENTA_IVA_A_COMPENSAR = "4700"
CUENTA_IVA_A_PAGAR = "4750"
CUENTA_RETENCIONES = "4751"
CUENTA_INMOVILIZADO_VEHICULOS = "2180"
CUENTA_AMORT_ACUM_VEHICULOS = "2818"
CUENTA_DOTACION_AMORT = "6810"
CUENTA_PERDIDA_INMOVILIZADO = "6710"
CUENTA_BENEFICIO_INMOVILIZADO = "7710"
CUENTA_RESULTADO = "1290"

PLAN_CUENTAS = {
    "1000": "Capital social",
    "1120": "Reserva legal",
    "1130": "Reservas voluntarias",
    "1180": "Aportaciones de socios o propietarios",
    "1200": "Remanente",
    "1210": "Resultados negativos de ejercicios anteriores",
    "1290": "Resultado del ejercicio",
    "1630": "Otras deudas a l/p con partes vinculadas (préstamo de socios)",
    "1700": "Deudas a l/p con entidades de crédito",
    "2130": "Maquinaria",
    "2180": "Elementos de transporte",
    "2818": "Amortización acumulada de elementos de transporte",
    "4000": "Proveedores",
    "4100": "Acreedores por prestaciones de servicios",
    "4300": "Clientes",
    "4650": "Remuneraciones pendientes de pago",
    "4700": "H.P. deudora por IVA (a compensar)",
    "4709": "H.P. deudora por devolución de impuestos",
    "4720": "H.P. IVA soportado",
    "4750": "H.P. acreedora por IVA (a ingresar)",
    "4751": "H.P. acreedora por retenciones practicadas (modelo 111)",
    "4752": "H.P. acreedora por Impuesto sobre Sociedades",
    "4760": "Organismos de la Seguridad Social, acreedores",
    "4770": "H.P. IVA repercutido",
    "4800": "Gastos anticipados",
    "5200": "Deudas a c/p con entidades de crédito",
    "5510": "Cuenta corriente con socios",
    "5550": "Partidas pendientes de aplicación",
    "5720": "Bancos c/c BBVA",
    "6220": "Reparaciones y conservación",
    "6230": "Servicios de profesionales independientes",
    "6250": "Primas de seguros",
    "6260": "Servicios bancarios",
    "6270": "Publicidad y propaganda",
    "6280": "Suministros (combustible, luz, teléfono...)",
    "6290": "Otros servicios",
    "6300": "Impuesto sobre beneficios",
    "6310": "Otros tributos (IVTM...)",
    "6400": "Sueldos y salarios",
    "6420": "Seguridad Social a cargo de la empresa",
    "6620": "Intereses de deudas",
    "6690": "Otros gastos financieros",
    "6710": "Pérdidas procedentes del inmovilizado material",
    "6780": "Gastos excepcionales (sanciones...)",
    "6810": "Amortización del inmovilizado material",
    "6910": "Pérdidas por deterioro del inmovilizado material",
    "7050": "Prestaciones de servicios (alquileres)",
    "7590": "Ingresos por servicios diversos",
    "7690": "Otros ingresos financieros",
    "7710": "Beneficios procedentes del inmovilizado material",
    "7780": "Ingresos excepcionales",
}


def nombre_cuenta(cuenta):
    if cuenta in PLAN_CUENTAS:
        return PLAN_CUENTAS[cuenta]
    for c, nombre in PLAN_CUENTAS.items():
        if c[:3] == cuenta[:3]:
            return nombre
    return f"Cuenta {cuenta}"


# ---------------------------------------------------------------------------
# Estructura de los estados financieros (modelo PGC Pymes)
#
# Cada línea es (código, texto, nivel, especificación). Especificaciones:
#   ("cuentas", [prefijos], signo)  saldo de las cuentas que empiezan por esos prefijos
#                                   (signo +1 = deudor positivo, -1 = acreedor positivo)
#   ("deudor", clave) / ("acreedor", clave)  para cuentas que pueden salir a un lado u
#                                   otro del balance según su saldo (socios, partidas pendientes)
#   ("suma", [códigos])             suma de otras líneas
# ---------------------------------------------------------------------------
CUENTAS_DUALES = {"D551": ["551"], "D555": ["555"]}

BALANCE_ACTIVO = [
    ("A", "A) ACTIVO NO CORRIENTE", 0, ("suma", ["AI", "AII", "AV"])),
    ("AI", "I. Inmovilizado intangible", 1, ("cuentas", ["20", "280", "290"], 1)),
    ("AII", "II. Inmovilizado material", 1, ("suma", ["AII1", "AII2", "AII3"])),
    ("AII1", "Elementos de transporte (vehículos)", 2, ("cuentas", ["218"], 1)),
    ("AII2", "Otro inmovilizado material", 2,
     ("cuentas", ["210", "211", "212", "213", "214", "215", "216", "217", "219", "23"], 1)),
    ("AII3", "Amortización acumulada", 2, ("cuentas", ["281", "291"], 1)),
    ("AV", "V. Inversiones financieras a largo plazo", 1, ("cuentas", ["25", "26"], 1)),
    ("B", "B) ACTIVO CORRIENTE", 0, ("suma", ["BII", "BIII", "BVI", "BVII"])),
    ("BII", "II. Existencias", 1, ("cuentas", ["3"], 1)),
    ("BIII", "III. Deudores comerciales y otras cuentas a cobrar", 1,
     ("suma", ["BIII1", "BIII2", "BIII3", "BIII4"])),
    ("BIII1", "1. Clientes por ventas y prestaciones de servicios", 2, ("cuentas", ["43", "44"], 1)),
    ("BIII2", "2. Hacienda Pública deudora (IVA soportado / a compensar)", 2,
     ("cuentas", ["470", "471", "472", "473"], 1)),
    ("BIII3", "3. Socios deudores", 2, ("deudor", "D551")),
    ("BIII4", "4. Partidas pendientes de aplicación (saldo deudor)", 2, ("deudor", "D555")),
    ("BVI", "VI. Periodificaciones a corto plazo", 1, ("cuentas", ["480"], 1)),
    ("BVII", "VII. Efectivo y otros activos líquidos equivalentes", 1, ("cuentas", ["57"], 1)),
    ("TA", "TOTAL ACTIVO (A + B)", 0, ("suma", ["A", "B"])),
]

BALANCE_PASIVO = [
    ("PA", "A) PATRIMONIO NETO", 0, ("suma", ["PAI", "PAIII", "PAV", "PAVI", "PAVII"])),
    ("PAI", "I. Capital", 1, ("cuentas", ["100", "103", "104"], -1)),
    ("PAIII", "III. Reservas", 1, ("cuentas", ["110", "112", "113", "114", "115", "119"], -1)),
    ("PAV", "V. Resultados de ejercicios anteriores", 1, ("cuentas", ["120", "121"], -1)),
    ("PAVI", "VI. Otras aportaciones de socios", 1, ("cuentas", ["118"], -1)),
    ("PAVII", "VII. Resultado del ejercicio", 1, ("cuentas", ["129", "6", "7"], -1)),
    ("PB", "B) PASIVO NO CORRIENTE", 0, ("suma", ["PBII"])),
    ("PBII", "II. Deudas a largo plazo (bancos, préstamos de socios)", 1, ("cuentas", ["16", "17"], -1)),
    ("PC", "C) PASIVO CORRIENTE", 0, ("suma", ["PCIII", "PCV"])),
    ("PCIII", "III. Deudas a corto plazo", 1, ("suma", ["PCIII1", "PCIII2", "PCIII3"])),
    ("PCIII1", "1. Deudas con entidades de crédito", 2, ("cuentas", ["520", "521", "523", "524"], -1)),
    ("PCIII2", "2. Deudas con socios", 2, ("acreedor", "D551")),
    ("PCIII3", "3. Partidas pendientes de aplicación (saldo acreedor)", 2, ("acreedor", "D555")),
    ("PCV", "V. Acreedores comerciales y otras cuentas a pagar", 1, ("suma", ["PCV1", "PCV2", "PCV3"])),
    ("PCV1", "1. Proveedores y acreedores", 2, ("cuentas", ["40", "41"], -1)),
    ("PCV2", "2. Hacienda Pública acreedora (IVA, retenciones, Sociedades)", 2,
     ("cuentas", ["475", "477"], -1)),
    ("PCV3", "3. Seguridad Social y personal", 2, ("cuentas", ["465", "476"], -1)),
    ("TP", "TOTAL PATRIMONIO NETO Y PASIVO (A + B + C)", 0, ("suma", ["PA", "PB", "PC"])),
]

PYG = [
    ("P1", "1. Importe neto de la cifra de negocios", 1, ("cuentas", ["70"], -1)),
    ("P4", "4. Aprovisionamientos", 1, ("cuentas", ["60", "61"], -1)),
    ("P5", "5. Otros ingresos de explotación", 1, ("cuentas", ["74", "75"], -1)),
    ("P6", "6. Gastos de personal", 1, ("cuentas", ["64"], -1)),
    ("P7", "7. Otros gastos de explotación", 1, ("suma", ["P7a", "P7b", "P7c"])),
    ("P7a", "a) Servicios exteriores", 2, ("cuentas", ["62"], -1)),
    ("P7b", "b) Tributos", 2, ("cuentas", ["631", "634", "636", "639"], -1)),
    ("P7c", "c) Otros gastos de gestión corriente", 2, ("cuentas", ["65", "694", "695", "794"], -1)),
    ("P8", "8. Amortización del inmovilizado", 1, ("cuentas", ["68"], -1)),
    ("P11", "11. Deterioro y resultado por enajenaciones del inmovilizado", 1,
     ("cuentas", ["670", "671", "672", "690", "691", "692", "770", "771", "772", "790", "791", "792"], -1)),
    ("P12", "12. Otros resultados", 1, ("cuentas", ["678", "778"], -1)),
    ("A1", "A.1) RESULTADO DE EXPLOTACIÓN", 0,
     ("suma", ["P1", "P4", "P5", "P6", "P7", "P8", "P11", "P12"])),
    ("P13", "13. Ingresos financieros", 1, ("cuentas", ["760", "761", "762", "769"], -1)),
    ("P14", "14. Gastos financieros", 1, ("cuentas", ["661", "662", "663", "664", "665", "669"], -1)),
    ("P16", "16. Diferencias de cambio", 1, ("cuentas", ["668", "768"], -1)),
    ("A2", "A.2) RESULTADO FINANCIERO", 0, ("suma", ["P13", "P14", "P16"])),
    ("A3", "A.3) RESULTADO ANTES DE IMPUESTOS", 0, ("suma", ["A1", "A2"])),
    ("P17", "17. Impuestos sobre beneficios", 1, ("cuentas", ["630", "633", "638"], -1)),
    ("A4", "A.4) RESULTADO DEL EJERCICIO", 0, ("suma", ["A3", "P17"])),
]

# PyG 2025 tal como la presentó Fisama (documentos/cuentas_anuales/), para comparar.
PYG_2025_FISAMA = {"P1": 2574.25, "P7a": -2509.37}


def _mapa(lineas):
    """Devuelve [(prefijo, código_línea)] ordenado de prefijo más largo a más corto."""
    pares = []
    for codigo, _, _, spec in lineas:
        if spec[0] == "cuentas":
            pares += [(p, codigo) for p in spec[1]]
        elif spec[0] in ("deudor", "acreedor"):
            pares += [(p, spec[1]) for p in CUENTAS_DUALES[spec[1]]]
    return sorted(set(pares), key=lambda x: -len(x[0]))


_MAPA_BALANCE = _mapa(BALANCE_ACTIVO + BALANCE_PASIVO)
_MAPA_PYG = _mapa(PYG)


def linea_balance(cuenta):
    for prefijo, codigo in _MAPA_BALANCE:
        if cuenta.startswith(prefijo):
            return codigo
    return ""


def linea_pyg(cuenta):
    if cuenta[:1] not in ("6", "7"):
        return ""
    for prefijo, codigo in _MAPA_PYG:
        if cuenta.startswith(prefijo):
            return codigo
    return ""


# ---------------------------------------------------------------------------
# Utilidades de lectura
# ---------------------------------------------------------------------------
def leer(nombre):
    path = DATOS / nombre
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [
            {k: (v or "").strip() for k, v in fila.items()}
            for fila in csv.DictReader(f)
            if any((v or "").strip() for v in fila.values())
        ]


def num(fila, campo):
    valor = (fila.get(campo) or "").replace(",", ".")
    try:
        return round(float(valor), 2) if valor else 0.0
    except ValueError:
        return 0.0


def fecha(texto):
    if not texto:
        return None
    return date.fromisoformat(texto[:10])


def eur(v):
    """Formato español: 1.234,56 €"""
    v = round(v, 2) or 0.0
    texto = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-{texto} €" if v < 0 else f"{texto} €"


def fin_de_mes(d):
    return date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])


def fin_de_trimestre(anio, t):
    return fin_de_mes(date(anio, t * 3, 1))


def trimestre(d):
    return f"{d.year}-T{(d.month - 1) // 3 + 1}"


# ---------------------------------------------------------------------------
# Libro diario
# ---------------------------------------------------------------------------
TIPOS = {
    "APE": "Apertura",
    "MAN": "Asiento manual",
    "APO": "Aportación de socios",
    "COM": "Compra de vehículo",
    "FRR": "Factura recibida",
    "PAG": "Pago",
    "FRE": "Factura emitida",
    "COB": "Cobro",
    "VTA": "Venta de inmovilizado",
    "AMO": "Amortización",
    "IVA": "Liquidación trimestral de IVA",
    "REG": "Cierre del ejercicio",
}
ORDEN_TIPOS = list(TIPOS)


@dataclass
class Apunte:
    asiento: int
    fecha: date
    cuenta: str
    concepto: str
    debe: float
    haber: float
    tipo: str
    vehiculo: str
    documento: str

    @property
    def saldo(self):
        return round(self.debe - self.haber, 2)


@dataclass
class Aviso:
    prioridad: str  # "ALTA", "MEDIA", "BAJA"
    tema: str
    detalle: str


class Contabilidad:
    def __init__(self, corte):
        self.corte = corte
        self._asientos = []  # (fecha, tipo, documento, [(cuenta, debe, haber, concepto, vehiculo)])
        self.apuntes = []
        self.avisos = []
        self.vehiculos = []
        self.liquidaciones_iva = []
        self.ventas_inmovilizado = []

    # -- registro -------------------------------------------------------
    def aviso(self, prioridad, tema, detalle):
        self.avisos.append(Aviso(prioridad, tema, detalle))

    def asiento(self, fecha_asiento, tipo, documento, lineas):
        lineas = [
            (c, round(d, 2), round(h, 2), concepto, veh)
            for c, d, h, concepto, veh in lineas
            if round(d, 2) or round(h, 2)
        ]
        if not lineas:
            return
        debe = round(sum(l[1] for l in lineas), 2)
        haber = round(sum(l[2] for l in lineas), 2)
        if abs(debe - haber) > 0.005:
            raise ValueError(
                f"Asiento descuadrado ({documento}, {fecha_asiento}): debe {debe} ≠ haber {haber}"
            )
        self._asientos.append((fecha_asiento, tipo, documento, lineas))
        # Mantener los apuntes siempre al día para poder consultar saldos intermedios.
        for c, d, h, concepto, veh in lineas:
            self.apuntes.append(Apunte(0, fecha_asiento, c, concepto, d, h, tipo, veh, documento))

    def numerar(self):
        self._asientos.sort(key=lambda a: (a[0], ORDEN_TIPOS.index(a[1])))
        self.apuntes = []
        for n, (f, tipo, doc, lineas) in enumerate(self._asientos, start=1):
            for c, d, h, concepto, veh in lineas:
                self.apuntes.append(Apunte(n, f, c, concepto, d, h, tipo, veh, doc))

    # -- consultas ------------------------------------------------------
    def saldo(self, prefijos, hasta=None, desde=None, vehiculo=None, excluir_tipos=()):
        if isinstance(prefijos, str):
            prefijos = [prefijos]
        total = 0.0
        for a in self.apuntes:
            if hasta and a.fecha > hasta:
                continue
            if desde and a.fecha < desde:
                continue
            if vehiculo is not None and a.vehiculo != vehiculo:
                continue
            if a.tipo in excluir_tipos:
                continue
            if any(a.cuenta.startswith(p) for p in prefijos):
                total += a.saldo
        return round(total, 2)

    def valor_lineas(self, lineas, hasta, desde=None, pyg=False):
        """Calcula el valor de cada línea de un estado financiero."""
        excluir = ("REG",) if pyg else ()
        mapa = linea_pyg if pyg else linea_balance
        por_codigo = defaultdict(float)
        for a in self.apuntes:
            if a.fecha > hasta or (desde and a.fecha < desde) or a.tipo in excluir:
                continue
            codigo = mapa(a.cuenta)
            if codigo:
                por_codigo[codigo] += a.saldo
        valores = {}
        todas = {l[0]: l for l in lineas}

        def calcular(codigo):
            if codigo in valores:
                return valores[codigo]
            spec = todas[codigo][3]
            if spec[0] == "cuentas":
                v = spec[2] * por_codigo.get(codigo, 0.0)
            elif spec[0] == "deudor":
                v = max(0.0, por_codigo.get(spec[1], 0.0))
            elif spec[0] == "acreedor":
                v = max(0.0, -por_codigo.get(spec[1], 0.0))
            else:
                v = sum(calcular(c) for c in spec[1])
            valores[codigo] = round(v, 2) or 0.0
            return valores[codigo]

        for codigo in todas:
            calcular(codigo)
        return valores

    def coste_vehiculo(self, vid, hasta):
        return self.saldo(CUENTA_INMOVILIZADO_VEHICULOS[:3], hasta=hasta, vehiculo=vid)

    def amortizacion_acumulada(self, vid, hasta):
        return -self.saldo(CUENTA_AMORT_ACUM_VEHICULOS[:3], hasta=hasta, vehiculo=vid)


# ---------------------------------------------------------------------------
# Traducción de cada CSV a asientos
# ---------------------------------------------------------------------------
def _contrapartida_pago(forma):
    forma = (forma or "").lower()
    if forma == "banco":
        return CUENTA_BANCO
    if forma in ("socio_prestamo", "prestamo_socio"):
        return CUENTA_SOCIOS
    if forma in ("socio_aportacion", "aportacion_socio"):
        return CUENTA_APORTACIONES
    return CUENTA_PENDIENTE


def _apertura(cont):
    filas = leer("saldos_apertura.csv")
    lineas = [
        (f["cuenta"], num(f, "saldo_deudor_eur"), num(f, "saldo_acreedor_eur"),
         f"Saldo de apertura: {f['nombre']}", "")
        for f in filas
    ]
    cont.asiento(FECHA_APERTURA, "APE", "Balance 2025 Fisama", lineas)


def _manuales(cont):
    grupos = defaultdict(list)
    for f in leer("asientos_manuales.csv"):
        grupos[f["asiento_ref"]].append(f)
    for ref, filas in grupos.items():
        f0 = filas[0]
        lineas = [
            (f["cuenta"], num(f, "debe_eur"), num(f, "haber_eur"), f["concepto"], f.get("vehiculo_id", ""))
            for f in filas
        ]
        cont.asiento(fecha(f0["fecha"]), "MAN", f"{ref} {f0.get('justificante', '')}".strip(), lineas)


def _aportaciones(cont):
    cuentas = {
        "capital_social": "1000",
        "aportacion_socios": CUENTA_APORTACIONES,
        "aportacion_capital": CUENTA_APORTACIONES,
        "prestamo_socio": CUENTA_SOCIOS,
        "prestamo_socio_largo_plazo": "1630",
    }
    for f in leer("aportaciones_capital.csv"):
        d = fecha(f["fecha"])
        if d is None or d < INICIO_EJERCICIO:
            continue  # ya incluidas en el saldo de apertura
        tipo = f["tipo_aportacion"].lower()
        cuenta = cuentas.get(tipo)
        if cuenta is None:
            cuenta = CUENTA_PENDIENTE
            cont.aviso("ALTA", "Aportaciones",
                       f"Aportación del {d} de {f['socio']} ({eur(num(f, 'importe_eur'))}) sin tipo claro "
                       "(aportación a fondo perdido o préstamo). Se deja en partidas pendientes.")
        destino = CUENTA_BANCO if f["forma"].lower() == "banco" else CUENTA_PENDIENTE
        concepto = f"{f['concepto']} - {f['socio']}"
        cont.asiento(d, "APO", f.get("justificante", ""), [
            (destino, num(f, "importe_eur"), 0, concepto, ""),
            (cuenta, 0, num(f, "importe_eur"), concepto, ""),
        ])


def _compras_vehiculos(cont):
    for v in leer("vehiculos.csv"):
        cont.vehiculos.append(v)
        vid = v["vehiculo_id"]
        precio = num(v, "precio_compra_eur")
        d = fecha(v["fecha_adquisicion"])
        if v["pagado_desde"] == "balance_apertura":
            continue  # entra por el saldo de apertura + reclasificación manual
        if v.get("precio_es_estimado_si_no") == "si":
            cont.aviso("ALTA", f"Vehículo {vid}",
                       f"{v['marca_modelo']}: el precio de compra ({eur(precio)}) es una ESTIMACIÓN "
                       "(valor declarado en aduana). Falta la factura de compra real.")
        if not precio or d is None:
            cont.aviso("ALTA", f"Vehículo {vid}",
                       f"{v['marca_modelo']}: falta precio o fecha de compra; no se ha podido registrar.")
            continue
        contrapartida = _contrapartida_pago(v["pagado_desde"])
        if contrapartida == CUENTA_PENDIENTE:
            cont.aviso("ALTA", f"Vehículo {vid}",
                       f"{v['marca_modelo']} ({eur(precio)}): no sabemos desde dónde se pagó "
                       "(¿BBVA de la empresa? ¿un socio de su bolsillo?). Queda en 'partidas pendientes de aplicación'.")
        concepto = f"Compra {v['marca_modelo']} {v['matricula']} a {v['vendedor']}"
        cont.asiento(max(d, INICIO_EJERCICIO), "COM", v.get("documento_compra", ""), [
            (CUENTA_INMOVILIZADO_VEHICULOS, precio, 0, concepto, vid),
            (contrapartida, 0, precio, concepto, vid),
        ])


def _facturas_recibidas(cont):
    for f in leer("facturas_recibidas.csv"):
        d = fecha(f["fecha_emision"])
        doc = f"{f['num_factura']} {f['proveedor']}"
        vid = f.get("vehiculo_id", "")
        base = num(f, "base_imponible_eur")
        cuota = num(f, "cuota_iva_eur")
        suplidos = num(f, "suplidos_eur")
        retencion = num(f, "retencion_irpf_eur")
        total = round(base + cuota + suplidos - retencion, 2)
        if abs(total - num(f, "total_eur")) > 0.01:
            cont.aviso("MEDIA", "Factura recibida",
                       f"{doc}: base + IVA + suplidos − retención = {eur(total)} pero el total anotado es "
                       f"{eur(num(f, 'total_eur'))}. Revisar.")
        cuenta = f.get("cuenta_pgc") or "6290"
        cuenta_sup = f.get("cuenta_suplidos") or cuenta
        deducible = f.get("iva_deducible_si_no", "si").lower() != "no"
        if d < INICIO_EJERCICIO:
            cont.aviso("MEDIA", "Gasto de 2025 no contabilizado",
                       f"{doc} ({f['concepto']}, {eur(num(f, 'total_eur'))}) es de {d} pero no está en la "
                       "contabilidad 2025 de Fisama: se registra el 01/01/2026.")
            d = INICIO_EJERCICIO
        acreedor = CUENTA_PROVEEDORES if cuenta.startswith(("60", "61")) else CUENTA_ACREEDORES
        concepto = f"{f['concepto']} ({f['proveedor']})"
        lineas = [
            (cuenta, base + (0 if deducible else cuota), 0, concepto, vid),
            (CUENTA_IVA_SOPORTADO, cuota if deducible else 0, 0, f"IVA soportado {doc}", vid),
            (cuenta_sup, suplidos, 0, f"Suplidos: {concepto}", vid),
            (CUENTA_RETENCIONES, 0, retencion, f"Retención IRPF {doc}", vid),
            (acreedor, 0, total, concepto, vid),
        ]
        cont.asiento(d, "FRR", doc, lineas)
        if retencion:
            cont.aviso("MEDIA", "Retenciones IRPF",
                       f"{doc}: Berts retuvo {eur(retencion)} de IRPF al profesional. Hay que ingresarlos en "
                       f"Hacienda con el modelo 111 del {trimestre(d)}. ¿Lo ha presentado Fisama?")
        pagada = f.get("pagada_si_no", "").lower()
        if pagada == "si":
            fp = max(fecha(f["fecha_pago"]) or d, INICIO_EJERCICIO)
            cont.asiento(fp, "PAG", doc, [
                (acreedor, total, 0, f"Pago {doc}", vid),
                (CUENTA_BANCO, 0, total, f"Pago {doc}", vid),
            ])
        else:
            cont.aviso("MEDIA", "Pagos pendientes de confirmar",
                       f"{doc} ({eur(total)}): no sabemos si está pagada. Figura como deuda con el proveedor.")


def _amortizaciones(cont, hasta_por_vehiculo):
    """Amortización lineal por días, un asiento a cada fin de mes (y a la fecha de corte o venta)."""
    for v in cont.vehiculos:
        vid = v["vehiculo_id"]
        inicio = fecha(v.get("fecha_inicio_amortizacion"))
        if not inicio:
            continue
        pct = num(v, "pct_amortizacion_anual") / 100
        inicio = max(inicio, INICIO_EJERCICIO)
        fin = hasta_por_vehiculo.get(vid, cont.corte)
        tramo_inicio = inicio
        while tramo_inicio <= fin:
            tramo_fin = min(fin_de_mes(tramo_inicio), fin)
            dias = (tramo_fin - tramo_inicio).days + 1
            base = cont.coste_vehiculo(vid, tramo_fin)
            ya_amortizado = cont.amortizacion_acumulada(vid, tramo_fin)
            importe = min(round(base * pct * dias / 365, 2), round(base - ya_amortizado, 2))
            concepto = f"Amortización {v['marca_modelo']} {v['matricula']} ({dias} días al {pct:.0%} anual)"
            cont.asiento(tramo_fin, "AMO", f"Amortización {vid} {tramo_fin:%m/%Y}", [
                (CUENTA_DOTACION_AMORT, importe, 0, concepto, vid),
                (CUENTA_AMORT_ACUM_VEHICULOS, 0, importe, concepto, vid),
            ])
            tramo_inicio = tramo_fin + timedelta(days=1)


def _facturas_emitidas(cont):
    ventas = []
    for f in leer("facturas_emitidas.csv"):
        cuenta = f.get("cuenta_pgc") or "7050"
        if cuenta.startswith("218"):
            ventas.append(f)
            continue
        d = fecha(f["fecha_emision"])
        doc = f"Factura {f['num_factura']} {f['cliente']}"
        vid = f.get("vehiculo_id", "")
        base, cuota = num(f, "base_imponible_eur"), num(f, "cuota_iva_eur")
        total = round(base + cuota, 2)
        concepto = f"{f['concepto']} ({f['cliente']})"
        cont.asiento(d, "FRE", doc, [
            (CUENTA_CLIENTES, total, 0, concepto, vid),
            (cuenta, 0, base, concepto, vid),
            (CUENTA_IVA_REPERCUTIDO, 0, cuota, f"IVA repercutido {doc}", vid),
        ])
        if not vid:
            cont.aviso("BAJA", "Factura emitida",
                       f"{doc}: no sabemos a qué vehículo corresponde (afecta solo a la rentabilidad por vehículo).")
        _cobro(cont, f, d, doc, total, vid)
    return ventas


def _cobro(cont, f, d, doc, total, vid):
    if f.get("cobrada_si_no", "").lower() == "si":
        fc = fecha(f["fecha_cobro"]) or d
        cont.asiento(fc, "COB", doc, [
            (CUENTA_BANCO, total, 0, f"Cobro {doc}", vid),
            (CUENTA_CLIENTES, 0, total, f"Cobro {doc}", vid),
        ])
    else:
        cont.aviso("ALTA", "Cobros pendientes de confirmar",
                   f"{doc} ({eur(total)}): no sabemos si se ha cobrado. Figura como deuda del cliente.")


def _ventas_inmovilizado(cont, ventas):
    for f in ventas:
        d = fecha(f["fecha_emision"])
        vid = f.get("vehiculo_id", "")
        doc = f"Factura {f['num_factura']} {f['cliente']}"
        base, cuota = num(f, "base_imponible_eur"), num(f, "cuota_iva_eur")
        total = round(base + cuota, 2)
        coste = cont.coste_vehiculo(vid, d)
        amort = cont.amortizacion_acumulada(vid, d)
        resultado = round(base - (coste - amort), 2)
        concepto = f"Venta {f['concepto']} ({f['cliente']})"
        lineas = [
            (CUENTA_CLIENTES, total, 0, concepto, vid),
            (CUENTA_AMORT_ACUM_VEHICULOS, amort, 0, f"Baja amortización acumulada {vid}", vid),
            (CUENTA_INMOVILIZADO_VEHICULOS, 0, coste, f"Baja del activo {vid}", vid),
            (CUENTA_IVA_REPERCUTIDO, 0, cuota, f"IVA repercutido {doc}", vid),
        ]
        if resultado < 0:
            lineas.append((CUENTA_PERDIDA_INMOVILIZADO, -resultado, 0, f"Pérdida en la venta de {vid}", vid))
        else:
            lineas.append((CUENTA_BENEFICIO_INMOVILIZADO, 0, resultado, f"Beneficio en la venta de {vid}", vid))
        cont.asiento(d, "VTA", doc, lineas)
        cont.ventas_inmovilizado.append(
            {"vehiculo": vid, "fecha": d, "precio": base, "coste": coste, "amortizacion": amort,
             "resultado": resultado}
        )
        _cobro(cont, f, d, doc, total, vid)


def _liquidaciones_iva(cont):
    """Al cierre de cada trimestre ya terminado se cancela el IVA soportado y repercutido contra
    'IVA a ingresar' (4750) o 'IVA a compensar' (4700), incluyendo lo pendiente de compensar."""
    anio = INICIO_EJERCICIO.year
    t = 1
    while True:
        fin_t = fin_de_trimestre(anio, t)
        if fin_t > cont.corte:
            break
        repercutido = -cont.saldo(CUENTA_IVA_REPERCUTIDO, hasta=fin_t)
        soportado = cont.saldo(CUENTA_IVA_SOPORTADO, hasta=fin_t)
        a_compensar_previo = cont.saldo(CUENTA_IVA_A_COMPENSAR, hasta=fin_t)
        resultado = round(repercutido - soportado - a_compensar_previo, 2)
        etiqueta = f"{anio}-T{t}"
        lineas = [
            (CUENTA_IVA_REPERCUTIDO, repercutido, 0, f"Liquidación IVA {etiqueta}", ""),
            (CUENTA_IVA_SOPORTADO, 0, soportado, f"Liquidación IVA {etiqueta}", ""),
            (CUENTA_IVA_A_COMPENSAR, 0, a_compensar_previo, f"Compensación de cuotas anteriores {etiqueta}", ""),
        ]
        if resultado >= 0:
            lineas.append((CUENTA_IVA_A_PAGAR, 0, resultado, f"IVA a ingresar {etiqueta} (modelo 303)", ""))
        else:
            lineas.append((CUENTA_IVA_A_COMPENSAR, -resultado, 0, f"IVA a compensar {etiqueta} (modelo 303)", ""))
        cont.asiento(fin_t, "IVA", f"Modelo 303 {etiqueta}", lineas)
        cont.liquidaciones_iva.append({
            "trimestre": etiqueta, "repercutido": repercutido, "soportado": soportado,
            "compensado": a_compensar_previo, "resultado": resultado,
        })
        if resultado > 0:
            cont.aviso("MEDIA", "IVA",
                       f"Modelo 303 {etiqueta}: salen {eur(resultado)} a ingresar. Cuando nos confirméis el pago "
                       "(extracto o justificante) se registra y desaparece del pasivo.")
        t += 1
        if t > 4:
            anio, t = anio + 1, 1


def _cierres(cont):
    """Regularización de gastos e ingresos (grupos 6 y 7) contra la cuenta 129 al cierre de
    cada ejercicio ya terminado antes de la fecha de corte."""
    for anio in range(INICIO_EJERCICIO.year, cont.corte.year):
        cierre = date(anio, 12, 31)
        saldos = defaultdict(float)
        for a in cont.apuntes:
            if a.fecha.year == anio and a.cuenta[:1] in ("6", "7"):
                saldos[a.cuenta] += a.saldo
        lineas = []
        for cuenta, s in sorted(saldos.items()):
            s = round(s, 2)
            if s:
                lineas.append((cuenta, max(0, -s), max(0, s), f"Regularización {anio}", ""))
        resultado = -round(sum(saldos.values()), 2)
        lineas.append((CUENTA_RESULTADO, max(0, -resultado), max(0, resultado), f"Resultado {anio}", ""))
        cont.asiento(cierre, "REG", f"Cierre {anio}", lineas)
        cont.aviso("ALTA", "Cierre del ejercicio",
                   f"Resultado {anio}: {eur(resultado)}. Falta anotar en asientos_manuales.csv cómo se aplica "
                   "(reservas, remanente o resultados negativos) según lo que apruebe la Junta.")


def _controles(cont):
    for f in leer("saldos_banco_reales.csv"):
        d = fecha(f["fecha"])
        if not d or d > cont.corte:
            continue
        contable = cont.saldo(f.get("cuenta") or CUENTA_BANCO, hasta=d)
        real = num(f, "saldo_real_eur")
        if abs(contable - real) > 0.01:
            cont.aviso("ALTA", "Cuadre bancario",
                       f"A {d}: el banco según contabilidad es {eur(contable)} y según el extracto "
                       f"{eur(real)} (diferencia {eur(contable - real)}). Hay movimientos sin registrar.")
    pendiente = cont.saldo(CUENTA_PENDIENTE, hasta=cont.corte)
    if pendiente:
        cont.aviso("ALTA", "Partidas pendientes de aplicación",
                   f"Hay {eur(abs(pendiente))} en la cuenta 555: pagos cuyo origen no sabemos (sobre todo compras de "
                   "vehículos). Con los extractos del BBVA se reparten entre banco, deuda con socios o aportación.")
    if not any(fecha(f["fecha"]) and fecha(f["fecha"]) >= INICIO_EJERCICIO
               for f in leer("saldos_banco_reales.csv")):
        cont.aviso("ALTA", "Cuadre bancario",
                   "No tenemos ningún saldo real del BBVA de 2026. Sin extractos no se puede comprobar que la "
                   "tesorería del balance sea la real.")


def construir(corte):
    """Construye la contabilidad completa hasta la fecha de corte."""
    cont = Contabilidad(corte)
    _apertura(cont)
    _manuales(cont)
    _aportaciones(cont)
    _compras_vehiculos(cont)
    _facturas_recibidas(cont)
    ventas = _facturas_emitidas(cont)
    fechas_venta = {f.get("vehiculo_id"): fecha(f["fecha_emision"]) for f in ventas}
    _amortizaciones(cont, fechas_venta)
    _ventas_inmovilizado(cont, ventas)
    _liquidaciones_iva(cont)
    _cierres(cont)
    _controles(cont)
    cont.numerar()

    debe = round(sum(a.debe for a in cont.apuntes), 2)
    haber = round(sum(a.haber for a in cont.apuntes), 2)
    if abs(debe - haber) > 0.01:
        raise ValueError(f"El diario no cuadra: debe {debe} ≠ haber {haber}")
    sin_linea = sorted({a.cuenta for a in cont.apuntes if not linea_balance(a.cuenta)})
    if sin_linea:
        raise ValueError(f"Cuentas sin línea de balance asignada: {sin_linea}")
    orden = {"ALTA": 0, "MEDIA": 1, "BAJA": 2}
    cont.avisos.sort(key=lambda a: (orden[a.prioridad], a.tema))
    return cont
