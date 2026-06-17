# Provisioning Engine

Functional design for a provisioning engine that connects internal spend requests, supplier invoices and corporate card movements with full accounting traceability.

## Objetivo

El sistema busca que todo gasto pase por una provision antes de impactar definitivamente en la cuenta de resultados.

El flujo esperado es:

```text
Compromiso de gasto -> Pedido interno -> Provision -> Factura -> Consumo -> Regularizacion -> Contabilizacion
```

## Principios

- Todo gasto debe pasar por provision.
- La IA sugiere, Administracion valida.
- El usuario de campo no debe conocer datos fiscales ni contables.
- El ID de provision debe viajar por todo el ciclo.
- Toda excepcion debe quedar auditada.

## Modulos previstos

- Pedido interno / compromiso de gasto.
- Motor comun de provisiones.
- Mapeo proveedor operativo -> proveedor fiscal.
- Integracion con modulo de facturas de proveedor.
- Integracion con modulo de tarjetas corporativas.
- Regularizaciones y periodificaciones.
- Analitica de proveedores y provisiones.
- Auditoria y reporting.

## Documentacion

- [Especificacion funcional inicial](docs/especificacion_funcional_inicial_provisiones.md)
- [Contexto funcional](docs/contexto_funcional.md)
- [Modelo de datos inicial](docs/modelo_datos_inicial.md)
- [Estados por entidad](docs/estados_entidades.md)
- [Casos de uso detallados](docs/casos_uso_detallados.md)
- [Diagramas de flujo](docs/diagramas_flujo.md)
- [Backlog de issues inicial](docs/issues_backlog.md)
- [Backlog inicial](docs/backlog_inicial.md)

## Estado

Proyecto en fase de definicion funcional y arquitectura inicial.

El foco actual es consolidar el modelo comun de provisiones, los estados de ciclo de vida, los casos de uso y un backlog accionable para un futuro prototipo.
