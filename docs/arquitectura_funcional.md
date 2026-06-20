# Arquitectura funcional

## Objetivo

Definir la arquitectura funcional de ProvCore como motor comun de provisiones, separando origenes operativos, gobierno contable, integraciones y analitica.

El documento evita decisiones tecnicas concretas. Su finalidad es explicar responsabilidades, limites de modulo y reglas de gobierno para un futuro prototipo.

## Vision general

ProvCore actua como capa comun entre los eventos operativos que generan gasto y los procesos contables que validan, consumen, regularizan y contabilizan ese gasto.

```text
Origen operativo -> Motor de provisiones -> Validacion / consumo -> ERP / reporting
```

El sistema no sustituye al ERP ni convierte a la IA en fuente de verdad contable. Su papel es adelantar el control, mantener trazabilidad y reducir trabajo manual en la conciliacion entre pedidos, facturas y tarjetas.

El modelo funcional se disena tenant-aware. Un tenant representa el cliente o grupo empresarial y una legal entity representa la sociedad sobre la que aplican proveedor fiscal, ERP, periodos y reglas contables.

## Modulos funcionales

### Pedido interno

Responsabilidad:

- Capturar el compromiso de gasto antes de recibir factura.
- Crear o reservar `id_provision`.
- Recoger informacion operativa entendible por el responsable.
- Enviar a validacion cuando falte proveedor fiscal o dato contable.

No debe hacer:

- Exigir NIF/VAT, codigo ERP o cuenta contable al usuario de campo.
- Contabilizar directamente el gasto.

### Motor comun de provisiones

Responsabilidad:

- Identificar movimientos provisionables y su origen.
- Crear provisiones desde distintos origenes.
- Mantener estados de provision.
- Exponer reglas comunes de consumo.
- Permitir consumos parciales y relaciones N a N con facturas.
- Detectar diferencias y disparar regularizaciones.
- Mantener `id_provision` como trazador comun.

No debe hacer:

- Depender de un origen operativo concreto.
- Validar por si mismo la verdad fiscal final.

### Mapeo de proveedores

Responsabilidad:

- Separar proveedor operativo y proveedor fiscal.
- Gestionar alias informados por usuarios.
- Sugerir candidatos por historico, datos maestros, OCR/IA y similitud.
- Requerir validacion de Administracion antes de convertir un mapeo en verdad.

No debe hacer:

- Convertir una sugerencia de IA en proveedor fiscal validado sin revision.

### Modulo de facturas

Responsabilidad:

- Recibir o registrar facturas.
- Extraer datos por OCR/IA.
- Validar proveedor fiscal contra ERP.
- Buscar provisiones abiertas compatibles.
- Sugerir consumos.
- Preparar registro y contabilizacion.

No debe hacer:

- Contabilizar facturas sin provision consumida o provision tardia auditada.

### Modulo de tarjetas corporativas

Responsabilidad:

- Gestionar movimientos de tarjeta como origen operativo especifico.
- Generar provisiones desde movimientos.
- Asociar facturas soporte.
- Permitir casos sin factura con motivo obligatorio.
- Regularizar diferencias de base, impuestos y divisa.
- Conciliar contra liquidacion bancaria.

No debe hacer:

- Saltarse el motor comun de provisiones.

### Regularizaciones y periodificaciones

Responsabilidad:

- Ajustar diferencias entre provision y factura.
- Registrar diferencias fiscales, no deducibles o sin factura.
- Distribuir gastos por periodo cuando aplique.
- Preparar impacto contable conceptual.

No debe hacer:

- Aplicar reglas fiscales complejas sin validacion de Administracion.

### Auditoria

Responsabilidad:

- Registrar acciones, cambios de estado, decisiones y motivos.
- Permitir reconstruir el ciclo completo de una provision.
- Cubrir mapeos, rechazos, consumos, regularizaciones, provisiones tardias y anulaciones.

No debe hacer:

- Ser opcional en procesos criticos.

### Analitica

Responsabilidad:

- Mostrar gasto provisionado, consumido y pendiente.
- Medir provisiones tardias, movimientos sin factura y no deducibles.
- Dar vistas por responsable, sociedad, proveedor, area y periodo.
- Alimentar metricas de cierre, alertas, eficiencia operativa y calidad de matching.
- Respetar permisos por ambito.

No debe hacer:

- Exponer informacion fuera del ambito autorizado del usuario.

## Capas de responsabilidad

```text
Experiencia operativa
  Pedido interno
  Tarjetas corporativas
  Validacion funcional de factura

Motor comun
  Provision
  Consumo
  Regularizacion
  Auditoria

Gobierno contable
  Mapeo fiscal
  Revision de impuestos
  Deducibilidad
  Periodificacion
  Integracion ERP

Analitica
  Seguimiento operativo
  Reporting de excepciones
  Vista contable analitica
```

## Contratos entre modulos

### Contrato de origen provisionable

Cualquier origen que quiera generar provision debe aportar:

- origen.
- id_origen.
- tenant.
- legal entity.
- sociedad.
- responsable.
- area.
- proveedor operativo o alias informado.
- importe.
- moneda.
- periodo o fecha de gasto.
- tipo de gasto.
- expectativa de factura.

### Contrato de consumo

Cualquier consumo de provision debe aportar:

- id_provision.
- id_factura, si existe.
- importe consumido.
- moneda.
- usuario aprobador.
- fecha de aprobacion.
- estado de revision.
- motivo si existe diferencia.

### Contrato de auditoria

Cualquier decision relevante debe aportar:

- entidad.
- id_entidad.
- accion.
- estado anterior.
- estado posterior.
- usuario.
- fecha y hora.
- motivo cuando aplique.
- origen de la accion.

### Contrato de evento de proceso

Cualquier evento explotable analiticamente debe aportar:

- tipo de evento.
- entidad.
- id_entidad.
- tenant.
- legal entity cuando aplique.
- fecha y hora.
- correlacion de proceso.
- origen del evento.

## Reglas transversales

- Ninguna factura debe contabilizarse definitivamente sin consumir una provision previa o una provision tardia auditada.
- La provision tardia existe como excepcion operativa, no como camino normal.
- La IA sugiere y explica, Administracion valida.
- El usuario de campo no debe conocer datos fiscales ni contables.
- El proveedor operativo y el proveedor fiscal son conceptos distintos.
- El `id_provision` debe viajar por pedido, factura, consumo, regularizacion y reporting.
- Toda excepcion debe ser medible.
- El tenant es frontera funcional y futura frontera de seguridad.
- Las reglas fiscales y ERP se evaluan como minimo por legal entity.

## Integraciones conceptuales

### ERP

Uso previsto:

- Consulta de proveedores fiscales.
- Consulta de sociedades y datos maestros.
- Integracion de asientos conceptuales de provision, factura, regularizacion y liquidacion.
- Confirmacion de contabilizacion.

### OCR/IA

Uso previsto:

- Extraccion de datos de factura.
- Sugerencia de proveedor fiscal.
- Sugerencia de matching factura-provision.
- Explicacion de confianza.

Limite:

- No valida fiscalmente.
- No aprueba consumos.
- No contabiliza.

### Buzon o repositorio documental

Uso previsto:

- Entrada de facturas.
- Almacenamiento de soporte.
- Vinculacion con factura, pedido, movimiento o provision.

## Decisiones pendientes de arquitectura

- Definir si el MVP empieza con pedido interno, facturas o tarjetas.
- Decidir si la primera maqueta simula ERP o usa una tabla de maestros.
- Definir tolerancias manuales para diferencias antes de regularizacion.
- Separar permisos minimos de responsable y Administracion.
- Decidir si el reporting inicial vive como vistas funcionales o dashboard prototipo.
