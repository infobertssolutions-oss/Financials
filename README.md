# Finanzas de Berts Solutions SL

Sistema para que Roberto y tú llevéis vosotros mismos el control financiero de la empresa (50% / 50%), sin depender solo de la gestoría.

**👉 Empieza por [`GUIA_RAPIDA.md`](GUIA_RAPIDA.md) — ahí está explicado paso a paso qué meter, dónde, y cómo ver las cuentas por trimestre y mes.**

**📊 Balance de Situación y Cuenta de Pérdidas y Ganancias:** [`informes/Estados_Financieros_Berts.xlsx`](informes/Estados_Financieros_Berts.xlsx). Cómo está organizado y qué criterios se aplican: [`ESTADOS_FINANCIEROS.md`](ESTADOS_FINANCIEROS.md).

**¿Solo quieres pasar información sin complicarte?** Adjunta fotos/PDFs/Excel directamente en la conversación, o súbelos a [`bandeja_entrada/`](bandeja_entrada/README.md) — Claude se encarga de clasificarlo y ordenarlo todo.

## Filosofía del sistema

- **Sencillo**: todo son hojas de cálculo (`.csv`, se abren con Excel o Google Sheets) más una carpeta donde se guardan los PDF/fotos de las facturas.
- **Nada se pierde**: al estar en Git, cada cambio queda guardado con fecha para siempre, y las facturas se guardan como documento real, no solo como un dato.
- **Trazable**: cada factura, aportación o inversión queda registrada de forma individual, para poder contrastar en cualquier momento lo que dice la gestoría contra lo que tenemos nosotros.
- **Informes automáticos**: nada se calcula a mano. Un script convierte cada dato en su asiento contable (PGC Pymes) y genera el balance de situación, la cuenta de pérdidas y ganancias, el IVA por trimestre y la rentabilidad de cada vehículo.

## Estructura del proyecto

```
GUIA_RAPIDA.md                ← EMPEZAR AQUÍ: qué meter, dónde y cuándo
ESTADOS_FINANCIEROS.md        ← Cómo se construyen el balance y la PyG, y criterios contables
PENDIENTE.md                  ← Lo que necesitamos que nos facilitéis para tener datos reales
ASESORIA_INICIAL.md           ← Primeras recomendaciones y riesgos a revisar

/bandeja_entrada/              ← Sube aquí cualquier documento sin clasificar; Claude lo ordena

/datos/                       ← Las hojas de cálculo donde se anota todo
    facturas_emitidas.csv     ← Facturas que emite Berts (ingresos)
    facturas_recibidas.csv    ← Facturas que recibe Berts (proveedores, seguros, combustible...)
    aportaciones_capital.csv  ← Dinero o bienes que habéis metido Roberto y tú
    vehiculos.csv             ← Ficha de cada vehículo: precio, cómo se pagó, amortización
    saldos_apertura.csv       ← Balance de Fisama a 31/12/2025 (punto de partida)
    asientos_manuales.csv     ← Lo que no encaja en lo anterior
    saldos_banco_reales.csv   ← Saldos del extracto del BBVA, para comprobar que el banco cuadra

/facturas/                    ← Aquí se guarda el PDF/foto real de cada factura
    emitidas/2026/
    recibidas/2026/

/lineas_negocio/               ← Notas y seguimiento de cada línea de negocio
    01_alquiler_vehiculos/
    02_servicios_empresas/

/informes/                     ← Se genera solo — nunca se edita a mano
    Estados_Financieros_Berts.xlsx ← Balance, PyG, IVA, vehículos, libro diario
/scripts/contabilidad.py       ← Motor contable: convierte cada dato en su asiento
/scripts/generar_informes.py   ← Genera el Excel y los informes en texto
```

## Próximo paso

Lee **[`PENDIENTE.md`](PENDIENTE.md)**: ahí está todo lo que necesitamos que nos vayáis pasando para sustituir las plantillas por vuestros datos reales.
