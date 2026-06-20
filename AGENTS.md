# AGENTS.md

## Proposito

Este archivo define como debe trabajar cualquier agente en el repositorio ProvCore.

ProvCore es un proyecto de arquitectura funcional y backend para un motor comun de provisiones. No es un repositorio para generar codigo sin criterio. Cualquier cambio debe estar alineado con el dominio, las decisiones documentadas y las issues abiertas.

## Regla principal

No hacer vibe coding.

Antes de implementar:

1. Entender el problema.
2. Revisar la documentacion existente.
3. Identificar la decision o issue relacionada.
4. Explicar opciones y trade-offs si hay una decision abierta.
5. Documentar la decision si afecta arquitectura, persistencia, API, seguridad, testing o modelo de dominio.
6. Implementar solo cuando el enfoque este confirmado.

## Lectura obligatoria antes de cambios relevantes

Para entender el proyecto:

- `README.md`
- `docs/contexto_para_agentes.md`
- `docs/contexto_funcional.md`
- `docs/arquitectura_funcional.md`
- `docs/roadmap_mvp.md`

Para cambios de arquitectura o backend:

- `docs/decisiones/0001-alcance-mvp.md`
- `docs/decisiones/0002-formato-prototipo.md`
- `docs/decisiones/0003-arquitectura-backend.md`
- `docs/decisiones/0004-persistencia-migraciones.md`
- `docs/decisiones/0005-modelo-saas-tenant-aware.md`

Para cambios de dominio:

- `docs/modelo_dominio_mvp.md`
- `docs/modelo_datos_inicial.md`
- `docs/estados_entidades.md`
- `docs/casos_uso_detallados.md`
- `docs/diagramas_flujo.md`

Para cambios de vision de producto:

- `docs/vision_estrategica_producto.md`

Para trabajo planificado:

- `docs/github_issues.md`
- `docs/issues_backlog.md`
- Issues abiertas en GitHub.

## Decisiones ya tomadas

- El MVP objetivo incluye flujo principal, provision tardia auditada, mapeo proveedor operativo-fiscal basico, auditoria y analitica minima.
- El primer incremento implementable es `Pedido interno -> Provision -> Factura -> Consumo -> Auditoria`.
- El prototipo sera backend-first.
- Stack aprobado: FastAPI, SQL Server, SQL Server Management Studio y frontend simple.
- La arquitectura sera modular orientada a clean architecture.
- El modulo central sera `provisioning_engine`.
- El dominio no debe depender de FastAPI ni de SQL Server.
- Persistencia aprobada: SQLAlchemy ORM, Alembic, pyodbc y Unit of Work.
- SQLAlchemy y pyodbc solo pueden vivir en infrastructure.
- Modelo SaaS tenant-aware aprobado.
- El motor identifica movimientos provisionables y su origen.
- La factura se bloquea si el proveedor fiscal no existe para la legal entity.

## Reglas de arquitectura

ProvCore debe proteger el dominio desde el inicio.

Reglas obligatorias:

- FastAPI vive en `interface`.
- SQL Server vive en `infrastructure`.
- SQLAlchemy vive en `infrastructure`.
- pyodbc vive en `infrastructure`.
- La logica de negocio vive en `domain` y `application`.
- Los casos de uso dependen de puertos, no de implementaciones concretas.
- Los repositorios concretos implementan puertos.
- Los routers no contienen reglas de negocio.
- Los repositorios no contienen reglas de negocio.
- Los modelos ORM no sustituyen a entidades de dominio.
- El commit y rollback se controlan desde Unit of Work.
- El motor `provisioning_engine` concentra reglas comunes de provision, consumo y regularizacion.
- Los modulos de entrada no implementan reglas propias de provision.
- Los modulos de entrada adaptan su origen a `ProvisionableMovement`.
- El tenant es frontera de seguridad.
- La legal entity es contexto minimo para proveedor fiscal, factura, provision, periodo e integracion ERP.
- Los bloqueos, alertas y excepciones deben generar auditoria o evento de proceso.

## Modulos iniciales

Para el MVP inicial:

- `provisioning_engine`
- `internal_orders`
- `invoices`
- `audit`

Futuros modulos:

- `suppliers`
- `cards`
- `analytics`

No crear carpetas vacias sin necesidad inmediata.

## Reglas de documentacion

- No usar em dash en documentos.
- No introducir nombres internos sensibles.
- Mantener tono de proyecto real.
- Si una decision cambia, actualizar el documento de decision correspondiente o crear uno nuevo.
- Si se crea una decision nueva, enlazarla desde `README.md` y `docs/roadmap_mvp.md` cuando aplique.
- Los documentos deben explicar el por que, no solo el que.

## Reglas de codigo cuando empiece el prototipo

- No crear codigo sin issue asociada.
- No mezclar reglas de negocio con HTTP.
- No mezclar reglas de negocio con SQL.
- No introducir dependencias sin justificar.
- No crear abstracciones que no resuelvan una necesidad real.
- Añadir tests cuando se implementen reglas de dominio o casos de uso.
- Validar cambios de base de datos con SQL Server Management Studio cuando aplique.

## Reglas SQL

- Trabajar paso a paso.
- Validar primero tablas y relaciones base.
- No lanzar scripts complejos sin haber validado las partes.
- Evitar cambios destructivos sin aprobacion explicita.
- Documentar claves, constraints e indices relevantes.

## Reglas Git

- Mantener commits pequeños y descriptivos.
- No hacer commits con cambios no relacionados.
- No reescribir historial sin instruccion explicita.
- No cerrar issues sin dejar comentario de trazabilidad cuando la issue representa una decision.

## Fuente de verdad

La fuente de verdad del proyecto se reparte asi:

- Vision general: `README.md`.
- Contexto rapido para agentes: `docs/contexto_para_agentes.md`.
- Funcional: `docs/especificacion_funcional_inicial_provisiones.md`.
- Arquitectura funcional: `docs/arquitectura_funcional.md`.
- Decisiones: `docs/decisiones/`.
- Modelo de datos: `docs/modelo_datos_inicial.md`.
- Estados: `docs/estados_entidades.md`.
- Plan de trabajo: GitHub Issues.

Si hay contradiccion, prevalecen las decisiones documentadas mas recientes.
