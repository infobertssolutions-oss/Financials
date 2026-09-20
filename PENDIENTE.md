# Qué necesitamos que nos facilitéis

Este sistema ya tiene la estructura lista, pero está vacío/con ejemplos de plantilla. Para que empiece a reflejar la realidad de Berts Solutions y sea útil desde ya, necesitamos que nos paséis lo siguiente. No hace falta todo de golpe: id mandando lo que tengáis a mano y lo vamos incorporando.

## 1. Datos societarios básicos

- [ ] CIF de Berts Solutions SL, fecha de constitución, capital social escriturado.
- [ ] Confirmación: ¿el 50%/50% está reflejado en escritura/libro de socios, o solo es un acuerdo verbal entre Roberto y tú? (importante para las aportaciones de capital, ver `ASESORIA_INICIAL.md`).
- [ ] Domicilio fiscal, epígrafes de IAE dados de alta (¿alquiler de vehículos sin conductor? ¿servicios a empresas, cuáles?).
- [ ] Régimen de IVA (general) y de Impuesto de Sociedades. ¿Estáis en algún régimen especial?

## 2. Datos de la gestoría (Fisama)

- [ ] Últimas cuentas anuales presentadas (Balance + Cuenta de Pérdidas y Ganancias) de los últimos 1-2 ejercicios, si existen.
- [ ] Últimos modelos 303 (IVA trimestral) presentados.
- [ ] Último modelo 200 (Impuesto de Sociedades) si ya se ha presentado alguno.
- [ ] Libro registro de facturas emitidas y recibidas que tenga la gestoría (para contrastar contra lo que vayamos metiendo aquí).
- [ ] Extracto bancario de la cuenta de la empresa (al menos los últimos 6-12 meses) para poder cuadrar ingresos y gastos reales.

## 3. Vehículos (los +80k€ invertidos)

Para cada uno de los 4 vehículos (2 furgonetas + 2 Mustang importados de Dubai), aunque ahora solo 2 estén en alquiler:

- [ ] Marca, modelo, matrícula (o nº de bastidor si aún no está matriculado).
- [ ] Fecha de compra/importación.
- [ ] Coste de compra (precio pagado en origen).
- [ ] Gastos de importación y aduana (aranceles, IVA de importación, transporte internacional, agente de aduanas).
- [ ] Gastos de matriculación en España: Impuesto Especial sobre Determinados Medios de Transporte ("impuesto de matriculación"), ITV, homologación/ficha reducida, tasas de tráfico.
- [ ] Quién lo pagó y con qué dinero: ¿aportación de Roberto, aportación tuya, cuenta de la empresa, préstamo/financiación? (esto es clave para `aportaciones_capital.csv`).
- [ ] Estado actual: en alquiler / parado / en venta / vendido.
- [ ] Para los 2 vehículos que ya NO se alquilan: ¿qué se hizo con ellos? ¿se vendieron, están guardados, se usan para otra cosa?

## 4. Negocio de alquiler de vehículos (línea 1)

- [ ] Para los 9+ meses de alquiler: listado de lo cobrado cada mes por cada vehículo (aunque sea aproximado al principio).
- [ ] Contratos de alquiler o acuerdo con quien alquila (¿empresas, particulares, plataformas tipo renting/carsharing?).
- [ ] Gastos recurrentes por vehículo: seguro, mantenimiento, financiación/leasing (si hay cuota mensual), gestoría de multas, limpieza, etc.
- [ ] Facturas emitidas por estos alquileres (para meter en `facturas_emitidas.csv`).

## 5. Negocio de servicios para empresas (línea 2)

- [ ] Qué tipo de servicio(s) concretos se van a ofrecer u ofrecen ya.
- [ ] Si ya hay clientes o facturación: listado de facturas emitidas y clientes.
- [ ] Estructura de costes prevista (¿subcontratáis, tenéis personal, es solo vosotros dos?).

## 6. Aportaciones de capital y gastos de importación

- [ ] Detalle de cuánto ha puesto cada socio (Roberto y tú) desde el inicio, con fechas.
- [ ] Si alguna aportación fue en forma de préstamo del socio a la empresa (que se debe devolver) en vez de aportación a fondo perdido o ampliación de capital — esto cambia mucho el tratamiento fiscal y contable.
- [ ] Justificantes de transferencias bancarias de estas aportaciones.

## 7. Otros

- [ ] ¿Hay empleados o solo trabajáis los dos socios?
- [ ] ¿Hay algún préstamo bancario o financiación externa (leasing, renting, préstamo ICO, etc.) además de las aportaciones de los socios?
- [ ] Facturas de gastos generales: alquiler de local/nave si hay, gestoría, seguros, suministros, etc.

---

**Cómo mandarlo**: puede ser en el formato que tengáis (Excel, PDF, fotos de facturas, extractos bancarios). Nosotros lo iremos volcando a los CSV de `/datos/` con el formato correcto. Si preferís, también podéis rellenar directamente los CSV vosotros mismos siguiendo las columnas que ya están creadas como plantilla — cuantos más datos reales metáis, antes podremos generar informes fiables y detectar si algo no cuadra con la gestoría.
