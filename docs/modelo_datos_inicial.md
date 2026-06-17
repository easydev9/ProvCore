# Modelo de datos inicial

## Objetivo

Definir un modelo funcional inicial para el motor comun de provisiones, separando la realidad operativa, la verdad fiscal/contable y la trazabilidad de decisiones.

El modelo no presupone tecnologia ni plan contable concreto. Describe entidades, relaciones y campos funcionales necesarios para construir un prototipo y conversar con Administracion, sistemas y negocio.

## Principios de modelado

- La provision es la entidad central del ciclo de gasto.
- El origen operativo no debe contaminar el motor comun.
- El proveedor operativo informado por usuario se separa del proveedor fiscal validado.
- Una factura puede consumir varias provisiones.
- Una provision puede consumirse con varias facturas.
- Toda decision relevante debe tener auditoria.
- La IA puede crear sugerencias, no verdades contables.

## Entidades principales

### pedido_interno

Representa el compromiso de gasto informado por un responsable antes de recibir la factura.

Campos recomendados:

- id_pedido_interno.
- id_provision.
- sociedad.
- area.
- centro_coste.
- responsable.
- proveedor_informado.
- id_proveedor_operativo.
- descripcion_servicio.
- tipo_gasto.
- tipo_servicio.
- importe_estimado.
- moneda.
- fecha_compromiso.
- fecha_esperada_factura.
- periodo_servicio_desde.
- periodo_servicio_hasta.
- espera_factura.
- recurrente.
- estado_pedido.
- creado_por.
- fecha_creacion.
- modificado_por.
- fecha_modificacion.

Reglas:

- Todo pedido enviado debe generar o tener asociado un `id_provision`.
- El responsable no informa datos fiscales obligatorios.
- Si falta proveedor fiscal validado, el pedido puede quedar pendiente de mapeo o validacion.

### provision

Entidad central del motor. Representa el gasto estimado que debe existir antes del impacto definitivo en resultados.

Campos recomendados:

- id_provision.
- origen_provision.
- id_origen.
- sociedad.
- area.
- responsable.
- id_proveedor_operativo.
- id_proveedor_fiscal_validado.
- tipo_gasto.
- importe_provisionado.
- importe_consumido.
- importe_pendiente.
- moneda.
- periodo_desde.
- periodo_hasta.
- estado_provision.
- requiere_regularizacion.
- deducibilidad_estimada.
- asiento_provision_id.
- fecha_integracion_provision.
- motivo_anulacion.
- creada_por.
- fecha_creacion.
- cerrada_por.
- fecha_cierre.

Valores esperados de `origen_provision`:

```text
PedidoInternoProveedor
MovimientoTarjetaCorporativa
ProvisionTardiaDesdeFactura
SuscripcionRecurrente
```

Reglas:

- El importe pendiente se deriva de importe provisionado menos consumos aprobados.
- Una provision integrada puede seguir abierta si no esta consumida totalmente.
- La anulacion debe exigir motivo y auditoria.

### factura

Documento fiscal recibido de proveedor. Es maestra del documento, OCR, validacion e integracion ERP.

Campos recomendados:

- id_factura.
- sociedad.
- proveedor_fiscal_detectado.
- id_proveedor_fiscal_validado.
- nif_vat_proveedor.
- numero_factura.
- fecha_factura.
- fecha_recepcion.
- base_imponible.
- impuestos.
- total_factura.
- moneda.
- tipo_cambio_aplicado.
- estado_factura.
- estado_ocr.
- estado_validacion_funcional.
- estado_revision_contable.
- estado_contabilizacion.
- deducibilidad.
- requiere_periodificacion.
- asiento_factura_id.
- fecha_contabilizacion.
- documento_origen.
- subida_por.
- fecha_subida.

Reglas:

- Una factura puede existir sin provision compatible, pero no debe contabilizarse sin provision consumida o provision tardia auditada.
- El proveedor fiscal detectado por OCR/IA debe validarse contra datos maestros.
- La factura guarda relaciones de consumo, no solo un campo simple de provision.

### factura_provision

Relacion de consumo entre factura y provision.

Campos recomendados:

- id_factura_provision.
- id_factura.
- id_provision.
- importe_consumido.
- moneda_consumo.
- porcentaje_consumo.
- diferencia_importe.
- motivo_diferencia.
- estado_relacion.
- sugerido_por.
- confianza_sugerencia.
- aprobado_por.
- fecha_aprobacion.
- integrado_erp.
- fecha_integracion.

Reglas:

- Permite relacion N a N entre facturas y provisiones.
- Todo consumo aprobado actualiza importe consumido e importe pendiente de la provision.
- Si hay diferencia relevante, debe crear o marcar regularizacion.

### proveedor_operativo

Proveedor como lo conoce el usuario de campo.

Campos recomendados:

- id_proveedor_operativo.
- alias_principal.
- alias_normalizado.
- descripcion.
- categoria_gasto_habitual.
- responsable_habitual.
- area_habitual.
- pais_estimado.
- activo.
- creado_por.
- fecha_creacion.

Reglas:

- Puede tener multiples alias informados por usuarios.
- No sustituye al proveedor fiscal.

### proveedor_fiscal

Proveedor validado contra ERP o datos maestros.

Campos recomendados:

- id_proveedor_fiscal.
- codigo_proveedor_erp.
- razon_social.
- nif_vat.
- pais.
- sociedad.
- direccion_fiscal.
- estado_dato_maestro.
- fecha_alta_erp.
- fecha_ultima_validacion.

Reglas:

- Es fuente de verdad solo si procede de ERP o validacion de Administracion.
- Puede estar asociado a multiples proveedores operativos o alias.

### mapeo_proveedor

Une alias/proveedor operativo con proveedor fiscal validado o sugerido.

Campos recomendados:

- id_mapeo_proveedor.
- id_proveedor_operativo.
- alias_informado.
- id_proveedor_fiscal_sugerido.
- id_proveedor_fiscal_validado.
- sociedad.
- confianza_matching.
- origen_sugerencia.
- explicacion_sugerencia.
- estado_mapeo.
- validado_por.
- fecha_validacion.
- rechazado_por.
- fecha_rechazo.
- motivo_rechazo.

Reglas:

- La IA puede crear mapeos sugeridos.
- Solo Administracion puede convertir un mapeo en validado.
- Todo rechazo o correccion alimenta historico auditable.

### movimiento_tarjeta

Movimiento operativo de tarjeta corporativa que genera provision.

Campos recomendados:

- id_movimiento_tarjeta.
- id_provision.
- sociedad.
- titular_tarjeta.
- responsable.
- area.
- fecha_movimiento.
- comercio_informado.
- id_proveedor_operativo.
- importe_movimiento.
- moneda_movimiento.
- importe_liquidado.
- moneda_liquidacion.
- descripcion_gasto.
- categoria_gasto.
- espera_factura.
- factura_recibida.
- motivo_sin_factura.
- estado_movimiento.
- id_liquidacion_tarjeta.

Reglas:

- Todo movimiento debe generar provision o asociarse a una existente segun reglas.
- Marcar sin factura exige motivo obligatorio.
- Las diferencias por divisa se regularizan contra factura o liquidacion.

### liquidacion_tarjeta

Agrupa movimientos contra liquidacion bancaria o extracto de tarjeta.

Campos recomendados:

- id_liquidacion_tarjeta.
- sociedad.
- entidad_tarjeta.
- periodo_liquidacion.
- fecha_liquidacion.
- importe_total.
- moneda.
- estado_liquidacion.
- asiento_liquidacion_id.
- fecha_integracion.

Reglas:

- Una liquidacion tiene muchos movimientos.
- Puede generar regularizaciones por divisa o diferencias contra extracto.

### regularizacion

Ajuste generado por diferencia entre provision, factura, impuestos, divisa, periodificacion o ausencia de factura.

Campos recomendados:

- id_regularizacion.
- id_provision.
- id_factura.
- id_movimiento_tarjeta.
- tipo_regularizacion.
- importe_regularizacion.
- moneda.
- signo.
- motivo.
- deducibilidad.
- estado_regularizacion.
- asiento_regularizacion_id.
- creada_por.
- fecha_creacion.
- aprobada_por.
- fecha_aprobacion.
- fecha_integracion.

Valores esperados de `tipo_regularizacion`:

```text
DiferenciaImporte
DiferenciaImpuesto
DiferenciaDivisa
Periodificacion
NoDeducible
SinFactura
AnulacionProvision
```

### periodificacion

Distribucion temporal de un gasto entre periodos.

Campos recomendados:

- id_periodificacion.
- id_factura.
- id_provision.
- periodo.
- importe_periodificado.
- moneda.
- porcentaje.
- estado_periodificacion.
- criterio.
- aprobada_por.
- fecha_aprobacion.

### auditoria_estado

Registro comun de cambios relevantes.

Campos recomendados:

- id_auditoria.
- entidad.
- id_entidad.
- accion.
- estado_anterior.
- estado_posterior.
- campo_modificado.
- valor_anterior.
- valor_nuevo.
- motivo.
- origen_accion.
- usuario.
- fecha_hora.
- correlacion_proceso.

Reglas:

- Debe cubrir cambios de estado, consumos, rechazos, mapeos, provisiones tardias, regularizaciones y anulaciones.
- Debe permitir reconstruir quien decidio que, cuando y por que.

### comentario

Comentarios funcionales o contables asociados a entidades.

Campos recomendados:

- id_comentario.
- entidad.
- id_entidad.
- tipo_comentario.
- texto.
- visibilidad.
- creado_por.
- fecha_creacion.

### adjunto

Documentacion soporte.

Campos recomendados:

- id_adjunto.
- entidad.
- id_entidad.
- tipo_adjunto.
- nombre_archivo.
- hash_documento.
- origen.
- subido_por.
- fecha_subida.

## Relaciones clave

```text
pedido_interno 1 -> 1 provision
movimiento_tarjeta 1 -> 1 provision
factura N -> N provision mediante factura_provision
proveedor_operativo N -> N proveedor_fiscal mediante mapeo_proveedor
provision 1 -> N regularizacion
factura 1 -> N regularizacion
factura 1 -> N periodificacion
liquidacion_tarjeta 1 -> N movimiento_tarjeta
entidad funcional 1 -> N auditoria_estado
entidad funcional 1 -> N comentario
entidad funcional 1 -> N adjunto
```

## Campos transversales recomendados

Para entidades principales:

- sociedad.
- responsable.
- area.
- moneda.
- estado.
- creado_por.
- fecha_creacion.
- modificado_por.
- fecha_modificacion.
- origen.
- correlacion_proceso.

## Indices funcionales sugeridos

- `id_provision`.
- proveedor fiscal + sociedad + periodo.
- proveedor operativo + responsable + area.
- factura + numero + proveedor fiscal + sociedad.
- estado de provision + importe pendiente.
- origen provision + id origen.
- responsable + periodo.
- estado de mapeo + confianza.

## Decisiones pendientes

- Si `pedido_interno` puede tener mas de una provision en casos de desglose por periodo o centro de coste.
- Nivel exacto de tolerancia para diferencias antes de exigir regularizacion.
- Si la periodificacion se decide en provision, factura o ambos.
- Como versionar reglas contables y fiscales sin acoplarlas al ERP.
- Como representar roles y permisos en el modelo final.
