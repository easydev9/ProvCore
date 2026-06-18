# ProvCore

Motor funcional de provisiones para conectar compromisos de gasto, facturas de proveedor y movimientos de tarjetas corporativas con trazabilidad contable completa.

## Objetivo

ProvCore busca que todo gasto pase por provision antes de impactar definitivamente en la cuenta de resultados.

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
- [Arquitectura funcional](docs/arquitectura_funcional.md)
- [Modelo de datos inicial](docs/modelo_datos_inicial.md)
- [Estados por entidad](docs/estados_entidades.md)
- [Casos de uso detallados](docs/casos_uso_detallados.md)
- [Diagramas de flujo](docs/diagramas_flujo.md)
- [Roadmap MVP](docs/roadmap_mvp.md)
- [Backlog de issues inicial](docs/issues_backlog.md)
- [Backlog inicial](docs/backlog_inicial.md)

## Estado

Proyecto en fase de definicion funcional y arquitectura inicial.

El foco actual es consolidar el modelo comun de provisiones, los estados de ciclo de vida, los casos de uso y un backlog accionable para un futuro prototipo.

## Valor profesional

Este repositorio documenta un caso funcional completo de automatizacion financiera: captura temprana del compromiso de gasto, gobierno contable por Administracion, sugerencias asistidas por IA, integracion con facturas y tarjetas, excepciones auditadas y analitica de seguimiento.
