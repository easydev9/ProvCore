# ProvCore

Motor funcional de provisiones para conectar compromisos de gasto, facturas de proveedor y movimientos de tarjetas corporativas con trazabilidad contable completa.

ProvCore esta planteado como un proyecto de arquitectura funcional y producto financiero: adelanta el control del gasto al momento en que se compromete, separa la operativa del dato fiscal y mantiene un hilo auditable desde el pedido interno hasta la contabilizacion.

## Problema

En muchos procesos de proveedores, el control empieza cuando llega la factura. Eso provoca retraso en el reconocimiento del gasto, baja visibilidad sobre compromisos ya adquiridos, trabajo manual de provision posterior y dificultad para explicar excepciones.

ProvCore propone un flujo distinto:

```text
Compromiso de gasto -> Pedido interno -> Provision -> Factura -> Consumo -> Regularizacion -> Contabilizacion
```

La idea central es sencilla: ninguna factura debe contabilizarse definitivamente sin consumir una provision previa o una provision tardia auditada.

## Principios

- Ninguna factura debe contabilizarse definitivamente sin consumir una provision previa o una provision tardia auditada.
- La IA sugiere, Administracion valida.
- El usuario de campo no debe conocer datos fiscales ni contables.
- El proveedor operativo y el proveedor fiscal son conceptos separados.
- El `id_provision` debe viajar por todo el ciclo.
- Toda excepcion debe quedar auditada.
- La provision tardia existe para no bloquear la operacion, pero debe medirse como incumplimiento del proceso.

## Alcance funcional

ProvCore cubre los siguientes bloques:

- Pedido interno o compromiso de gasto.
- Motor comun de provisiones.
- Mapeo proveedor operativo -> proveedor fiscal.
- Integracion funcional con facturas de proveedor.
- Integracion funcional con tarjetas corporativas.
- Consumo total, parcial y N a N entre facturas y provisiones.
- Regularizaciones por importe, impuestos, divisa, periodificacion o ausencia de factura.
- Auditoria de estados, decisiones y excepciones.
- Analitica por responsable, proveedor, sociedad, area y periodo.

## Gobierno del proceso

ProvCore diferencia tres responsabilidades:

```text
Responsable operativo
  Informa el compromiso de gasto y valida que la factura corresponde al servicio.

IA / OCR
  Extrae datos, sugiere proveedor fiscal y propone matching factura-provision.

Administracion
  Valida proveedor fiscal, datos contables, impuestos, consumos, regularizaciones y contabilizacion.
```

La IA no es fuente de verdad contable. El gobierno final recae en Administracion y en los datos maestros del ERP.

## Casos clave

- Factura que consume una provision.
- Factura que consume varias provisiones.
- Provision consumida por varias facturas.
- Factura sin provision previa con provision tardia auditada.
- Proveedor operativo con confianza baja de matching fiscal.
- Movimiento de tarjeta con factura.
- Movimiento de tarjeta sin factura con motivo obligatorio.
- Regularizacion por diferencia de importe, impuestos o divisa.
- Periodificacion de gastos entre periodos.

## Roadmap MVP

El MVP recomendado para portfolio se centra en:

1. Crear pedido interno y generar `id_provision`.
2. Registrar proveedor operativo y simular mapeo fiscal.
3. Crear provision abierta.
4. Registrar factura.
5. Buscar provisiones compatibles.
6. Aprobar consumo total o parcial.
7. Gestionar factura sin provision mediante provision tardia auditada.
8. Mostrar analitica minima de provisionado, consumido, pendiente y excepciones.

El detalle completo esta en [Roadmap MVP](docs/roadmap_mvp.md).

## Documentacion

| Documento | Contenido |
| --- | --- |
| [Contexto funcional](docs/contexto_funcional.md) | Vision del problema, principios y flujos principales. |
| [Especificacion funcional inicial](docs/especificacion_funcional_inicial_provisiones.md) | Documento funcional base del motor de provisiones. |
| [Arquitectura funcional](docs/arquitectura_funcional.md) | Modulos, responsabilidades, contratos e integraciones conceptuales. |
| [Modelo de datos inicial](docs/modelo_datos_inicial.md) | Entidades, relaciones, campos funcionales e indices sugeridos. |
| [Estados por entidad](docs/estados_entidades.md) | Ciclos de vida de pedido, provision, factura, mapeo y regularizacion. |
| [Casos de uso detallados](docs/casos_uso_detallados.md) | Casos principales con actores, precondiciones, flujos y excepciones. |
| [Diagramas de flujo](docs/diagramas_flujo.md) | Diagramas Mermaid de arquitectura, flujos, estados y ERD funcional. |
| [Roadmap MVP](docs/roadmap_mvp.md) | Fases recomendadas para convertir la documentacion en prototipo. |
| [Backlog de issues inicial](docs/issues_backlog.md) | Backlog accionable por epicas y prioridades. |
| [Backlog inicial](docs/backlog_inicial.md) | Vision resumida por epicas. |

## Estado

Proyecto en fase de definicion funcional y arquitectura inicial.

El foco actual es consolidar la documentacion portfolio-friendly y preparar la conversion del backlog en un prototipo navegable del flujo principal.

## Valor profesional

Este repositorio documenta un caso funcional completo de automatizacion financiera: captura temprana del compromiso de gasto, gobierno contable por Administracion, sugerencias asistidas por IA, integracion con facturas y tarjetas, excepciones auditadas, modelo de datos, estados, diagramas y roadmap MVP.

El proyecto esta escrito sin nombres internos sensibles y puede usarse como muestra de analisis funcional, arquitectura de producto, criterio contable-operativo y diseño de procesos auditables.
