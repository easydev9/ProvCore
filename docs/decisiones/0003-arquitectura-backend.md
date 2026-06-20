# Decision 0003 - Arquitectura tecnica minima del backend

## Estado

Aceptada.

## Contexto

ProvCore no es una aplicacion centrada en un unico formulario o CRUD. Es un motor comun de provisiones que debe adaptarse a distintos origenes operativos:

- pedido interno.
- factura sin provision previa.
- movimiento de tarjeta corporativa.
- suscripcion recurrente.
- otros origenes futuros.

El concepto central es abstracto y transversal. Si el prototipo se construye alrededor del primer origen implementado, el motor quedara acoplado por accidente a pedido interno o factura. Eso dificultaria incorporar tarjetas, provisiones tardias y nuevos intermodulos.

## Problema

Una arquitectura plana por capas globales seria rapida al principio:

```text
routes -> services -> repositories -> database
```

Pero podria mezclar responsabilidades de negocio, datos y HTTP en cuanto el dominio crezca.

Una clean architecture completa desde el primer commit tambien tiene coste:

- mas carpetas.
- mas conceptos.
- mas codigo de coordinacion.
- mas lentitud inicial.

El proyecto necesita separar negocio de datos desde el inicio, pero sin convertir el MVP en un ejercicio academico.

## Decision

ProvCore se construira como un monolito modular orientado a clean architecture.

Esto significa:

- un unico backend desplegable.
- una unica base de datos principal.
- modulos internos con limites funcionales claros.
- separacion explicita entre dominio, application, ports, infrastructure e interface.
- evolucion posible hacia una clean architecture mas estricta tras cerrar el MVP.

La implementacion del MVP sera pragmatica, pero respetara desde el inicio la separacion entre:

- dominio.
- casos de uso.
- puertos.
- infraestructura.
- interfaz.

El modulo central sera:

```text
provisioning_engine
```

Este modulo encapsulara las reglas comunes de provision, consumo, regularizacion y auditoria funcional. Los modulos de entrada no implementaran reglas de provision por su cuenta. Actuaran como origenes o adaptadores del motor comun.

## Arquitectura conceptual

```text
interface -> application -> domain
infrastructure -> application/domain
application -> ports
ports -> implementations in infrastructure
```

Regla principal:

```text
El negocio no depende de FastAPI ni de SQL Server.
```

## Estructura inicial esperada

```text
backend/
  app/
    main.py
    core/
    shared/
    modules/
      provisioning_engine/
        domain/
        application/
        ports/
        infrastructure/
        interface/
      internal_orders/
        domain/
        application/
        ports/
        infrastructure/
        interface/
      invoices/
        domain/
        application/
        ports/
        infrastructure/
        interface/
      audit/
        domain/
        application/
        ports/
        infrastructure/
        interface/
```

Los modulos `suppliers`, `cards` y `analytics` se añadiran cuando entren en el alcance de implementacion. No se crearan carpetas vacias si no aportan valor inmediato.

## Responsabilidad de cada capa

### Domain

Contiene negocio puro.

Puede contener:

- entidades.
- value objects.
- estados.
- reglas.
- errores de dominio.

No puede depender de:

- FastAPI.
- SQLAlchemy.
- pyodbc.
- Pydantic de API.
- SQL Server.
- variables de entorno.

### Application

Contiene casos de uso.

Ejemplos:

- crear provision desde pedido interno.
- buscar provisiones compatibles.
- aprobar consumo de provision.
- crear provision tardia.
- registrar auditoria funcional.

La capa application coordina dominio y puertos. No debe conocer detalles de SQL Server ni responder directamente con errores HTTP.

### Ports

Define contratos que la aplicacion necesita.

Ejemplos:

- `ProvisionRepository`.
- `InvoiceRepository`.
- `AuditRepository`.
- `UnitOfWork`.

Un puerto expresa que necesita el caso de uso, no como se implementa.

### Infrastructure

Contiene implementaciones concretas.

Puede contener:

- modelos ORM.
- repositorios SQL Server.
- conexion a base de datos.
- implementacion de Unit of Work.
- migraciones.

Esta capa si puede depender de SQLAlchemy, pyodbc o librerias concretas de persistencia.

### Interface

Contiene adaptadores de entrada y salida.

Puede contener:

- routers FastAPI.
- schemas Pydantic de request y response.
- traduccion de errores de dominio a errores HTTP.
- dependencias de FastAPI.

No debe contener reglas de negocio.

## Modulo central provisioning_engine

El modulo `provisioning_engine` es el nucleo del sistema.

Debe contener:

- entidad `Provision`.
- contrato de origen provisionable.
- reglas de creacion de provision.
- reglas de consumo.
- relacion factura-provision.
- regularizaciones basicas.
- estados de provision.
- errores de dominio del motor.

Los modulos externos llaman al motor.

Ejemplo:

```text
internal_orders -> provisioning_engine -> audit
invoices -> provisioning_engine -> audit
cards -> provisioning_engine -> audit
```

## Regla sobre origenes

Un origen operativo puede generar provision si cumple un contrato minimo:

- tipo de origen.
- id de origen.
- sociedad.
- responsable.
- area.
- proveedor operativo o alias.
- importe.
- moneda.
- periodo o fecha.
- tipo de gasto.

El motor no debe depender del detalle interno de cada origen.

## Reglas de dependencia

Permitido:

```text
interface importa application
application importa domain
application importa ports
infrastructure implementa ports
infrastructure importa domain si necesita mapear entidades
```

Prohibido:

```text
domain importa infrastructure
domain importa interface
domain importa FastAPI
domain importa SQLAlchemy
application importa FastAPI
application usa sesiones SQL directamente
router accede a SQL Server directamente
```

## Estrategia para el MVP

Durante el MVP no se implementara una clean architecture completa en todos los modulos. Se aplicara una version pragmatica:

- crear solo los modulos necesarios.
- crear solo las capas necesarias dentro de cada modulo.
- mantener las dependencias en direccion correcta.
- evitar logica de negocio en routers.
- evitar logica de negocio en repositorios.
- evitar que modelos ORM actuen como entidades de dominio.

El primer incremento se construira con:

- `provisioning_engine`.
- `internal_orders`.
- `invoices`.
- `audit`.

## Evolucion hacia clean architecture completa

Una vez finalizado el MVP, la arquitectura podra evolucionar a una clean architecture mas estricta sin reescribir el sistema.

La evolucion esperada sera:

1. Extraer reglas puras a `domain`.
2. Convertir servicios en casos de uso explicitos.
3. Formalizar puertos con interfaces o protocolos.
4. Encapsular transacciones en Unit of Work.
5. Separar modelos ORM de entidades de dominio.
6. Aumentar tests de dominio sin base de datos.
7. Aumentar tests de application con repositorios fake.

## Consecuencias

### Positivas

- El negocio queda protegido de FastAPI y SQL Server.
- El motor comun no queda acoplado al primer origen implementado.
- El sistema puede crecer hacia tarjetas, proveedores y analitica sin reordenar toda la base.
- El testing del dominio sera mas sencillo.
- El proyecto fuerza criterio arquitectonico desde el inicio.

### Costes

- Habra mas estructura inicial.
- Cada caso de uso tocara mas de una capa.
- Habra que ser disciplinado con dependencias.
- La primera entrega sera mas lenta que un CRUD plano.

## Reglas derivadas

- No se implementara logica de provision dentro de `internal_orders` o `invoices`.
- El motor `provisioning_engine` sera la fuente de reglas comunes.
- SQL Server solo se tocara desde infrastructure.
- FastAPI solo vivira en interface.
- La auditoria sera transversal, pero se invocara desde casos de uso.
- Toda excepcion relevante debe pasar por dominio o application antes de persistirse.
