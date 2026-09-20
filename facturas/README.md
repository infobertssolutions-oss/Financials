# Facturas (los documentos, no solo el dato)

Aquí se guarda el **PDF o foto de cada factura real**. La fila en `datos/facturas_emitidas.csv` o `datos/facturas_recibidas.csv` es el "resumen" para calcular cifras; este archivo es la prueba/justificante, por si Hacienda o la gestoría lo piden algún día.

## Estructura

```
facturas/
  emitidas/AAAA/    ← facturas que hace Berts a sus clientes (dinero que entra)
  recibidas/AAAA/   ← facturas que Berts recibe de proveedores (dinero que sale)
```

Una carpeta por año. Dentro, todos los archivos de ese año juntos — no hace falta crear subcarpetas por mes o trimestre, porque los informes ya agrupan automáticamente por trimestre y mes usando la fecha que pongas en el CSV.

## Cómo nombrar cada archivo

```
AAAA-MM-DD_numerofactura_nombrecliente-o-proveedor.pdf
```

Ejemplo: `2026-02-10_F-002_Cliente-Real-SL.pdf`

Así, sin abrir el archivo, ya sabes de cuándo es y a quién corresponde, y coincide con lo que pones en la columna `archivo_pdf` del CSV — eso es lo que enlaza la fila de datos con el documento real.

## Regla de oro

**No hay factura sin las dos cosas**: el archivo aquí + la fila en el CSV correspondiente. Si solo guardas el PDF, no cuenta para los informes. Si solo metes la fila y no guardas el documento, no tienes justificante si te lo piden. Los dos pasos van siempre juntos (ver `GUIA_RAPIDA.md` en la raíz del proyecto).
