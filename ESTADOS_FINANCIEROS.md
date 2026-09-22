# Balance de Situación y Cuenta de Pérdidas y Ganancias

Cómo está montado, dónde se guarda cada cosa y qué necesito de vosotros para que ambos estados estén siempre al día.

**El resultado está en [`informes/Estados_Financieros_Berts.xlsx`](informes/Estados_Financieros_Berts.xlsx).** Si solo queréis echar un vistazo desde el móvil, también está en texto: [`balance_situacion.md`](informes/balance_situacion.md) y [`cuenta_perdidas_ganancias.md`](informes/cuenta_perdidas_ganancias.md).

---

## 1. La idea en una frase

Vosotros me pasáis **documentos** (facturas, extractos, justificantes). Yo los apunto en unas **hojas de datos** sencillas. Un script convierte cada dato en su **asiento contable** y de ahí salen **solos** el balance y la PyG. Todo queda guardado en Git con fecha, así que nada se pierde y siempre se puede ver quién cambió qué.

```
 Vosotros                Yo (Claude)                  Automático
 ─────────               ──────────────               ─────────────────────────────────
 Foto / PDF   ──►  archivo en /facturas/  ──►  fila en /datos/*.csv  ──►  Libro diario (asientos)
 Extracto                                                                     │
 "Roberto metió                                                               ├──► Balance de situación
  5.000 €"                                                                    ├──► Cuenta de PyG
                                                                              ├──► IVA por trimestre
                                                                              └──► Rentabilidad por vehículo
```

No tenéis que saber contabilidad ni tocar el Excel. El Excel **no se edita a mano**: se vuelve a generar cada vez que entra información nueva.

## 2. Dónde vive cada cosa

| Qué | Dónde | Quién lo toca |
|---|---|---|
| Documentos originales (facturas, contratos, extractos) | `facturas/` y `documentos/` | Yo, con lo que me mandáis |
| Documentos sin clasificar | `bandeja_entrada/` | Vosotros (lo soltáis ahí y yo lo ordeno) |
| **Datos de entrada** (una fila por operación) | `datos/*.csv` | Yo |
| Motor contable (reglas de qué asiento genera cada cosa) | `scripts/contabilidad.py` | Nadie en el día a día |
| **Estados financieros** | `informes/` | Nadie: se generan solos |

### Las hojas de datos (`datos/`)

| Archivo | Qué se apunta | Asiento que genera |
|---|---|---|
| `saldos_apertura.csv` | El balance de Fisama a 31/12/2025. Se toca una vez. | Asiento de apertura |
| `facturas_emitidas.csv` | Cada factura a un cliente (alquileres, venta de un vehículo) | Ingreso + IVA repercutido + cliente; y el cobro si está cobrada |
| `facturas_recibidas.csv` | Cada factura de un proveedor (taller, seguro, gestoría, aduana...) | Gasto **o** mayor valor del vehículo + IVA soportado + proveedor; y el pago si está pagada |
| `vehiculos.csv` | Ficha de cada vehículo: precio, fecha, desde dónde se pagó, % de amortización | Alta del vehículo en el activo y su amortización mensual |
| `aportaciones_capital.csv` | Dinero que metéis los socios, y si es aportación o préstamo | Aportación (fondos propios) o deuda con el socio |
| `asientos_manuales.csv` | Lo que no encaja en lo anterior (reparto del resultado, correcciones, comisiones bancarias...) | El asiento tal cual |
| `saldos_banco_reales.csv` | El saldo real del BBVA en una fecha (del extracto) | Ninguno: es el **control** para comprobar que el banco cuadra |

Hay columnas que deciden cómo se contabiliza cada factura. Las relleno yo:

- **`cuenta_pgc`**: a qué cuenta va. Ejemplos: `6220` reparaciones, `6250` seguros, `6280` combustible, `6310` impuestos (IVTM), `6780` sanciones, `7050` alquileres. **`2180`** significa que no es un gasto del año sino **parte del coste del vehículo** (ITP, gestoría del cambio de titularidad, aduana, arancel, matriculación): ese importe se reparte a lo largo de los años con la amortización.
- **`pagada_si_no` / `cobrada_si_no`**: `si` → el dinero salió/entró del BBVA en `fecha_pago`/`fecha_cobro`. Cualquier otra cosa → queda como deuda pendiente (del cliente o con el proveedor) hasta que se confirme.
- **`pagado_desde`** (vehículos): `banco`, `socio_prestamo` (la empresa se lo debe al socio), `socio_aportacion` (se queda en la empresa) o `desconocido` → va a **partidas pendientes de aplicación** (cuenta 555) hasta que lo aclaremos.

## 3. Qué hay en el Excel

| Hoja | Para qué sirve |
|---|---|
| **Resumen** | Cifras clave, controles de cuadre (todos deben decir OK) y la **fecha de corte** (celda amarilla: se puede poner una fecha anterior para ver el balance a ese día) |
| **Balance** | Modelo oficial PGC Pymes. Columna 31/12/2025 (reproduce exactamente el de Fisama) y columna a la fecha de corte |
| **PyG** | Modelo oficial PGC Pymes. 2025 de Fisama, T1, T2, T3, T4 y acumulado del año, más el detalle por cuenta |
| **Vehículos** | Coste de cada vehículo, amortización, valor neto y si gana o pierde dinero |
| **IVA** | IVA repercutido y soportado por trimestre, para contrastar con el modelo 303 de Fisama |
| **Pendiente** | Todo lo que falta o no cuadra, por prioridad. Se actualiza solo |
| **Diario** | Todos los asientos. **Todo lo demás sale de aquí con fórmulas** |
| Sumas y saldos / Plan de cuentas | Detalle contable, por si Fisama o un auditor lo piden |

## 4. Criterios contables aplicados (para que Fisama los revise)

1. **Punto de partida**: el balance de Fisama a 31/12/2025 tal cual (75.318,61 €). La columna del 31/12/2025 lo reproduce al céntimo.
2. **Resultado 2025 (64,88 €)**: propuesta de reparto → 10 % a reserva legal (6,49 €, art. 274 LSC) y el resto a remanente (58,39 €). *Hay que confirmarlo con el acta de la Junta.*
3. **El activo de 9.192 € de Fisama** («Maquinaria», cuenta 2130) se supone que es la NV200 2436KSS (V2) y se reclasifica a **Elementos de transporte** (2180), que es donde va un vehículo.
4. **Vehículos**: coste = precio + gastos necesarios para ponerlo en marcha (ITP, gestoría, tasas DGT, arancel, transporte, despacho, placas). Las **demoras y el almacenaje en puerto** (1.147 € en total) **no** se suman al coste: son ineficiencias y van a gasto.
5. **Amortización**: lineal, **16 % anual** (máximo de la tabla fiscal para elementos de transporte), calculada por días desde que el vehículo está en uso. Los dos **Mustang no se amortizan** todavía: el Blanco nunca ha estado en condiciones de uso (motor roto) y el Gris no está matriculado. Fisama no amortizó nada en 2025; no se corrige hacia atrás.
6. **Mustang sin factura de compra**: se registran provisionalmente por el **valor declarado en aduana** (incoterm CIF: 6.967,03 € y 7.931,03 €). Cuando llegue la factura real se ajusta.
7. **Venta del Ford Fiesta**: no es un ingreso ordinario. Se da de baja el coche (coste 6.156,70 € − 261,78 € amortizados) y la diferencia con el precio de venta (2.480 €) es una **pérdida de 3.414,92 €** (línea 11 de la PyG).
8. **IVA**: cada trimestre cerrado se liquida contra «IVA a ingresar» (4750) o «IVA a compensar» (4700), arrastrando lo pendiente de compensar. El IVA de facturas que no son a nombre de Berts o de tickets sin datos fiscales **no se deduce**: va a gasto.
9. **Seguros de Mutua**: no estaban en las cuentas de 2025 de Fisama, así que se registran enteros en 2026.
10. **Sanciones**: gasto contable (cuenta 678), pero **no deducible** en el Impuesto sobre Sociedades.
11. **Impuesto sobre Sociedades**: con pérdidas no se registra gasto por impuesto. Tampoco se activa el crédito fiscal por pérdidas (criterio prudente; lo puede decidir Fisama al cierre).
12. **Lo que no sabemos de dónde se pagó** va a la cuenta **555 «Partidas pendientes de aplicación»**, visible en el pasivo. **Tiene que acabar en 0**: cuando tengamos los extractos, cada importe se reparte entre banco, deuda con socios o aportación.

## 5. Cómo me vais pasando la información

Lo más cómodo es adjuntarlo en la conversación con una frase de contexto, como un WhatsApp:

> «Factura del taller de la furgoneta blanca, pagada con tarjeta el 3 de octubre»
> «Extracto del BBVA de enero a septiembre»
> «Roberto metió 3.000 € el 15/10 para la reparación del Mustang, como préstamo»

Yo: (1) guardo el documento, (2) añado la fila, (3) regenero balance y PyG, (4) os digo qué ha cambiado y qué aviso nuevo sale, y (5) hago commit y push, así queda guardado.

Si no estamos hablando, soltad los archivos en `bandeja_entrada/` desde la web de GitHub y los proceso la próxima vez.

### Ritmo recomendado

- **Cada vez que pase algo con dinero**: mandádmelo ese mismo día o esa semana.
- **Una vez al mes**: el **extracto del BBVA** del mes. Es lo que permite cuadrar la tesorería y detectar lo que se ha olvidado.
- **Cada trimestre**, antes del día 20 de abril, julio, octubre y enero: repasamos la hoja **IVA** contra lo que va a presentar Fisama.
- **Al cierre del año**: el script genera solo el asiento de cierre y abre el ejercicio siguiente; solo hay que decidir qué se hace con el resultado.

## 6. Para regenerar a mano (opcional)

```bash
pip install openpyxl                                       # solo la primera vez
python3 scripts/generar_informes.py                        # balance a hoy
python3 scripts/generar_informes.py --corte 2026-06-30     # balance a una fecha concreta
```
