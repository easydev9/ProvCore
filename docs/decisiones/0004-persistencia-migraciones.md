# Decision 0004 - Persistencia y migraciones

## Estado

Aceptada.

## Contexto

ProvCore se construira como monolito modular orientado a clean architecture. El backend usara FastAPI y SQL Server.

Antes de implementar codigo, es necesario decidir como se accedera a datos, como se versionara el esquema de base de datos y como se mantendra separada la logica de negocio de la persistencia.

## Problema

El sistema necesita persistir entidades y relaciones del dominio:

- pedidos internos.
- provisiones.
- facturas.
- relaciones factura-provision.
- auditoria.
- proveedores operativos y fiscales.
- regularizaciones.

Estas operaciones no son simples inserciones. Hay casos de uso que deben ser atomicos:

- crear pedido interno y provision.
- aprobar consumo factura-provision.
- crear provision tardia y consumirla inmediatamente.
- registrar auditoria junto con cambios de estado.

Si la persistencia se mezcla con dominio o application, el sistema quedara acoplado a SQL Server y sera dificil de testear.

## Decision

ProvCore usara:

```text
SQLAlchemy ORM + Alembic + pyodbc + Unit of Work
```

Regla no negociable:

```text
El ORM y el driver de base de datos solo pueden vivir en infrastructure.
```

Por tanto:

- `domain` no importa SQLAlchemy.
- `domain` no importa pyodbc.
- `domain` no conoce SQL Server.
- `application` no importa SQLAlchemy.
- `application` no usa sesiones SQL directamente.
- `interface` no accede directamente a repositories concretos.
- `infrastructure` implementa los puertos definidos por application.

## Componentes

### SQLAlchemy ORM

SQLAlchemy ORM se usara para mapear tablas SQL Server a modelos de persistencia Python.

Su responsabilidad sera:

- definir modelos persistidos.
- mapear columnas y relaciones.
- permitir queries desde repositories concretos.
- trabajar con sesiones y transacciones bajo control de Unit of Work.

Regla clave:

```text
Modelo ORM no es entidad de dominio.
```

Ejemplo conceptual:

```text
Provision
  entidad de dominio con reglas de negocio

ProvisionORM
  modelo de infrastructure que representa una tabla
```

La traduccion entre ambos corresponde a infrastructure.

### Alembic

Alembic se usara para versionar cambios de esquema.

Su responsabilidad sera:

- crear migraciones versionadas.
- aplicar cambios de estructura.
- permitir reconstruir el esquema desde Git.
- mantener historial de evolucion de base de datos.

SQL Server Management Studio se usara para inspeccionar y validar, pero no sera la fuente de verdad de cambios estructurales.

Fuente de verdad:

```text
Git + migraciones Alembic
```

### pyodbc

pyodbc se usara como driver de conexion entre Python y SQL Server.

Cadena conceptual:

```text
FastAPI -> SQLAlchemy -> pyodbc -> ODBC Driver -> SQL Server
```

pyodbc es detalle de infrastructure.

No debe aparecer en:

- domain.
- application.
- casos de uso.
- reglas de negocio.

### Unit of Work

Unit of Work se usara para coordinar transacciones de casos de uso.

Su responsabilidad sera:

- abrir una unidad transaccional.
- exponer repositories necesarios.
- confirmar cambios con commit.
- revertir cambios con rollback si hay error.

Ejemplo funcional:

```text
Aprobar consumo factura-provision
  cargar factura
  cargar provision
  ejecutar regla de consumo
  guardar relacion factura-provision
  guardar auditoria
  confirmar transaccion
```

La operacion debe guardar todo o no guardar nada.

## Flujo de dependencias

```text
interface
  -> application
    -> ports
    -> domain

infrastructure
  -> implements ports
  -> uses SQLAlchemy
  -> uses pyodbc
  -> uses SQL Server
```

## Flujo de un caso de uso

```text
FastAPI router
  recibe request
  valida schema
  llama caso de uso

Application use case
  abre Unit of Work
  usa repositories definidos por puertos
  ejecuta entidades y reglas de dominio
  solicita persistencia
  confirma transaccion

Infrastructure
  traduce dominio a ORM
  persiste en SQL Server
  ejecuta commit o rollback
```

## Repositories

Los repositories seran contratos definidos como puertos.

Ejemplos:

- `ProvisionRepository`.
- `InternalOrderRepository`.
- `InvoiceRepository`.
- `AuditRepository`.

Los contratos expresan operaciones necesarias por los casos de uso:

- obtener por id.
- guardar.
- buscar abiertas compatibles.
- registrar relacion.
- registrar evento de auditoria.

Las implementaciones SQL Server viviran en infrastructure.

## Migraciones

Todo cambio estructural de base de datos debera tener migracion Alembic.

Ejemplos:

- crear tabla.
- añadir columna.
- crear indice.
- crear clave foranea.
- modificar constraint.

No se aceptara crear o modificar estructura manualmente en SQL Server Management Studio sin reflejarlo en migracion.

## Validacion con SQL Server Management Studio

SQL Server Management Studio se usara para:

- inspeccionar tablas.
- validar constraints.
- revisar datos.
- ejecutar consultas de diagnostico.
- comprobar indices.
- entender el modelo fisico.

No sustituye:

- Alembic.
- Git.
- tests.
- repositories.

## Consecuencias

### Positivas

- El dominio queda separado de SQL Server.
- El sistema mantiene historial versionado de esquema.
- Los casos de uso pueden testearse con repositories fake.
- Las transacciones quedan centralizadas.
- La arquitectura queda alineada con clean architecture.
- SQL Server Management Studio sigue siendo util para aprendizaje y validacion manual.

### Costes

- SQLAlchemy y Alembic tienen curva de aprendizaje.
- Hay que mantener mappers entre dominio y ORM.
- Unit of Work añade estructura inicial.
- Alembic con SQL Server requiere configuracion cuidadosa.

## Reglas derivadas

- No usar modelos ORM como entidades de dominio.
- No hacer commit dentro de repositories individuales.
- El commit se controla desde Unit of Work.
- No ejecutar SQL desde application.
- No importar SQLAlchemy fuera de infrastructure.
- No importar pyodbc fuera de infrastructure.
- Toda migracion debe poder explicarse desde un cambio funcional o tecnico.
- Todo cambio de esquema debe poder validarse en SQL Server Management Studio.

## Decisiones pendientes derivadas

- Convencion exacta de nombres de tablas y columnas.
- Formato de identificadores tecnicos.
- Uso de GUID, enteros o codigos funcionales.
- Configuracion concreta de Alembic.
- Organizacion inicial de migraciones por modulo o global.
- Convencion de errores de persistencia.
