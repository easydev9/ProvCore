# Vision estrategica de producto

## Objetivo

Definir la vision final de ProvCore mas alla del MVP tecnico inicial.

ProvCore no debe entenderse solo como un gestor de provisiones. Su objetivo estrategico es convertirse en una plataforma SaaS para controlar, auditar y explotar el ciclo completo del gasto provisionado.

## Vision final

ProvCore aspira a cubrir este flujo completo:

```text
movimiento provisionable
-> identificacion de origen
-> provision
-> proveedor fiscal y ERP
-> factura
-> consumo
-> regularizacion
-> auditoria
-> eventos
-> metricas
-> alertas
-> control de cierre
-> forecast y presupuesto
```

El valor final no esta solo en crear provisiones, sino en convertir el proceso operativo en informacion estructurada, auditable y explotable.

## Principio central

Todo gira alrededor del movimiento provisionable.

Un movimiento provisionable es cualquier evento operativo capaz de generar una provision bajo un contrato comun.

Ejemplos:

- pedido interno.
- movimiento de tarjeta.
- factura sin provision previa.
- suscripcion recurrente.
- otro origen futuro.

El motor debe identificar el origen del movimiento y aplicar reglas comunes. Cada origen puede implementar su propia forma de obtener datos, validar campos o integrarse, pero el motor no debe depender de la logica interna de cada origen.

## Plataforma SaaS

ProvCore se plantea como una solucion SaaS conectada a sistemas ERP de clientes.

Conceptos clave:

- `tenant`: cliente, grupo empresarial o unidad aislada dentro del SaaS.
- `legal_entity`: sociedad juridica dentro del tenant.
- `ERP`: sistema externo donde viven maestros, proveedores, sociedades, facturas o integraciones contables.

Ejemplo:

```text
Tenant: Grupo empresarial
  Legal entity: Sociedad Espana
  Legal entity: Sociedad Francia
  Legal entity: Sociedad Alemania
```

El MVP puede operar con un tenant inicial, pero el modelo debe nacer preparado para multiples sociedades y para una futura separacion estricta entre tenants.

## Routing multi-sociedad

En una version SaaS o multipais, ProvCore debe poder enrutar peticiones hacia la infraestructura autorizada para cada contexto.

El criterio principal no es solo tecnico. Antes de ejecutar una operacion, el sistema debe resolver:

- tenant.
- legal entity.
- permisos.
- pais.
- residencia del dato.
- ERP asociado.
- tipo de operacion.

Despues se aplica balanceo tecnico dentro del pool autorizado.

Esto permite soportar distintos modelos de despliegue:

- infraestructura comun para MVP.
- pools por region.
- pools por grupo de sociedades.
- pools dedicados para sociedades criticas.
- integraciones ERP diferentes por legal entity.

## Integracion ERP

ProvCore no debe acoplar su dominio al ERP.

La integracion debe hacerse mediante puertos y adaptadores:

```text
application
  -> ERPIntegrationPort
    -> D365FOAdapter
```

D365 Finance & Operations puede ser ERP de referencia y entorno real de validacion, pero no debe sustituir al dominio de ProvCore.

Regla:

```text
El ERP valida e integra. ProvCore gobierna su dominio.
```

## Alta de proveedor fiscal

El flujo final debe contemplar casos donde una factura llega con un proveedor fiscal que no existe en el ERP para una sociedad.

Flujo esperado:

```text
OCR o carga factura
-> deteccion proveedor fiscal
-> comprobacion proveedor en ERP para la legal entity
-> si no existe, solicitud de alta proveedor
-> confirmacion ERP satisfactoria
-> continuacion del registro de factura
```

La factura no debe continuar hacia registro definitivo si el proveedor fiscal requerido no existe o no esta validado para la sociedad correspondiente.

En MVP se puede simular la comprobacion ERP. La arquitectura debe dejar preparado el puerto de integracion.

## Grupos compradores y responsabilidad por proveedor

Los proveedores pueden estar asociados a grupos compradores o grupos responsables.

Estos grupos pueden venir de:

- ERP.
- configuracion interna de ProvCore.
- carga manual.
- sincronizacion externa.

ProvCore debe modelarlos como concepto funcional porque son necesarios para:

- alertas.
- control de cierre.
- seguimiento de movimientos abiertos.
- responsabilidad operativa.
- escalado de excepciones.

La fuente de verdad puede variar por tenant.

## Control de cierre y alertas

ProvCore debe evolucionar hacia una capa de control operativo de cierre.

Casos esperados:

- proveedores con movimientos abiertos.
- provisiones pendientes de consumir.
- facturas pendientes de validar.
- proveedores pendientes de alta ERP.
- movimientos de tarjeta sin factura.
- regularizaciones pendientes.
- excepciones no resueltas.

El sistema debe poder generar alertas para usuarios y grupos responsables en fechas clave.

Ejemplo:

```text
Proveedor con movimientos abiertos
-> grupo comprador responsable
-> usuarios del grupo
-> alerta antes del cierre
-> seguimiento hasta resolucion
```

## Eventos, auditoria y metricas

Todo cambio relevante debe generar informacion estructurada.

La informacion sirve para:

- auditoria.
- trazabilidad.
- analitica operativa.
- eficiencia administrativa.
- calidad de matching.
- control de cierre.
- forecast.
- presupuestacion futura.

Eventos relevantes:

- movimiento provisionable identificado.
- provision creada.
- proveedor no encontrado en ERP.
- solicitud de alta proveedor enviada.
- factura bloqueada.
- factura desbloqueada.
- matching sugerido.
- matching aceptado o rechazado.
- consumo aprobado.
- provision tardia creada.
- regularizacion generada.
- alerta creada.
- alerta resuelta.

No se implementara event sourcing en el MVP. El estado principal vivira en tablas transaccionales y los eventos serviran para trazabilidad y analitica.

## Matching, confianza e IA

La IA y las reglas pueden sugerir relaciones.

Ejemplos:

- proveedor operativo con proveedor fiscal.
- factura con provision.
- factura con responsable.
- factura con movimiento de tarjeta.
- proveedor con grupo comprador.

Cada sugerencia debe guardar:

- tipo de matching.
- score de confianza.
- evidencias usadas.
- explicacion.
- umbral aplicado.
- decision final.
- usuario validador.
- fecha de validacion.

La IA sugiere. Administracion valida.

El valor futuro esta en analizar que sugerencias funcionan, cuales fallan y que senales son mas fiables.

## Analitica operativa

ProvCore debe permitir medir:

- porcentaje de facturas con provision previa.
- porcentaje de provisiones tardias.
- tiempo medio de alta proveedor.
- tiempo medio de factura recibida a registrada.
- tiempo medio de provision abierta a consumida.
- provisiones abiertas por antiguedad.
- excepciones por sociedad, pais, area y proveedor.
- tasa de aceptacion de sugerencias.
- tasa de rechazo de matching.
- regularizaciones por causa.
- alertas vencidas por grupo responsable.

Estas metricas deben poder agregarse por tenant, legal entity, pais, proveedor, area, grupo comprador y periodo.

## Presupuesto y forecast

ProvCore puede evolucionar hacia presupuestacion y forecast.

La diferencia frente a un ERP tradicional es que ProvCore captura informacion antes de la factura:

```text
compromiso operativo
-> provision
-> consumo real
-> desviacion
```

Esto permite:

- presupuesto anual basado en compromisos reales.
- forecast dinamico por periodo.
- deteccion de recurrencias.
- comparacion entre presupuesto, provisionado, consumido y pendiente.
- simulaciones por proveedor, sociedad, pais o tipo de gasto.

No entra en el MVP inicial, pero los datos deben capturarse de forma que esta evolucion sea posible.

## Multipais

La vision final contempla multipais.

El modelo debe poder representar:

- pais del tenant o grupo.
- pais de la legal entity.
- pais del proveedor fiscal.
- moneda.
- fiscalidad local.
- periodos contables.
- reglas de deducibilidad.
- formatos de identificacion fiscal.
- integraciones ERP por sociedad.

El MVP no implementara reglas fiscales multipais completas, pero no debe cerrar el modelo a una unica jurisdiccion.

## Fuera de alcance del MVP inicial

No forman parte del primer desarrollo:

- integracion real con D365 F&O.
- X++.
- OCR productivo.
- machine learning productivo.
- budgeting completo.
- forecast automatico.
- multi-tenant productivo completo.
- motor de alertas avanzado.
- conciliacion bancaria completa.

## Implicaciones para el MVP

Aunque el MVP sea acotado, debe capturar desde el inicio:

- tenant conceptual.
- legal entity.
- origen del movimiento provisionable.
- estado anterior y estado posterior.
- usuario y rol.
- proveedor operativo.
- proveedor fiscal.
- importe, moneda y periodo.
- eventos de auditoria.
- sugerencias y confianza cuando aplique.
- excepciones y motivos.

Regla final:

```text
No implementamos toda la vision ahora. Pero el MVP no debe impedir llegar a ella.
```
