# Finanzas de Berts Solutions SL

Este repositorio es el **sistema central de gestión financiera** de Berts Solutions SL, controlado directamente por los socios (50% / 50%), sin depender de que la gestoría sea la única que tenga la información.

## Filosofía del sistema

- **Sencillo**: todo son hojas de cálculo (`.csv`) que se pueden abrir con Excel, Google Sheets o Numbers. No hace falta saber programar ni de finanzas para rellenarlas.
- **Nada se pierde**: al estar en Git, cada cambio queda guardado con fecha y autor para siempre. Si alguien borra o modifica algo por error, se puede recuperar.
- **Trazable**: cada factura, aportación o inversión queda registrada de forma individual, para poder auditar en cualquier momento lo que dice la gestoría contra lo que tenemos nosotros.
- **Con informes automáticos**: a partir de los datos que vayáis metiendo, un script genera cuenta de resultados, IVA, y rentabilidad por línea de negocio y por vehículo.

## Estructura del proyecto

```
/datos/                      ← AQUÍ SE METE TODA LA INFORMACIÓN (lo único que tenéis que tocar el día a día)
    facturas_emitidas.csv    ← Facturas que emite Berts (ingresos)
    facturas_recibidas.csv   ← Facturas/gastos que recibe Berts (proveedores, seguros, combustible...)
    aportaciones_capital.csv ← Dinero o bienes que habéis metido Roberto y tú en la empresa
    inversiones_vehiculos.csv← Detalle de cada vehículo: coste, importación, matriculación, quién lo pagó
    alquileres_vehiculos.csv ← Seguimiento mes a mes de cada vehículo en alquiler (ingresos y gastos asociados)

/lineas_negocio/              ← Explicación y seguimiento específico de cada línea de negocio
    01_alquiler_vehiculos/
    02_servicios_empresas/

/informes/                    ← Aquí se generan automáticamente los informes (no se edita a mano)

/scripts/
    generar_informes.py       ← Script que lee /datos/ y genera los informes

PENDIENTE.md                  ← Lista de lo que necesitamos que nos facilitéis para completar el cuadro
ASESORIA_INICIAL.md           ← Primeras recomendaciones, riesgos detectados y puntos a revisar con un experto
```

## Cómo se usa (rutina mensual recomendada)

1. Cada vez que emitáis o recibáis una factura, se añade una fila en `datos/facturas_emitidas.csv` o `datos/facturas_recibidas.csv`.
2. Cada vez que uno de los dos socios mete dinero (o un bien, como un vehículo) en la empresa, se añade una fila en `datos/aportaciones_capital.csv`.
3. Una vez al mes, se actualiza `datos/alquileres_vehiculos.csv` con lo cobrado y gastado por cada furgoneta/Mustang.
4. Se ejecuta el script de informes (o se le pide a Claude que lo haga) y se revisan los resultados en `/informes/`.
5. A final de mes/trimestre, se compara lo que dice este sistema con lo que reporta Fisama (la gestoría), para detectar cualquier discrepancia.

## Cómo generar los informes

```bash
cd scripts
python3 generar_informes.py
```

Esto genera en `/informes/`:
- `cuenta_resultados.md` — ingresos, gastos y beneficio, por línea de negocio y por mes.
- `iva.md` — IVA repercutido vs soportado (orientativo, para contrastar con el modelo 303 que presente la gestoría).
- `rentabilidad_vehiculos.md` — qué gana o pierde cada vehículo en alquiler.
- `balance_resumen.md` — resumen de lo invertido, aportado por cada socio, y situación patrimonial simplificada.

## Próximo paso

Lee **`PENDIENTE.md`**: ahí está todo lo que necesitamos que nos vayáis pasando (datos, documentos, cifras) para dejar esto funcionando de verdad con vuestra información real, y no con plantillas vacías.
