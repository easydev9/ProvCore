# Especificacion funcional inicial - Motor de provisiones

## 1. Objetivo

Diseñar un sistema que permita que ninguna factura de proveedor se contabilice definitivamente sin consumir una provision previa o una provision tardia auditada, garantizando trazabilidad desde el momento en que nace el compromiso de gasto hasta la recepcion de factura, consumo de provision, regularizacion y contabilizacion.

El sistema cubre dos circuitos principales:

- provisiones de proveedores originadas desde pedidos internos o compromisos de gasto.
- provisiones asociadas a movimientos de tarjetas corporativas.

Ambos circuitos comparten un motor comun de provisiones, pero mantienen origenes, reglas y necesidades especificas.

## 2. Principios rectores

### 2.1 Todo pasa por provision

Ninguna factura debe contabilizarse definitivamente sin consumir una provision previa o una provision tardia auditada.

Flujo esperado:

```text
Compromiso de gasto -> Pedido interno -> Provision -> Factura -> Consumo de provision -> Regularizacion -> Contabilizacion
```

Cuando llegue una factura sin provision previa, el sistema permitira crear una provision tardia, consumirla inmediatamente y dejar trazabilidad obligatoria del motivo. Este caso debe tratarse como excepcion.

### 2.2 La IA sugiere, Administracion gobierna

La IA sera motor de sugerencia, no fuente de verdad contable.

La fuente de verdad sobre proveedor fiscal, NIF/VAT, codigo de proveedor ERP, dimension financiera, cuenta contable y tratamiento fiscal recaera sobre Administracion y los datos maestros del ERP.

### 2.3 El usuario de campo no debe conocer datos fiscales

El responsable que contrata un servicio debe poder notificarlo de forma sencilla, sin conocer:

- razon social fiscal exacta.
- NIF/VAT.
- codigo de proveedor ERP.
- cuentas contables.
- dimension financiera.
- tratamiento fiscal completo.

El sistema debe permitirle informar datos operativos: proveedor conocido, descripcion, importe, moneda, sociedad, area, periodo y tipo de gasto.

### 2.4 Auditoria completa

Toda accion relevante debe quedar auditada:

- usuario.
- fecha y hora.
- accion.
- valor anterior.
- valor nuevo.
- motivo.
- origen de la accion.
- estado anterior.
- estado posterior.

Esto aplica especialmente a rechazos, reasignaciones, provisiones tardias, cambios de proveedor, ajustes, regularizaciones, cambios de periodificacion y consumos de provision.

## 3. Modulos funcionales

### 3.1 Pedido interno / compromiso de gasto

Modulo donde el responsable notifica que ha contratado o comprometido un servicio.

Su finalidad es generar una provision antes de recibir la factura.

Datos minimos:

- sociedad.
- area / centro de coste / responsable.
- proveedor conocido por el usuario.
- descripcion del servicio.
- tipo de gasto.
- tipo especifico de servicio.
- importe total estimado.
- moneda.
- fecha esperada de factura.
- periodo de servicio, si aplica.
- si espera factura.
- si es recurrente.
- documentacion soporte opcional.

Resultado:

```text
Pedido interno creado
ID_PROVISION generado
Provision pendiente de validacion o integracion
```

### 3.2 Motor comun de provisiones

Componente transversal encargado de:

- crear provisiones.
- mantener estados.
- preparar asientos.
- consumir provisiones.
- gestionar consumos parciales.
- permitir consumo de varias provisiones por una factura.
- permitir consumo de una provision por varias facturas.
- calcular diferencias.
- generar regularizaciones.
- mantener trazabilidad.

El motor no debe depender del origen operativo. Debe trabajar con un contrato comun.

Ejemplo conceptual:

```text
Provisionable
- origen
- sociedad
- proveedor operativo
- proveedor fiscal
- moneda
- importe provisionado
- importe consumido
- importe pendiente
- estado
- reglas de consumo
- reglas de regularizacion
```

Implementaciones previstas:

```text
Pedido interno de proveedor
Movimiento de tarjeta corporativa
Provision tardia desde factura
Suscripcion recurrente
```

### 3.3 Modulo de facturas de proveedor

El modulo de facturas sera maestro de:

- documento de factura.
- OCR/IA de factura.
- proveedor fiscal detectado.
- validacion de factura.
- asiento de factura.
- estado de contabilizacion de factura.

Al subir una factura, el sistema debera:

- ejecutar OCR/IA.
- detectar sociedad cliente.
- extraer VAT/NIF de cliente y proveedor.
- consultar datos maestros del ERP.
- identificar proveedor fiscal para esa sociedad.
- identificar validadores/responsables.
- buscar provisiones abiertas compatibles.
- sugerir consumo de provision.
- informar al validador si existe o no provision previa.

Despues de validada la factura, Administracion revisara:

- datos contables.
- proveedor fiscal.
- cuentas.
- impuestos.
- deducibilidad.
- periodificacion.
- provisiones sugeridas.
- consumo propuesto.
- ajustes o regularizaciones.

La factura pasara a estado `Registrada` cuando este lista para integracion ERP. Tras integracion, pasara a `Contabilizada`.

### 3.4 Modulo de tarjetas corporativas

El modulo de tarjetas corporativas mantiene su propio origen operativo: el movimiento de tarjeta.

Cuando nace un movimiento:

- se genera movimiento.
- el usuario informa gasto.
- se crea provision.
- se integra provision contable.
- se solicitan facturas mediante recordatorios.
- se permite marcar sin factura con motivo obligatorio.
- se asocian facturas cuando lleguen.
- se regulariza por impuestos/base imponible si procede.
- se regulariza por divisa contra liquidacion bancaria si procede.
- se cierra con la liquidacion de la tarjeta.

Las provisiones de tarjetas deben salir del mismo motor comun, pero se notificaran y gestionaran desde su apartado por sus necesidades especificas.


### 3.5 Analitica de proveedores y provisiones

El modulo de facturas debe incluir una capa de analitica para que cada responsable pueda consultar en todo momento la situacion de sus proveedores, provisiones y consumos asociados.

La analitica debe tener tres niveles principales:

```text
Vista general
Vista detallada
Vista contable analitica
```

La vista general debe permitir entender rapidamente:

- proveedores asociados al responsable.
- provisiones abiertas.
- provisiones consumidas.
- importe provisionado.
- importe consumido.
- importe pendiente.
- facturas recibidas.
- facturas pendientes de validar.
- consumos con diferencias.
- provisiones tardias.
- movimientos sin factura.
- importes no deducibles o pendientes de determinar.

La vista detallada debe permitir bajar al nivel de cada proveedor, pedido interno, provision, factura y consumo.

Debe mostrar:

- ID_PROVISION.
- proveedor operativo.
- proveedor fiscal validado.
- responsable.
- sociedad.
- area.
- tipo de gasto.
- periodo.
- moneda.
- importe provisionado.
- importe consumido.
- importe pendiente.
- facturas asociadas.
- regularizaciones asociadas.
- estado documental.
- estado de provision.
- estado contable.
- comentarios y auditoria relevante.

La vista contable analitica debe estar orientada a Administracion y responsables con permisos ampliados.

Debe permitir consultar:

- gasto provisionado por periodo.
- gasto consumido por factura.
- gasto pendiente de recibir factura.
- diferencias entre provision y factura.
- diferencias por divisa.
- periodificaciones.
- importes deducibles.
- importes no deducibles.
- movimientos sin factura.
- provisiones tardias.
- regularizaciones pendientes.
- regularizaciones integradas.

La analitica debe respetar permisos por rol. Un responsable solo debe consultar proveedores, pedidos, provisiones y facturas asociadas a su ambito. Administracion podra consultar toda la informacion con filtros globales.

Filtros recomendados:

- responsable.
- proveedor operativo.
- proveedor fiscal.
- sociedad.
- area.
- periodo.
- estado de provision.
- estado de factura.
- estado de regularizacion.
- moneda.
- tipo de gasto.
- deducibilidad.
- origen operativo.

## 4. Mapeo proveedor operativo - proveedor fiscal

El usuario puede informar un proveedor por su nombre comercial o habitual:

```text
Proveedor de movilidad
```

Pero fiscalmente puede corresponder a una razon social distinta:

```text
Sociedad fiscal del proveedor de movilidad
```

Por tanto, el sistema debe crear una capa de mapeo:

```text
Proveedor operativo / alias -> proveedor fiscal ERP
```

Campos recomendados:

- alias informado por usuario.
- proveedor operativo normalizado.
- proveedor fiscal sugerido.
- proveedor fiscal validado.
- NIF/VAT.
- codigo proveedor ERP.
- sociedad.
- pais proveedor.
- confianza del matching.
- origen de la sugerencia.
- estado de validacion.
- validado por.
- fecha de validacion.

Estados posibles:

```text
PendienteMapeo
SugeridoPorIA
MapeadoPorHistorico
ValidadoAdministracion
ConfirmadoPorFactura
Rechazado
Corregido
```

Fuentes de confianza:

- NIF/VAT exacto.
- codigo ERP.
- alias previamente validado.
- historico de facturas.
- similitud semantica.
- categoria de gasto.
- mismo responsable o area.
- documentacion adjunta.
- recurrencia del proveedor.

Regla de gobierno:

```text
La IA puede sugerir el proveedor fiscal, pero Administracion debe validar el mapeo antes de convertirlo en verdad contable.
```

## 5. Flujo happy path - proveedor normal

```text
1. Responsable contrata servicio.
2. Crea pedido interno.
3. Informa proveedor conocido, importe, moneda, sociedad, tipo de gasto y periodo.
4. Sistema genera ID_PROVISION.
5. IA sugiere proveedor fiscal si puede.
6. Administracion valida proveedor fiscal/cuenta/dimension si falta.
7. Se integra asiento de provision.
8. Llega factura a buzon.
9. Administracion sube factura al modulo de facturas.
10. OCR/IA extrae datos.
11. El sistema detecta proveedor fiscal y busca provisiones abiertas.
12. Sistema sugiere consumir ID_PROVISION.
13. Responsable valida que la factura corresponde al servicio.
14. Administracion revisa contabilidad, impuestos y consumo.
15. Factura guarda ID_PROVISION.
16. Se registra factura.
17. Integracion ERP procesa las facturas registradas.
18. Factura queda contabilizada.
19. Provision queda consumida/cerrada o parcialmente abierta.
```

## 6. Flujo excepcion - factura sin provision previa

```text
1. Llega factura.
2. OCR/IA detecta proveedor, sociedad e importes.
3. El sistema busca provisiones abiertas.
4. No encuentra provision compatible.
5. Se marca como SinProvisionPrevia.
6. Responsable debe justificar por que no existia pedido interno.
7. Administracion crea provision tardia.
8. La provision tardia se consume inmediatamente con la factura.
9. Queda trazabilidad completa.
10. La factura puede pasar a registrada.
```

Datos obligatorios:

- motivo de provision tardia.
- responsable.
- usuario que crea.
- factura origen.
- fecha/hora.
- proveedor.
- sociedad.
- importe.
- comentario obligatorio.

## 7. Casos especiales a contemplar

### 7.1 Confianza baja de proveedor

Cuando el sistema no pueda mapear con seguridad el proveedor operativo contra proveedor fiscal, debera:

- mostrar candidatos.
- explicar origen de la sugerencia.
- bloquear integracion contable automatica.
- enviar a revision de Administracion.
- guardar decision final para mejorar futuros casos.

### 7.2 Una factura consume varias provisiones

Una factura puede agrupar varios servicios, pedidos o movimientos.

El sistema debe permitir:

- seleccionar varias provisiones.
- comparar suma provisionada contra total/base factura.
- generar consumos individuales.
- calcular diferencias.
- guardar todas las relaciones factura-provision.

### 7.3 Una provision se consume con varias facturas

Debe permitirse consumo parcial.

Campos:

- importe provisionado.
- importe consumido.
- importe pendiente.
- porcentaje consumido.
- estado de provision.

### 7.4 Periodificacion

Cuando la factura cubra varios periodos, el modulo de facturas debera sugerir periodificacion.

Administracion podra:

- aceptar sugerencia.
- modificarla.
- no periodificar.
- periodificar manualmente.

### 7.5 No deducible / sin factura

El sistema debe permitir extraer analitica fiscal.

Clasificaciones:

- deducible.
- no deducible.
- parcialmente deducible.
- sin factura.
- pendiente de determinar.

Datos necesarios:

- motivo.
- responsable.
- area.
- proveedor.
- importe.
- base.
- impuestos.
- sociedad.
- periodo.
- ID_PROVISION.
- ID_FACTURA si existe.

### 7.6 Divisa

El usuario informara moneda al crear pedido/movimiento.

El sistema aceptara temporalmente diferencias por tipo de cambio y regularizara posteriormente segun:

- factura.
- tipo de cambio ERP.
- liquidacion bancaria en caso de tarjeta.
- documento soporte.

### 7.7 Tarjeta corporativa con factura agrupada

Una factura puede justificar varios movimientos de tarjeta.

El sistema debe permitir:

- asociar una factura a N movimientos.
- consumir N provisiones de tarjeta.
- comparar total factura contra suma movimientos.
- detectar diferencias.
- regularizar por impuestos/base.
- regularizar por divisa en liquidacion.

## 8. Estados recomendados

### 8.1 Pedido interno

```text
Borrador
Enviado
PendienteMapeoProveedor
PendienteValidacionAdministracion
ProvisionPendienteIntegracion
ProvisionIntegrada
ConsumidoParcialmente
ConsumidoTotalmente
Cerrado
Cancelado
```

### 8.2 Provision

```text
Creada
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

### 8.3 Factura

```text
Subida
OCRProcesado
PendienteValidacion1
PendienteValidacion2
Rechazada
Validada
PendienteRevisionContable
Registrada
Contabilizada
```

### 8.4 Relacion factura-provision

```text
Sugerida
Seleccionada
PendienteRevision
Aprobada
Integrada
Rechazada
Anulada
```

## 9. Asientos conceptuales

Los asientos se documentan de forma conceptual para evitar acoplar la especificacion a un plan contable concreto.

### 9.1 Provision inicial

```text
Debe: cuenta de gasto
Haber: cuenta de provision
```

### 9.2 Recepcion/contabilizacion de factura

```text
Debe: cuenta de provision
Haber: cuenta de proveedor
```

### 9.3 Regularizacion

Cuando exista diferencia entre provision y realidad de factura/liquidacion:

```text
Debe/Haber: cuenta de gasto correspondiente
Contra: cuenta de provision
```

El sentido debe depender del signo de la diferencia.

### 9.4 Liquidacion de tarjeta corporativa

```text
Debe: cuenta de proveedor
Haber: cuenta puente de tarjeta corporativa
```

## 10. Modelo de datos inicial

Entidades principales:

- pedido_interno.
- provision.
- factura.
- factura_provision.
- proveedor_operativo.
- proveedor_fiscal.
- mapeo_proveedor.
- movimiento_tarjeta.
- liquidacion_tarjeta.
- regularizacion.
- auditoria_estado.
- comentario.
- adjunto.
- regla_contable.
- regla_fiscal.
- periodificacion.

Relaciones clave:

```text
pedido_interno 1 -> 1 provision
movimiento_tarjeta 1 -> 1 provision
factura N -> N provision
proveedor_operativo N -> 1 proveedor_fiscal validado
provision N -> N regularizacion
factura 1 -> N comentarios/auditoria
responsable 1 -> N proveedores/provisiones visibles
proveedor_fiscal 1 -> N vistas analiticas por periodo
```

## 11. MVP recomendado

Primera fase:

- una sociedad cliente como alcance inicial.
- proveedores nacionales, intracomunitarios e internacionales.
- moneda informada desde pedido/movimiento.
- pedido interno con generacion de provision.
- busqueda de provisiones en el modulo de facturas.
- consumo total/parcial.
- factura contra varias provisiones.
- provision tardia auditada.
- mapeo proveedor operativo/fiscal con confianza.
- validacion final por Administracion.
- reporting de no deducibles/sin factura.
- auditoria completa.

No incluir inicialmente:

- reglas fiscales completas de multiples jurisdicciones.
- automatizacion contable sin revision.
- aprendizaje automatico que valide solo proveedores fiscales.
- tolerancias automaticas.

## 12. Frases de alineamiento

```text
Todo compromiso de gasto debe notificarse antes de recibir la factura, generando una provision con ID unico.
```

```text
Ninguna factura debe contabilizarse definitivamente sin consumir una provision previa o una provision tardia auditada.
```

```text
Si no existe provision previa, se crea una provision tardia como excepcion auditada.
```

```text
La IA sugiere. Administracion valida.
```

```text
El usuario de campo no debe conocer datos fiscales ni contables.
```

```text
Los distintos origenes operativos comparten motor de provisiones, pero mantienen flujos especificos.
```
