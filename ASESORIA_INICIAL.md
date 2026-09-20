# Asesoría inicial: riesgos, recomendaciones y puntos a revisar

Esto es una primera lectura basada en lo que nos habéis contado, **no sustituye el consejo de un asesor fiscal/laboral colegiado**, especialmente en decisiones que impliquen presentar declaraciones. El objetivo es que sepáis qué preguntar (también a Fisama) y qué vigilar vosotros mismos.

## 1. Aportaciones de capital: formalizarlas bien es prioritario

Si Roberto y tú habéis puesto dinero (o vehículos) en la empresa sin dejarlo bien documentado, es el riesgo nº1 ahora mismo:

- **Aportación a fondo perdido / ampliación de capital** vs **préstamo de socio**: son fiscalmente muy distintos. Un préstamo de socio genera una deuda de la empresa hacia el socio (se puede devolver sin tributar, pero necesita contrato de préstamo con intereses a mercado o justificar que es sin interés). Una aportación a capital aumenta el capital social (requiere escritura/registro) o puede ir a una cuenta de "aportaciones de socios para compensar pérdidas".
- **Sin papel de por medio, Hacienda puede considerar estas entradas de dinero como ingresos no justificados de la sociedad**, con el riesgo de que tributen como si fueran beneficio.
- **Acción recomendada**: revisar con Fisama (o un segundo asesor) cómo se ha contabilizado cada aportación hasta ahora, y a partir de ahora documentar cada una en `datos/aportaciones_capital.csv` + guardar el justificante bancario.

## 2. Vehículos importados de Dubai: fiscalidad de importación

Importar vehículos de fuera de la UE implica varios impuestos que hay que verificar que se han liquidado correctamente:

- **IVA a la importación** (se paga en aduana al entrar el vehículo).
- **Aranceles de aduana**, según el origen y tipo de vehículo.
- **Impuesto Especial sobre Determinados Medios de Transporte (IEDMT / "impuesto de matriculación")**: depende de las emisiones de CO₂. Un Mustang (motor grande, alto consumo) puede caer en el tramo más alto (hasta el 14,75% del valor del vehículo). Esto puede ser una parte muy significativa de esos +80.000 € invertidos.
- **Homologación/ficha reducida** para poder matricular en España un vehículo que no viene de fábrica homologado para la UE.

**Pregunta clave para la gestoría**: ¿estos importes se dedujeron/liquidaron a través de la empresa, y se puede acreditar documentalmente cada pago? Si falta algún justificante, es mejor detectarlo ahora que en una inspección.

## 3. IVA de los vehículos en alquiler

- Como norma general, el IVA de un vehículo de uso mixto solo se puede deducir al 50%.
- Sin embargo, si el vehículo está afecto **exclusivamente** a una actividad de alquiler (como parece ser vuestro caso con estas furgonetas/Mustang), **se puede deducir el 100% del IVA**, tanto de la compra/importación como de los gastos asociados (seguro, mantenimiento, combustible).
- Esto es una diferencia económica grande sobre +80.000 € de inversión. Confirmad con la gestoría que se está aplicando el 100% y no el 50% por defecto.

## 4. Vehículos parados (los 2 que ya no se alquilan)

- Un activo que no genera ingresos pero sigue generando gastos (seguro, impuesto de circulación, depreciación contable) erosiona la rentabilidad global sin que se note "a simple vista" en la caja.
- Recomendación: decidir explícitamente para cada uno de los 2 vehículos parados: (a) plan y fecha para volver a alquilarlo, (b) venderlo y liberar capital, o (c) uso interno de la empresa. Un activo "aparcado sin decisión" durante meses suele ser la forma más silenciosa de perder rentabilidad.

## 5. Sobre no fiaros de la gestoría

Es razonable querer llevar vuestro propio control en paralelo — de hecho es una buena práctica incluso con una gestoría de confianza. Recomendaciones concretas:

- No canceléis a Fisama todavía sin tener este sistema alimentado con al menos unos meses de datos reales y contrastados.
- Pedid a Fisama el libro de facturas y las cuentas presentadas (ver `PENDIENTE.md`, sección 2) y comparadlo con lo que vayáis metiendo aquí.
- Si encontráis discrepancias, tratadlo primero como pregunta ("¿por qué esta factura no aparece?") antes que como acusación — muchas veces son diferencias de criterio contable, no errores.

## 6. Próximos pasos de rentabilidad e inversión (cuando ya tengamos datos reales)

Una vez tengamos al menos 3-6 meses de datos reales en `/datos/`, podremos:

- Calcular el **payback real** de cada vehículo (cuánto tarda en recuperar lo invertido).
- Ver si la línea de **alquiler de vehículos** genera caja suficiente para autofinanciar el crecimiento, o si sigue dependiendo de aportaciones de los socios.
- Definir un **colchón de tesorería** recomendado antes de acometer nuevas inversiones (regla general: 3-6 meses de gastos fijos de la empresa).
- Analizar si conviene reinvertir beneficios en más vehículos, en la línea de servicios, o repartir dividendos — y qué impuestos conlleva cada opción (Impuesto de Sociedades al 25% —o 15% los 2 primeros años con base imponible positiva si aplican los requisitos de empresa de nueva creación— y luego IRPF al repartir dividendos a los socios).

Este documento se irá ampliando y matizando a medida que tengamos vuestros datos reales — de momento son las líneas generales a vigilar.
