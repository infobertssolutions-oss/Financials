# Finanzas de Berts Solutions SL

Sistema para que Roberto y tú llevéis vosotros mismos el control financiero de la empresa (50% / 50%), sin depender solo de la gestoría.

**👉 Empieza por [`GUIA_RAPIDA.md`](GUIA_RAPIDA.md) — ahí está explicado paso a paso qué meter, dónde, y cómo ver las cuentas por trimestre y mes.**

## Filosofía del sistema

- **Sencillo**: todo son hojas de cálculo (`.csv`, se abren con Excel o Google Sheets) más una carpeta donde se guardan los PDF/fotos de las facturas.
- **Nada se pierde**: al estar en Git, cada cambio queda guardado con fecha para siempre, y las facturas se guardan como documento real, no solo como un dato.
- **Trazable**: cada factura, aportación o inversión queda registrada de forma individual, para poder contrastar en cualquier momento lo que dice la gestoría contra lo que tenemos nosotros.
- **Informes automáticos**: nada se calcula a mano. Un script lee todo lo que hayáis metido y genera cuenta de resultados, IVA y rentabilidad, agrupados por trimestre y por mes.

## Estructura del proyecto

```
GUIA_RAPIDA.md                ← EMPEZAR AQUÍ: qué meter, dónde y cuándo
PENDIENTE.md                  ← Lo que necesitamos que nos facilitéis para tener datos reales
ASESORIA_INICIAL.md           ← Primeras recomendaciones y riesgos a revisar

/datos/                       ← Las hojas de cálculo donde se anota todo
    facturas_emitidas.csv     ← Facturas que emite Berts (ingresos)
    facturas_recibidas.csv    ← Facturas que recibe Berts (proveedores, seguros, combustible...)
    aportaciones_capital.csv  ← Dinero o bienes que habéis metido Roberto y tú
    inversiones_vehiculos.csv ← Ficha de cada vehículo: coste, importación, matriculación

/facturas/                    ← Aquí se guarda el PDF/foto real de cada factura
    emitidas/2026/
    recibidas/2026/

/lineas_negocio/               ← Notas y seguimiento de cada línea de negocio
    01_alquiler_vehiculos/
    02_servicios_empresas/

/informes/                     ← Se genera solo — nunca se edita a mano
/scripts/generar_informes.py   ← El script que lee /datos/ y crea los informes
```

## Próximo paso

Lee **[`PENDIENTE.md`](PENDIENTE.md)**: ahí está todo lo que necesitamos que nos vayáis pasando para sustituir las plantillas por vuestros datos reales.
