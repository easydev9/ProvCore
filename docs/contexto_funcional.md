# Contexto funcional del proyecto

## Proposito

El proyecto define un motor de provisiones para conectar compromisos de gasto, facturas de proveedor y movimientos de tarjetas corporativas con trazabilidad contable completa.

La idea central es que todo gasto nazca como provision antes de impactar en la cuenta de resultados.

## Problema que resuelve

En muchos procesos de proveedores, la gestion empieza cuando llega la factura. Esto provoca que el gasto se registre tarde, que la responsabilidad operativa sea difusa y que las provisiones dependan de trabajo manual posterior.

El objetivo es adelantar el control al momento en que el responsable contrata o compromete el servicio.

## Principios de diseño

- Todo gasto debe pasar por provision.
- El responsable notifica el compromiso de gasto de forma sencilla.
- El usuario de campo no debe conocer datos fiscales ni contables.
- La IA sugiere. Administracion valida.
- La fuente de verdad contable es Administracion y el ERP.
- Toda excepcion debe quedar auditada.
- El ID de provision debe viajar por todo el ciclo.

## Flujo principal

```text
Responsable contrata servicio
-> crea pedido interno
-> el sistema genera ID_PROVISION
-> Administracion valida datos contables si falta informacion
-> se integra la provision
-> llega factura
-> el modulo de facturas busca provisiones compatibles
-> se consume una o varias provisiones
-> se regularizan diferencias
-> se contabiliza factura
```

## Flujo excepcional

Si llega una factura sin provision previa, el sistema permite crear una provision tardia.

Esa provision se consume inmediatamente con la factura y requiere:

- motivo obligatorio.
- responsable asociado.
- usuario que registra la excepcion.
- fecha y hora.
- factura origen.
- auditoria completa.

Este flujo existe para no bloquear la operacion, pero debe servir para medir incumplimientos del proceso.

## Motor comun

El sistema debe tener un motor comun de provisiones con implementaciones por origen.

Implementaciones previstas:

```text
PedidoInternoProveedor
MovimientoTarjetaCorporativa
ProvisionTardiaDesdeFactura
SuscripcionRecurrente
```

Todas comparten un contrato funcional:

- pueden generar provision.
- tienen responsable.
- tienen sociedad.
- tienen importe y moneda.
- pueden asociarse a proveedor operativo.
- pueden mapearse a proveedor fiscal.
- pueden ser consumidas por facturas.
- pueden generar regularizaciones.
- deben tener auditoria.

## Mapeo proveedor operativo y proveedor fiscal

El responsable puede conocer al proveedor por nombre comercial, no por razon social fiscal.

El sistema debe permitir mapear:

```text
Alias operativo -> proveedor fiscal ERP
```

La IA puede sugerir candidatos con nivel de confianza usando alias, historico, similitud semantica, categoria de gasto y datos de factura. Administracion valida el mapeo antes de convertirlo en fuente de verdad.

## Modulo de facturas

El modulo de facturas es maestro del documento, OCR, proveedor fiscal detectado, validacion funcional, asiento de factura y estado de contabilizacion.

Al subir una factura debe:

- extraer datos por OCR/IA.
- consultar datos maestros del ERP.
- detectar proveedor fiscal.
- identificar responsables validadores.
- buscar provisiones abiertas compatibles.
- sugerir consumo de provision.
- informar si no existe provision previa.

## Modulo de tarjetas corporativas

Los movimientos de tarjeta corporativa tambien generan provisiones, pero se notifican desde su modulo operativo.

Debe cubrir:

- movimientos con factura.
- movimientos sin factura con motivo obligatorio.
- facturas agrupadas para varios movimientos.
- regularizaciones por impuestos/base.
- regularizaciones por divisa.
- conciliacion contra liquidacion bancaria.

## Analitica

El sistema necesita analitica para responsables y Administracion.

Vistas principales:

- vista general por responsable, proveedor, area, sociedad y periodo.
- vista detallada por pedido interno, provision, factura, consumo y regularizacion.
- vista contable analitica con gasto provisionado, consumido, pendiente, no deducible, sin factura y regularizaciones.

Los permisos deben limitar a cada responsable a su ambito. Administracion puede consultar informacion global.

## Casos importantes

- factura que consume una provision.
- factura que consume varias provisiones.
- provision consumida por varias facturas.
- factura sin provision previa.
- proveedor con confianza baja de matching.
- proveedor extranjero.
- factura en divisa.
- gastos no deducibles.
- movimientos sin factura.
- periodificacion.
- suscripciones recurrentes.

## Estado actual del repo

El repo contiene:

- README con descripcion general.
- especificacion funcional inicial.
- arquitectura funcional.
- modelo de datos inicial.
- estados por entidad.
- casos de uso detallados.
- diagramas de flujo.
- roadmap MVP.
- backlog de issues.
- backlog inicial.
- contexto funcional para futuros hilos.

## Proximos pasos sugeridos

1. Validar con Administracion el modelo de datos inicial.
2. Revisar estados definitivos por entidad y transiciones bloqueantes.
3. Priorizar los casos de uso detallados para MVP.
4. Convertir el backlog de issues en tareas de prototipo.
5. Decidir tecnologia para un prototipo.
6. Construir una maqueta funcional del flujo principal.
7. Probar el circuito de excepcion de provision tardia.
