# Estados definitivos por entidad

## Objetivo

Definir estados funcionales estables para las entidades principales del motor de provisiones, con foco en control, auditoria y trazabilidad contable.

Los estados se plantean como vocabulario inicial comun. Podran adaptarse durante el prototipo, pero deben preservar una regla: ningun gasto llega a resultados sin provision previa o provision tardia auditada.

## Pedido interno

Estados:

```text
Borrador
Enviado
PendienteMapeoProveedor
PendienteValidacionAdministracion
ProvisionGenerada
ProvisionIntegrada
EnConsumo
ConsumidoParcialmente
ConsumidoTotalmente
Cerrado
Cancelado
```

Transiciones principales:

```text
Borrador -> Enviado
Enviado -> PendienteMapeoProveedor
Enviado -> PendienteValidacionAdministracion
Enviado -> ProvisionGenerada
PendienteMapeoProveedor -> PendienteValidacionAdministracion
PendienteValidacionAdministracion -> ProvisionGenerada
ProvisionGenerada -> ProvisionIntegrada
ProvisionIntegrada -> EnConsumo
EnConsumo -> ConsumidoParcialmente
EnConsumo -> ConsumidoTotalmente
ConsumidoParcialmente -> ConsumidoTotalmente
ConsumidoTotalmente -> Cerrado
Borrador -> Cancelado
Enviado -> Cancelado
```

Reglas:

- `Borrador` no genera impacto ni asiento.
- `Enviado` debe generar o reservar `id_provision`.
- `PendienteMapeoProveedor` bloquea integracion contable automatica.
- `PendienteValidacionAdministracion` requiere decision humana.
- `Cancelado` exige motivo si ya existia provision.

## Provision

Estados:

```text
Creada
PendienteMapeoProveedor
PendienteValidacion
PendienteIntegracion
Integrada
Abierta
ConsumoSugerido
ConsumoPreparado
ConsumidaParcialmente
ConsumidaTotalmente
PendienteRegularizacion
Regularizada
Cerrada
Anulada
```

Transiciones principales:

```text
Creada -> PendienteMapeoProveedor
Creada -> PendienteValidacion
Creada -> PendienteIntegracion
PendienteMapeoProveedor -> PendienteValidacion
PendienteValidacion -> PendienteIntegracion
PendienteIntegracion -> Integrada
Integrada -> Abierta
Abierta -> ConsumoSugerido
ConsumoSugerido -> ConsumoPreparado
ConsumoPreparado -> ConsumidaParcialmente
ConsumoPreparado -> ConsumidaTotalmente
ConsumidaParcialmente -> ConsumoSugerido
ConsumidaParcialmente -> ConsumidaTotalmente
ConsumidaTotalmente -> PendienteRegularizacion
PendienteRegularizacion -> Regularizada
Regularizada -> Cerrada
ConsumidaTotalmente -> Cerrada
Creada -> Anulada
PendienteValidacion -> Anulada
Abierta -> Anulada
```

Reglas:

- `Creada` existe funcionalmente, pero aun puede necesitar mapeo, validacion o integracion.
- `Integrada` confirma que la provision fue enviada o registrada contablemente.
- `Abierta` significa disponible para consumo.
- `ConsumoSugerido` no debe modificar importes consumidos.
- `ConsumoPreparado` implica seleccion revisable antes de aprobacion final.
- `ConsumidaParcialmente` mantiene importe pendiente mayor que cero.
- `ConsumidaTotalmente` puede requerir regularizacion si hay diferencias.
- `Anulada` exige motivo, usuario y auditoria.

## Factura

Estados:

```text
Subida
OCRProcesado
ProveedorDetectado
PendienteAltaProveedor
PendienteProvision
ProvisionSugerida
PendienteValidacionFuncional
PendienteRevisionContable
Validada
Registrada
Contabilizada
Rechazada
Anulada
```

Transiciones principales:

```text
Subida -> OCRProcesado
OCRProcesado -> ProveedorDetectado
ProveedorDetectado -> PendienteAltaProveedor
PendienteAltaProveedor -> PendienteProvision
ProveedorDetectado -> PendienteProvision
ProveedorDetectado -> ProvisionSugerida
PendienteProvision -> ProvisionSugerida
PendienteProvision -> PendienteValidacionFuncional
ProvisionSugerida -> PendienteValidacionFuncional
PendienteValidacionFuncional -> PendienteRevisionContable
PendienteRevisionContable -> Validada
Validada -> Registrada
Registrada -> Contabilizada
Subida -> Rechazada
PendienteValidacionFuncional -> Rechazada
PendienteRevisionContable -> Rechazada
Registrada -> Anulada
```

Reglas:

- `PendienteAltaProveedor` bloquea el registro hasta confirmar proveedor fiscal para la sociedad.
- `PendienteProvision` puede resolverse con provision existente o provision tardia.
- `PendienteValidacionFuncional` confirma que el servicio corresponde.
- `PendienteRevisionContable` confirma datos fiscales, impuestos, cuentas, periodificacion y consumo.
- `Registrada` esta lista para integracion ERP.
- `Contabilizada` confirma impacto final.
- `Rechazada` exige motivo.

## Relacion factura-provision

Estados:

```text
Sugerida
Seleccionada
PendienteRevision
Aprobada
Integrada
Rechazada
Anulada
```

Transiciones principales:

```text
Sugerida -> Seleccionada
Seleccionada -> PendienteRevision
PendienteRevision -> Aprobada
Aprobada -> Integrada
Sugerida -> Rechazada
Seleccionada -> Rechazada
PendienteRevision -> Rechazada
Aprobada -> Anulada
```

Reglas:

- `Sugerida` puede venir de IA, historico o reglas.
- `Aprobada` actualiza consumo funcional.
- `Integrada` confirma que el consumo fue procesado por integracion o asiento.
- Rechazar una sugerencia debe guardar motivo para mejorar futuros matching.

## Mapeo proveedor

Estados:

```text
PendienteMapeo
SugeridoPorIA
MapeadoPorHistorico
PendienteValidacionAdministracion
ValidadoAdministracion
ConfirmadoPorFactura
Rechazado
Corregido
Inactivo
```

Transiciones principales:

```text
PendienteMapeo -> SugeridoPorIA
PendienteMapeo -> MapeadoPorHistorico
SugeridoPorIA -> PendienteValidacionAdministracion
MapeadoPorHistorico -> PendienteValidacionAdministracion
PendienteValidacionAdministracion -> ValidadoAdministracion
ValidadoAdministracion -> ConfirmadoPorFactura
SugeridoPorIA -> Rechazado
MapeadoPorHistorico -> Rechazado
ValidadoAdministracion -> Corregido
Corregido -> ValidadoAdministracion
ValidadoAdministracion -> Inactivo
```

Reglas:

- Solo `ValidadoAdministracion` y `ConfirmadoPorFactura` pueden actuar como verdad operativa para nuevos casos.
- `SugeridoPorIA` nunca debe bastar para integracion contable automatica.
- `Corregido` debe preservar el valor anterior.

## Solicitud de alta proveedor

Estados:

```text
Detectada
PendienteValidacionAdministracion
ListaParaEnvioERP
EnviadaERP
ConfirmadaERP
FallidaERP
Cancelada
```

Transiciones principales:

```text
Detectada -> PendienteValidacionAdministracion
PendienteValidacionAdministracion -> ListaParaEnvioERP
ListaParaEnvioERP -> EnviadaERP
EnviadaERP -> ConfirmadaERP
EnviadaERP -> FallidaERP
FallidaERP -> ListaParaEnvioERP
Detectada -> Cancelada
PendienteValidacionAdministracion -> Cancelada
```

Reglas:

- `ConfirmadaERP` desbloquea la factura afectada.
- `FallidaERP` exige motivo tecnico o funcional.
- `Cancelada` exige motivo si habia una factura bloqueada.
- En MVP la confirmacion ERP puede estar simulada.

## Movimiento de tarjeta

Estados:

```text
Importado
PendienteClasificacion
ProvisionGenerada
PendienteFactura
FacturaAsociada
MarcadoSinFactura
PendienteRegularizacion
Regularizado
Conciliado
Cerrado
Rechazado
```

Transiciones principales:

```text
Importado -> PendienteClasificacion
PendienteClasificacion -> ProvisionGenerada
ProvisionGenerada -> PendienteFactura
PendienteFactura -> FacturaAsociada
PendienteFactura -> MarcadoSinFactura
FacturaAsociada -> PendienteRegularizacion
MarcadoSinFactura -> PendienteRegularizacion
PendienteRegularizacion -> Regularizado
Regularizado -> Conciliado
Conciliado -> Cerrado
Importado -> Rechazado
PendienteClasificacion -> Rechazado
```

Reglas:

- `MarcadoSinFactura` requiere motivo obligatorio.
- `FacturaAsociada` puede relacionarse con una factura agrupada.
- `Conciliado` depende de liquidacion bancaria o extracto de tarjeta.

## Regularizacion

Estados:

```text
Calculada
PendienteRevision
Aprobada
PendienteIntegracion
Integrada
Rechazada
Anulada
```

Transiciones principales:

```text
Calculada -> PendienteRevision
PendienteRevision -> Aprobada
Aprobada -> PendienteIntegracion
PendienteIntegracion -> Integrada
Calculada -> Rechazada
PendienteRevision -> Rechazada
Aprobada -> Anulada
```

Reglas:

- Toda regularizacion debe tener tipo, motivo e importe.
- Las regularizaciones por no deducible o sin factura deben alimentar reporting.
- La anulacion exige motivo y auditoria.

## Periodo de cierre

Estados:

```text
Preparado
Abierto
EnRevision
Cerrado
Reabierto
```

Transiciones principales:

```text
Preparado -> Abierto
Abierto -> EnRevision
EnRevision -> Cerrado
Cerrado -> Reabierto
Reabierto -> EnRevision
```

Reglas:

- `EnRevision` dispara controles de pendientes y alertas.
- `Cerrado` no debe permitir nuevos consumos sin excepcion auditada.
- `Reabierto` exige motivo y usuario.

## Alerta

Estados:

```text
Creada
Notificada
Reconocida
Escalada
Resuelta
Cerrada
Cancelada
```

Transiciones principales:

```text
Creada -> Notificada
Notificada -> Reconocida
Reconocida -> Resuelta
Notificada -> Escalada
Escalada -> Resuelta
Resuelta -> Cerrada
Creada -> Cancelada
Notificada -> Cancelada
```

Reglas:

- `Escalada` se usa cuando no hay respuesta antes de fecha objetivo.
- `Resuelta` exige indicar como se resolvio el pendiente.
- La alerta debe mantener vinculo con entidad origen.

## Provision tardia

La provision tardia no es una entidad separada, sino una `provision` con `origen_provision = ProvisionTardiaDesdeFactura`.

Reglas obligatorias:

- Debe nacer desde una factura concreta.
- Debe consumirse inmediatamente o quedar bloqueada.
- Debe registrar responsable, motivo, usuario, fecha, factura origen e importe.
- Debe aparecer en reporting de excepciones.

## Estados que bloquean integracion contable

Estados bloqueantes:

- `PendienteMapeoProveedor`.
- `PendienteValidacion`.
- `PendienteValidacionAdministracion`.
- `PendienteAltaProveedor`.
- `PendienteProvision`.
- `PendienteValidacionFuncional`.
- `PendienteRevisionContable`.
- `Sugerida`.
- `Seleccionada`.
- `PendienteRevision`.
- `Rechazada`.
- `FallidaERP`.

## Estados aptos para reporting de cumplimiento

Indicadores recomendados:

- Provisiones abiertas por antiguedad.
- Facturas en `PendienteProvision`.
- Provisiones tardias creadas por periodo.
- Movimientos en `PendienteFactura`.
- Movimientos `MarcadoSinFactura`.
- Mapeos `Rechazado` o `Corregido`.
- Regularizaciones pendientes.
