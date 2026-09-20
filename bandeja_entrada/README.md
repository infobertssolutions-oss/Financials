# Bandeja de entrada

Esta carpeta es el "cajón desastre" a propósito: aquí soltáis cualquier documento **sin preocuparos de nombrarlo bien ni de clasificarlo**. Yo (Claude) lo reviso, lo llevo a su sitio en `/facturas/`, `/datos/`, etc., y luego lo borro de aquí.

## Qué podéis meter

Cualquier cosa que tenga que ver con dinero de la empresa: fotos de facturas, PDFs, extractos bancarios, capturas de Excel de la gestoría, cuentas anuales, contratos de alquiler, justificantes de transferencias de aportaciones de capital... Cualquier formato sirve (foto, PDF, Excel, captura de pantalla).

## Cómo se sube

**Opción A — Directamente en esta conversación (la más cómoda):**
Adjunta aquí el archivo o la foto tal cual, como harías por WhatsApp, y dime brevemente qué es ("esto es el seguro de la furgoneta de enero" o "esto es lo que aportó Roberto en marzo"). Yo lo guardo en el sitio correcto, lo doy de alta en el CSV que toque, actualizo los informes, y hago commit y push. No hace falta que hagas nada más.

**Opción B — Subida directa al repositorio (para cuando no estamos hablando):**
Si Roberto o tú queréis dejar documentos sueltos para que los procese en otro momento, podéis subirlos directamente a esta carpeta desde la web de GitHub (arrastrando el archivo a `bandeja_entrada/` y dando a "Commit changes"). La próxima vez que retome el proyecto, reviso todo lo que haya aquí, lo ordeno y os aviso de lo que he entendido y de lo que me falta por aclarar.

## Qué hago yo con ello

1. Identifico de qué se trata (factura emitida, factura recibida, aportación, dato de un vehículo...).
2. Lo guardo con el nombre y en la carpeta correctos dentro de `/facturas/`.
3. Añado la fila correspondiente en el CSV de `/datos/` que toque.
4. Si algo no me queda claro (falta un dato, no sé a qué vehículo corresponde, no sé si es aportación o préstamo), te pregunto en vez de adivinarlo.
5. Regenero los informes y confirmo qué he metido.

## Cómo organizar el volcado si tenéis mucho acumulado

No hace falta mandarlo todo de golpe. Lo más práctico, siguiendo el orden de `PENDIENTE.md`, es ir por tandas:

1. Primero: datos societarios básicos (CIF, capital social, si el 50/50 está en escritura).
2. Después: lo de los 4 vehículos (compra, importación, matriculación de cada uno).
3. Después: últimas facturas de los alquileres de los 9 meses.
4. Después: aportaciones de capital de cada socio.
5. Por último: lo que tengáis de Fisama (cuentas anuales, modelos 303 presentados) para contrastarlo con lo que vayamos montando.

Pero si preferís mandarlo todo mezclado y que yo lo vaya ordenando, también funciona — para eso está esta carpeta.
