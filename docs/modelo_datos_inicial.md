# Modelo de datos inicial

## Objetivo

Definir un modelo funcional inicial para el motor comun de provisiones, separando la realidad operativa, la verdad fiscal/contable y la trazabilidad de decisiones.

El modelo no presupone tecnologia ni plan contable concreto. Describe entidades, relaciones y campos funcionales necesarios para construir un prototipo y conversar con area financiera, sistemas y negocio.

## Principios de modelado

- La provision es la entidad central del ciclo de gasto.
- El origen operativo no debe contaminar el motor comun.
- El proveedor operativo informado por usuario se separa del proveedor fiscal validado.
- Una factura puede consumir varias provisiones.
- Una provision puede consumirse con varias facturas.
- Toda decision relevante debe tener auditoria.
- La IA puede crear sugerencias, no verdades contables.
- El tenant es frontera funcional y futura frontera de seguridad.
- La legal entity representa la sociedad sobre la que aplican proveedor fiscal, periodo, ERP y reglas contables.

## Entidades principales

### tenant

Representa el cliente, grupo empresarial o unidad aislada dentro del SaaS.

Campos recomendados:

- id_tenant.
- nombre_tenant.
- estado_tenant.
- pais_principal.
- moneda_principal.
- creado_por.
- fecha_creacion.

Reglas:

- Un tenant puede contener varias legal entities.
- Ninguna consulta futura debe mezclar datos entre tenants sin autorizacion explicita.
- En MVP puede existir un tenant unico de prueba.

### legal_entity

Representa una sociedad juridica dentro de un tenant.

Campos recomendados:

- id_legal_entity.
- id_tenant.
- codigo_sociedad_erp.
- nombre_sociedad.
- pais.
- moneda_funcional.
- identificador_fiscal.
- estado_sociedad.
- fecha_inicio_operacion.
- fecha_fin_operacion.

Reglas:

- Una provision, factura o proveedor fiscal debe estar asociada a una legal entity.
- Una legal entity puede tener integracion ERP propia.
- Las reglas fiscales futuras se aplicaran como minimo por legal entity.

### usuario

Persona o servicio autenticado en ProvCore.

Campos recomendados:

- id_usuario.
- id_tenant.
- tipo_usuario.
- nombre_visible.
- email.
- estado_usuario.
- origen_identidad.
- creado_por.
- fecha_creacion.

Reglas:

- Todo usuario pertenece a un tenant.
- Un usuario puede tener varios roles.
- Un servicio de integracion tambien debe modelarse como actor auditable.

### rol

Perfil funcional asignable a usuarios o servicios.

Campos recomendados:

- id_rol.
- id_tenant.
- codigo_rol.
- nombre_rol.
- descripcion.
- estado_rol.

Valores iniciales:

```text
UsuarioOperativo
UsuarioFinancieroAutorizado
SupervisorFinanciero
AdministradorTenant
AdministradorTecnico
ServicioIntegracion
Auditor
```

### permiso

Capacidad concreta de ejecutar una accion.

Campos recomendados:

- id_permiso.
- codigo_permiso.
- descripcion.
- categoria_permiso.

### usuario_rol

Asignacion de rol a usuario con alcance.

Campos recomendados:

- id_usuario_rol.
- id_usuario.
- id_rol.
- id_tenant.
- id_legal_entity.
- id_buyer_group.
- area.
- pais.
- fecha_desde.
- fecha_hasta.
- estado_asignacion.

Reglas:

- Un rol sin alcance valido no autoriza operaciones sensibles.
- Las operaciones fiscales y contables requieren legal entity.

### rol_permiso

Relacion entre rol y permiso.

Campos recomendados:

- id_rol_permiso.
- id_rol.
- id_permiso.
- estado_permiso.

Reglas:

- El permiso define la accion.
- El alcance viene de la asignacion del usuario.

### pedido_interno

Representa el compromiso de gasto informado por un responsable antes de recibir la factura.

Campos recomendados:

- id_pedido_interno.
- id_tenant.
- id_legal_entity.
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
- id_tenant.
- id_legal_entity.
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
- id_tenant.
- id_legal_entity.
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
- id_solicitud_alta_proveedor.
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
- id_tenant.
- id_legal_entity.
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
- id_tenant.
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
- id_tenant.
- id_legal_entity.
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

- Es fuente de verdad solo si procede de ERP o validacion de usuario financiero autorizado.
- Puede estar asociado a multiples proveedores operativos o alias.
- Puede existir para una legal entity y no para otra.

### solicitud_alta_proveedor

Solicitud para crear o validar un proveedor fiscal en ERP antes de continuar el flujo de factura.

Campos recomendados:

- id_solicitud_alta_proveedor.
- id_tenant.
- id_legal_entity.
- id_factura.
- razon_social_detectada.
- nif_vat_detectado.
- pais_detectado.
- direccion_detectada.
- estado_solicitud.
- origen_deteccion.
- enviada_erp.
- codigo_respuesta_erp.
- id_proveedor_fiscal_resultante.
- motivo_bloqueo.
- creada_por.
- fecha_creacion.
- confirmada_por.
- fecha_confirmacion.

Reglas:

- Si el proveedor fiscal no existe para la legal entity, la factura queda bloqueada.
- La factura solo continua cuando el ERP confirma o un usuario financiero autorizado valida una alternativa.
- En MVP se puede simular la respuesta ERP.

### mapeo_proveedor

Une alias/proveedor operativo con proveedor fiscal validado o sugerido.

Campos recomendados:

- id_mapeo_proveedor.
- id_tenant.
- id_legal_entity.
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
- Solo un usuario financiero autorizado puede convertir un mapeo en validado.
- Todo rechazo o correccion alimenta historico auditable.

### buyer_group

Grupo comprador o responsable operativo asociado a proveedores, sociedades o areas.

Campos recomendados:

- id_buyer_group.
- id_tenant.
- codigo_buyer_group_erp.
- nombre_buyer_group.
- origen_dato.
- estado_buyer_group.
- creado_por.
- fecha_creacion.

Reglas:

- Puede venir del ERP o de configuracion interna.
- Alimenta alertas, control de cierre y responsabilidad por proveedor.

### supplier_responsibility

Relacion entre proveedor fiscal, proveedor operativo o area y grupo responsable.

Campos recomendados:

- id_supplier_responsibility.
- id_tenant.
- id_legal_entity.
- id_proveedor_fiscal.
- id_proveedor_operativo.
- id_buyer_group.
- fecha_desde.
- fecha_hasta.
- origen_asignacion.
- estado_asignacion.
- creado_por.
- fecha_creacion.

Reglas:

- Permite saber a que grupo avisar por movimientos abiertos o excepciones.
- Debe poder cambiar en el tiempo sin perder historico.

### movimiento_tarjeta

Movimiento operativo de tarjeta corporativa que genera provision.

Campos recomendados:

- id_movimiento_tarjeta.
- id_tenant.
- id_legal_entity.
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
- id_tenant.
- id_legal_entity.
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
- id_tenant.
- id_legal_entity.
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
- id_tenant.
- id_legal_entity.
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
- id_tenant.
- id_legal_entity.
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
- rol_usado.
- permiso_usado.
- fecha_hora.
- correlacion_proceso.

Reglas:

- Debe cubrir cambios de estado, consumos, rechazos, mapeos, provisiones tardias, regularizaciones y anulaciones.
- Debe permitir reconstruir quien decidio que, cuando y por que.

### evento_proceso

Registro estructurado de eventos explotables para analitica y trazabilidad.

Campos recomendados:

- id_evento_proceso.
- id_tenant.
- id_legal_entity.
- tipo_evento.
- entidad.
- id_entidad.
- origen_evento.
- payload_resumido.
- correlacion_proceso.
- fecha_hora.

Reglas:

- No sustituye a la auditoria de decisiones.
- Sirve para metricas de tiempos, conversiones, bloqueos y eficiencia operativa.
- En MVP puede convivir fisicamente con auditoria si se documenta la distincion.

### periodo_cierre

Periodo operativo o financiero usado para control de cierre y alertas.

Campos recomendados:

- id_periodo_cierre.
- id_tenant.
- id_legal_entity.
- periodo.
- fecha_inicio.
- fecha_fin.
- fecha_limite_operativa.
- fecha_limite_contable.
- estado_periodo.
- creado_por.
- fecha_creacion.

Reglas:

- Permite detectar pendientes antes del cierre.
- Puede variar por legal entity.

### alerta

Aviso generado para usuario o grupo responsable.

Campos recomendados:

- id_alerta.
- id_tenant.
- id_legal_entity.
- id_periodo_cierre.
- id_buyer_group.
- usuario_destino.
- tipo_alerta.
- entidad_origen.
- id_entidad_origen.
- prioridad.
- estado_alerta.
- fecha_objetivo.
- fecha_creacion.
- fecha_resolucion.
- resuelta_por.
- motivo_resolucion.

Reglas:

- Debe poder dirigirse a usuario o grupo.
- Debe enlazar con la entidad que genera el pendiente.
- Debe ser medible para reporting de cierre.

### comentario

Comentarios funcionales o contables asociados a entidades.

Campos recomendados:

- id_comentario.
- id_tenant.
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
- id_tenant.
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
tenant 1 -> N legal_entity
tenant 1 -> N usuario
tenant 1 -> N rol
tenant 1 -> N buyer_group
usuario N -> N rol mediante usuario_rol
rol N -> N permiso mediante rol_permiso
legal_entity 1 -> N pedido_interno
legal_entity 1 -> N provision
legal_entity 1 -> N factura
legal_entity 1 -> N proveedor_fiscal
pedido_interno 1 -> 1 provision
movimiento_tarjeta 1 -> 1 provision
factura N -> N provision mediante factura_provision
proveedor_operativo N -> N proveedor_fiscal mediante mapeo_proveedor
factura 1 -> N solicitud_alta_proveedor
proveedor_fiscal 1 -> N supplier_responsibility
buyer_group 1 -> N supplier_responsibility
buyer_group 1 -> N alerta
periodo_cierre 1 -> N alerta
provision 1 -> N regularizacion
factura 1 -> N regularizacion
factura 1 -> N periodificacion
liquidacion_tarjeta 1 -> N movimiento_tarjeta
entidad funcional 1 -> N auditoria_estado
entidad funcional 1 -> N evento_proceso
entidad funcional 1 -> N comentario
entidad funcional 1 -> N adjunto
```

## Campos transversales recomendados

Para entidades principales:

- id_tenant.
- id_legal_entity cuando aplique.
- usuario.
- rol_usado cuando aplique.
- permiso_usado cuando aplique.
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

- tenant + estado.
- tenant + legal entity + periodo.
- usuario + rol + tenant.
- rol + permiso.
- `id_provision`.
- proveedor fiscal + sociedad + periodo.
- proveedor operativo + responsable + area.
- factura + numero + proveedor fiscal + sociedad.
- estado de provision + importe pendiente.
- origen provision + id origen.
- responsable + periodo.
- estado de mapeo + confianza.
- buyer group + periodo + estado de alerta.
- tipo evento + fecha_hora + correlacion_proceso.

## Decisiones pendientes

- Si `pedido_interno` puede tener mas de una provision en casos de desglose por periodo o centro de coste.
- Nivel exacto de tolerancia para diferencias antes de exigir regularizacion.
- Si la periodificacion se decide en provision, factura o ambos.
- Como versionar reglas contables y fiscales sin acoplarlas al ERP.
- Como representar roles y permisos en el modelo final.
- Como aislar tenants fisicamente en una version productiva.
- Que datos minimos exige cada ERP para alta de proveedor fiscal.
