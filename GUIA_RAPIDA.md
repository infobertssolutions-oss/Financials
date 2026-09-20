# Guía rápida: qué meto, dónde, y para qué

Solo hay **4 sitios** donde metéis información. El resto (informes, cuentas, IVA por trimestre) se calcula solo. Esta guía es el único documento que necesitáis tener a mano en el día a día.

---

## 1. Te llega una factura de un proveedor (gasto) → `datos/facturas_recibidas.csv`

Ejemplos: el seguro de una furgoneta, el taller, la gestoría, gasolina, alquiler de una nave...

**Pasos:**
1. Guarda el PDF o haz una foto legible de la factura.
2. Ponle este nombre: `AAAA-MM-DD_numerofactura_proveedor.pdf` (ej: `2026-03-02_F-045_Talleres-Perez.pdf`).
3. Guárdala en `facturas/recibidas/2026/` (la carpeta del año que corresponda; si no existe el año, se crea).
4. Abre `datos/facturas_recibidas.csv` con Excel/Google Sheets y añade una fila nueva con los datos de esa factura (fecha, proveedor, importe, IVA, etc.). En la columna `archivo_pdf` pon la ruta del archivo que acabas de guardar. Si es un gasto de un vehículo concreto, pon su `vehiculo_id` (V1, V2, V3, V4); si no, déjalo en blanco.

Ya está. Esa factura ya cuenta en gastos, en el IVA soportado del trimestre, y (si tiene `vehiculo_id`) en la rentabilidad de ese vehículo.

## 2. Emitís una factura a un cliente (ingreso) → `datos/facturas_emitidas.csv`

Ejemplos: el alquiler mensual de una furgoneta, un servicio facturado a una empresa.

**Pasos:** igual que arriba pero en la carpeta `facturas/emitidas/2026/` y en el fichero `datos/facturas_emitidas.csv`.

## 3. Roberto o tú metéis dinero en la empresa → `datos/aportaciones_capital.csv`

Cada vez que uno de los dos socios transfiere dinero a la cuenta de Berts (o aporta un bien, como pagar directamente la importación de un vehículo):

1. Añade una fila: fecha, quién (Roberto o tú), importe, y **tipo**: ¿es `aportacion_capital` (se queda en la empresa) o `prestamo_socio` (la empresa te lo debe devolver)? Si no lo sabéis, dejadlo anotado en "notas" y lo revisamos con la gestoría — es importante no confundirlo.
2. Guarda el justificante de la transferencia donde guardéis los documentos societarios (de momento puede ser junto a la factura relacionada, si la hay).

## 4. Compráis, importáis o vendéis un vehículo → `datos/inversiones_vehiculos.csv`

Esto se toca pocas veces (solo cuando entra o sale un vehículo de la flota). Una fila por vehículo, con el desglose: coste de compra, aduana/importación, matriculación/impuestos, transporte, quién lo pagó.

---

## Lo que NO tenéis que tocar nunca a mano

- **`/informes/`** — se genera solo. Nunca escribáis ahí directamente.

## Cómo ver "cómo vamos" por trimestre y por mes

Cada vez que queráis ver el estado de las cuentas (o pedídselo a Claude directamente: "genera los informes"):

```bash
cd scripts
python3 generar_informes.py
```

Esto actualiza automáticamente, a partir de todo lo que hayáis metido:

- **`informes/cuenta_resultados.md`** — ingresos, gastos y beneficio, agrupado por línea de negocio, **por trimestre y por mes**.
- **`informes/iva.md`** — IVA repercutido vs soportado **por trimestre** (así lo contrastáis fácilmente con lo que la gestoría presenta en el modelo 303 cada trimestre).
- **`informes/rentabilidad_vehiculos.md`** — cuánto gana o pierde cada vehículo, y qué % de lo invertido lleváis recuperado.
- **`informes/balance_resumen.md`** — cuánto ha aportado cada socio y cuánto tenéis invertido en vehículos.

No hace falta que sepáis nada de contabilidad para leerlos: son tablas con euros, listas de leer de arriba a abajo.

## Rutina recomendada

- **Cada vez que pase algo** (llega/emitís una factura, entra dinero): metedlo en el momento, 2 minutos. Es lo que evita que se pierda o se acumule.
- **Una vez al mes**: ejecutad los informes y echadle un vistazo rápido a `cuenta_resultados.md`.
- **Cada trimestre** (antes de que la gestoría presente el IVA): revisad `iva.md` y comparadlo con lo que va a declarar Fisama. Si no coincide, es la señal de que falta meter alguna factura (vuestra o de ellos).

## Regla de oro

**Todo lo que pase con dinero de la empresa se anota el mismo día que ocurre.** Es la única forma de que dentro de 6 meses no tengáis que reconstruir nada de memoria ni depender solo de lo que os diga la gestoría.
