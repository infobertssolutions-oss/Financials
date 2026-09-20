# Línea 1: Alquiler de furgonetas y vehículos

## Situación actual (según lo que nos habéis contado)

- Inversión acumulada en vehículos: **+80.000 €**.
- Flota comprada/importada: **2 furgonetas + 2 Ford Mustang importados de Dubai**.
- Actualmente **en alquiler activo: 2 vehículos** (antes eran 4; se redujo a 2 para liberar capital y pagar gastos de importación de los Mustang).
- Llevan **+9 meses** de alquiler mensual recurrente.

Esto ya nos dice varias cosas importantes a vigilar:

1. **Los 2 vehículos parados no generan ingresos pero sí pueden seguir generando gastos** (seguro, impuestos de circulación, depreciación, posible financiación). Hay que saber si están parados a propósito (a la espera de alquilarlos) o si conviene venderlos.
2. **Los Mustang son vehículos de alta cilindrada** → en España tributan un tipo alto del Impuesto de Matriculación (IEDMT), pueden tener seguros más caros y consumos elevados, lo que afecta a la rentabilidad neta del alquiler. Conviene calcular la rentabilidad de cada vehículo por separado, no en conjunto, porque furgonetas y Mustang tienen estructuras de coste muy distintas.
3. **Un vehículo importado y puesto en alquiler por una empresa suele permitir deducir el 100% del IVA soportado** (a diferencia del 50% habitual para vehículos de uso mixto) — pero solo si se puede acreditar que el vehículo se destina exclusivamente a la actividad de alquiler. Hay que revisar con la gestoría/asesor fiscal si esto se está aplicando correctamente.

## Qué se registra aquí

- `datos/inversiones_vehiculos.csv`: ficha de cada vehículo (coste, importación, matriculación, quién lo pagó). Se toca solo cuando se compra/importa/vende un vehículo.
- `datos/facturas_emitidas.csv` / `facturas_recibidas.csv`: cada factura de esta línea, con `linea_negocio = alquiler_vehiculos` y el `vehiculo_id` correspondiente (V1, V2, V3, V4...). No hace falta ningún fichero aparte: la rentabilidad de cada vehículo se calcula automáticamente sumando sus facturas.

## Preguntas clave que iremos respondiendo con los datos reales

- ¿Cuánto tiempo se tarda en recuperar la inversión de cada vehículo (payback)?
- ¿Qué vehículo es más rentable por euro invertido: furgonetas o Mustang?
- ¿Compensa mantener parados los 2 vehículos no alquilados, o es mejor venderlos y reinvertir/reducir deuda?
- ¿El precio de alquiler cubre amortización + seguro + mantenimiento + margen, o solo cubre gastos corrientes?

Estas respuestas saldrán automáticamente en `/informes/rentabilidad_vehiculos.md` en cuanto metáis los datos reales.
