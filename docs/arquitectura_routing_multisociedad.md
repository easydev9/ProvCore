# Arquitectura de routing multi-sociedad

## Objetivo

Definir como debe enrutar ProvCore peticiones en un escenario con multiples tenants, sociedades, ERPs e infraestructuras posibles.

Este documento no define todavia una configuracion productiva concreta. Define el modelo conceptual para que el backend y las futuras integraciones no nazcan acopladas a una unica sociedad o a un unico servidor.

## Principio

```text
Routing funcional primero. Balanceo tecnico despues.
```

El routing funcional responde a esta pregunta:

```text
Que contexto de negocio tiene esta peticion y que infraestructura esta autorizada para procesarla?
```

El balanceo tecnico responde despues:

```text
Dentro del pool autorizado, que instancia esta en mejores condiciones para atenderla?
```

## Flujo esperado

```text
Peticion
-> autenticacion
-> autorizacion
-> resolucion de contexto
-> seleccion de pool
-> balanceo tecnico
-> ejecucion del caso de uso
-> auditoria, evento o log tecnico
```

## Contexto de routing

Cada peticion relevante debe poder construir un contexto minimo.

Campos conceptuales:

- `tenant_id`.
- `legal_entity_id`.
- `user_id`.
- `roles`.
- `operation_type`.
- `country`.
- `data_region`.
- `erp_connection_id`.
- `correlation_id`.

No todos los campos tienen que existir desde el primer prototipo, pero el diseno debe preverlos.

## Seleccion de pool

Un pool es un conjunto de recursos tecnicos autorizados para un contexto funcional.

Ejemplos:

- pool unico del MVP.
- pool por region.
- pool por pais.
- pool por grupo de sociedades.
- pool dedicado para una legal entity.
- pool de integracion ERP.

La seleccion del pool puede depender de:

- tenant.
- legal entity.
- residencia del dato.
- criticidad de la operacion.
- ERP asociado.
- disponibilidad de integracion.
- reglas contractuales.

## Balanceo tecnico

Dentro del pool seleccionado se puede aplicar balanceo tecnico.

Estrategias posibles:

- round robin ponderado.
- menor numero de conexiones.
- menor latencia.
- menor tasa de error.
- capacidad disponible.
- combinacion de metricas.

La estrategia concreta no debe afectar al dominio. El dominio recibe un caso de uso valido y trabaja con puertos, repositorios y Unit of Work.

## Resource-aware routing

El routing basado en recursos puede ser util cuando existe observabilidad fiable.

Metricas relevantes:

- CPU.
- memoria.
- conexiones activas.
- cola de trabajos.
- latencia media.
- tasa de error.
- tiempo de respuesta del ERP.
- circuit breaker abierto o cerrado.

Regla:

```text
Las metricas tecnicas optimizan dentro del pool autorizado. No deciden el contexto funcional.
```

## Integracion ERP

El routing debe considerar que una legal entity puede estar asociada a una conexion ERP concreta.

Ejemplos:

- una sociedad usa D365 F&O.
- otra sociedad usa otra compania dentro del mismo ERP.
- una sociedad futura usa otro ERP.
- una integracion esta temporalmente degradada.

El adaptador ERP se decide en application o infrastructure mediante puertos. El dominio no conoce el ERP concreto.

## Seguridad y privacidad

Reglas:

- Resolver tenant es obligatorio.
- Resolver legal entity es obligatorio en operaciones fiscales, contables y de provision.
- Las peticiones sin contexto suficiente deben rechazarse.
- El fallback tecnico solo puede ocurrir dentro del pool autorizado.
- Los logs no deben exponer datos sensibles innecesarios.
- Toda decision relevante debe ser trazable.

## Observabilidad

El sistema debe poder explicar:

- que contexto tenia la peticion.
- que pool se selecciono.
- que instancia proceso la peticion.
- que regla se aplico.
- cuanto tardo.
- si hubo error.
- si hubo fallback.
- que correlacion de proceso tuvo.

En MVP puede bastar con logs estructurados. En una version productiva puede evolucionar a metricas, trazas distribuidas y dashboards.

## Fallos esperados

Casos a controlar:

- tenant no resuelto.
- legal entity no resuelta.
- usuario sin permisos.
- pool no disponible.
- ERP no disponible.
- instancia saturada.
- timeout.
- fallback no permitido.

El sistema debe fallar de forma controlada y auditable.

## Alcance MVP

Para el MVP basta con:

- tenant y legal entity conceptuales.
- un pool unico de ejecucion.
- una politica de routing simple y documentada.
- logs de contexto y correlacion.
- health check del backend.

No hace falta:

- multi-region real.
- balanceo dinamico avanzado.
- service mesh.
- autoscaling.
- aislamiento fisico por tenant.

## Conceptos de configuracion futura

Entidades o configuraciones futuras:

- `infrastructure_pool`.
- `pool_instance`.
- `legal_entity_routing_policy`.
- `erp_connection`.
- `routing_decision_log`.
- `health_snapshot`.

Estas piezas no forman parte del dominio financiero. Deben vivir en configuracion, infraestructura u observabilidad.

## Regla de arquitectura

```text
El dominio decide si una operacion es valida. La infraestructura decide donde se ejecuta.
```
