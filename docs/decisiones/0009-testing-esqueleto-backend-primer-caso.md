# Decisión 0009 - Testing, esqueleto backend y primer caso implementable

## Estado

Aceptada.

## Contexto

ProvCore ya tiene definidas las decisiones de alcance, stack, arquitectura backend, persistencia, modelo tenant-aware, routing funcional, autorización y contratos API.

El siguiente paso es preparar el inicio del desarrollo sin caer en implementación improvisada. Antes de crear carpetas y código productivo, debe quedar definido cómo se validará la separación de capas y cuál será el primer caso real.

## Problema

Si el backend empieza directamente por FastAPI o por tablas, aparecerán riesgos:

- routers con lógica de negocio.
- entidades de dominio contaminadas por ORM.
- tests tardíos o inexistentes.
- estructura de carpetas creada sin necesidad real.
- primer incremento demasiado grande.
- dependencia prematura de SQL Server para validar reglas simples.

ProvCore necesita empezar por un caso pequeño que permita probar arquitectura, tests y flujo de trabajo.

## Decisión

El primer caso implementable será:

```text
CreateInternalOrder
```

Motivo:

- es la primera entrada operativa del flujo.
- captura el compromiso de gasto antes de la factura.
- no exige todavía consumir provisiones.
- permite validar tenant, legal entity, usuario, permiso, importe, periodo y proveedor operativo.
- prepara el cruce posterior con provisión, factura, auditoría y analítica.

## Enfoque de implementación

El desarrollo empezará por dominio y application.

Orden:

1. Definir entidad o modelo de dominio mínimo para pedido interno.
2. Definir value objects necesarios para importe, periodo y contexto.
3. Definir comando de application `CreateInternalOrderCommand`.
4. Definir caso de uso `CreateInternalOrder`.
5. Definir puertos mínimos para persistencia y auditoría.
6. Probar el caso con implementaciones en memoria.
7. Añadir interface FastAPI cuando application esté validado.
8. Añadir infrastructure SQLAlchemy después de validar el contrato del caso de uso.

Regla:

```text
No se implementa FastAPI antes de tener probado el caso de uso en application.
```

## Esqueleto backend objetivo

El backend se organizará bajo un paquete Python propio.

Estructura objetivo:

```text
backend/
  pyproject.toml
  src/
    provcore/
      internal_orders/
        domain/
        application/
        ports/
        interface/
        infrastructure/
      provisioning_engine/
        domain/
        application/
        ports/
      audit/
        application/
        ports/
        infrastructure/
      shared/
        domain/
        application/
        interface/
  tests/
    unit/
    integration/
    api/
```

Durante el primer incremento no se crearán carpetas vacías sin uso inmediato.

La estructura crecerá solo cuando una issue lo necesite.

## Idioma técnico

El código se escribirá en inglés.

Aplica a:

- paquetes.
- clases.
- métodos.
- funciones.
- variables.
- endpoints.
- permisos.
- eventos.
- errores.
- tests.

La documentación funcional seguirá en español.

## Estrategia de testing

### Tests unitarios de dominio

Objetivo:

Validar reglas puras sin base de datos, HTTP ni frameworks.

Ejemplos:

- importe no puede ser cero o negativo.
- periodo de servicio debe tener inicio y fin coherentes.
- pedido interno debe tener tenant y legal entity.
- proveedor operativo informado no sustituye al proveedor fiscal.

### Tests de application

Objetivo:

Validar casos de uso con puertos en memoria.

Ejemplos:

- `CreateInternalOrder` crea pedido en estado inicial esperado.
- se registra evento o auditoría funcional.
- se rechaza operación sin legal entity.
- se rechaza operación sin permiso suficiente.

### Tests de integración

Objetivo:

Validar SQLAlchemy, Unit of Work, repositorios y migraciones.

No entran en el primer microincremento si todavía no existe infrastructure.

### Tests API

Objetivo:

Validar contrato HTTP cuando exista router FastAPI.

No sustituyen tests de dominio ni application.

## Herramienta de tests

La herramienta base será:

```text
pytest
```

Motivos:

- estándar en Python backend.
- simple para tests unitarios.
- compatible con FastAPI.
- compatible con fixtures de base de datos en fases posteriores.

## Regla sobre persistencia

Para `CreateInternalOrder`, la primera validación no dependerá de SQL Server.

Primero se probará con repositorios en memoria.

Después se implementará SQLAlchemy y Alembic cuando el contrato del caso de uso esté claro.

## Regla sobre auditoría

El caso `CreateInternalOrder` deberá dejar previsto el registro de auditoría o evento funcional.

En el primer incremento podrá usarse un puerto de auditoría en memoria.

No se debe dejar la auditoría como añadido posterior.

## Consecuencias

### Positivas

- El primer desarrollo valida arquitectura real.
- Se evita empezar por HTTP o por tablas.
- Se protege el dominio desde el primer commit de código.
- Se puede explicar el avance de forma profesional.
- Se reduce el riesgo de refactorización temprana.

### Costes

- Hay más trabajo inicial antes de ver un endpoint funcionando.
- El primer caso requiere definir puertos y tests aunque sea pequeño.
- La integración con SQL Server se pospone hasta que el caso de uso esté estable.

## Criterio de finalización del primer caso

`CreateInternalOrder` estará listo cuando:

- exista caso de uso en application.
- existan reglas mínimas de dominio.
- existan tests unitarios y de application.
- exista puerto de repositorio.
- exista puerto de auditoría o eventos.
- no exista dependencia de FastAPI en dominio ni application.
- no exista dependencia de SQLAlchemy fuera de infrastructure.
- el contrato API correspondiente pueda implementarse sin cambiar la lógica de negocio.
