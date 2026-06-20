# Glosario

## Objetivo

Definir vocabulario comun para ProvCore.

Este glosario debe usarse en documentacion, issues, decisiones y codigo futuro.

## Administracion

Equipo responsable de validar la verdad fiscal y contable.

Valida proveedor fiscal, impuestos, cuentas, consumos, regularizaciones y contabilizacion.

## Analitica minima

Conjunto inicial de vistas para entender:

- importe provisionado.
- importe consumido.
- importe pendiente.
- provisiones tardias.
- casos bloqueados o pendientes.

## Alerta

Aviso operativo generado por el sistema para que un usuario o grupo responsable actue sobre un pendiente, excepcion o fecha clave.

## Alembic

Herramienta de migraciones usada para versionar cambios de esquema de base de datos.

En ProvCore, Alembic sera la fuente de verdad tecnica para crear o modificar estructura de SQL Server.

## Auditoria

Registro trazable de acciones, decisiones, cambios de estado y motivos.

Debe permitir reconstruir quien hizo que, cuando y por que.

## Balanceo tecnico

Distribucion de carga entre instancias tecnicas dentro de un pool autorizado.

No decide tenant, legal entity ni permisos.

## Buyer group

Grupo comprador o grupo responsable asociado a proveedores, sociedades o areas.

Puede venir de ERP, configuracion interna o sincronizacion externa.

## Closing period

Periodo usado para controlar fechas de cierre, pendientes y alertas.

Puede estar asociado a una legal entity.

## Contabilizacion definitiva

Momento en que una factura queda registrada contablemente de forma final en el circuito previsto.

## Correlation id

Identificador tecnico que permite seguir una peticion o proceso a traves de logs, eventos, auditoria e integraciones.

En ProvCore, ninguna factura debe contabilizarse definitivamente sin consumir una provision previa o una provision tardia auditada.

## Consumo de provision

Operacion por la que una factura consume total o parcialmente una provision.

Actualiza:

- importe consumido.
- importe pendiente.
- estado de la provision.
- relacion factura-provision.
- auditoria.

## Dominio

Capa que contiene reglas puras de negocio.

No debe depender de FastAPI, SQL Server, ORM ni frameworks.

## ERP

Sistema externo que actua como fuente de datos maestros y destino conceptual de integraciones contables.

En el MVP no habra integracion real con ERP.

## Infrastructure pool

Conjunto de recursos tecnicos autorizados para procesar peticiones de un contexto funcional concreto.

Puede ser comun, regional, por grupo de sociedades o dedicado a una legal entity.

## Evento de proceso

Registro estructurado de algo que ocurrio en el flujo.

Sirve para trazabilidad, metricas y analitica operativa.

## Factura

Documento recibido de proveedor.

Puede consumir una o varias provisiones. Si no existe provision compatible, puede activar una provision tardia auditada.

## Factura-provision

Relacion entre una factura y una provision.

Permite:

- una factura contra una provision.
- una factura contra varias provisiones.
- una provision consumida por varias facturas.

## IA/OCR

Herramienta de extraccion o sugerencia.

Puede sugerir datos, proveedor fiscal o matching factura-provision. No valida la verdad contable.

## Legal entity

Sociedad juridica dentro de un tenant.

Puede tener pais, moneda, identificador fiscal, reglas fiscales, periodos contables e integracion ERP propia.

## Matching suggestion

Sugerencia generada por reglas, historico o IA para relacionar entidades.

Ejemplos:

- proveedor operativo con proveedor fiscal.
- factura con provision.
- factura con responsable.
- factura con movimiento de tarjeta.

## Interfaz

Capa de entrada y salida tecnica.

En backend, contiene routers FastAPI, schemas HTTP y traduccion de errores.

No contiene reglas de negocio.

## Modelo ORM

Clase tecnica que representa una tabla o estructura persistida.

No equivale a entidad de dominio.

Debe vivir en infrastructure.

## Monolito modular

Arquitectura con un unico backend desplegable, pero dividido internamente en modulos funcionales con responsabilidades claras.

ProvCore se construira como monolito modular orientado a clean architecture.

## Movimiento de tarjeta

Gasto originado por tarjeta corporativa.

Es un origen operativo futuro del motor de provisiones.

## Movimiento provisionable

Entrada operativa normalizada capaz de generar una provision.

Tiene un origen identificado y cumple un contrato comun para que el motor pueda procesarla sin conocer detalles del origen.

## Origen provisionable

Cualquier origen capaz de generar una provision bajo un contrato comun.

Ejemplos:

- pedido interno.
- movimiento de tarjeta.
- factura sin provision previa.
- suscripcion recurrente.

## Pool autorizado

Pool de infraestructura seleccionado por reglas funcionales de tenant, legal entity, permisos, residencia del dato e integracion asociada.

## Process event

Nombre tecnico posible para evento de proceso.

Puede convivir con auditoria en MVP si todavia no se separa fisicamente.

## Resource-aware routing

Estrategia tecnica que usa metricas como latencia, errores, conexiones, CPU, memoria o colas para elegir una instancia dentro del pool autorizado.

## Routing funcional

Decision de destino basada en contexto de negocio y seguridad.

Usa tenant, legal entity, permisos, residencia del dato, ERP asociado y tipo de operacion.

Debe ejecutarse antes del balanceo tecnico.

## Pedido interno

Compromiso de gasto informado por el responsable antes de recibir la factura.

No debe exigir datos fiscales al usuario operativo.

## Periodificacion

Distribucion de un gasto entre varios periodos.

Puede aplicarse cuando el servicio o factura cubre mas de un periodo contable.

## Persistencia

Forma en que el sistema guarda y recupera informacion estable.

En ProvCore se realizara sobre SQL Server, aislada en infrastructure.

## pyodbc

Driver que permite a Python conectarse a SQL Server mediante ODBC.

En ProvCore es un detalle de infrastructure y no debe aparecer en domain ni application.

## Proveedor fiscal

Proveedor validado fiscalmente.

Puede incluir razon social, NIF/VAT y codigo ERP.

La fuente de verdad es Administracion y los datos maestros.

## Proveedor operativo

Proveedor tal como lo conoce el usuario.

Puede ser alias, nombre comercial o denominacion habitual. No sustituye al proveedor fiscal.

## Solicitud de alta proveedor

Flujo por el que se solicita crear o validar un proveedor fiscal que no existe en ERP para una legal entity.

Debe resolverse antes de continuar con el registro definitivo de la factura afectada.

## Supplier responsibility

Relacion entre proveedor y grupo responsable.

Permite saber que usuarios deben recibir alertas por pendientes, excepciones o cierre.

## Tenant

Cliente, grupo empresarial o unidad aislada dentro de un SaaS.

Los datos de un tenant no deben mezclarse con los de otro tenant.

## Provision

Entidad central del motor.

Representa un gasto previsto o comprometido que debe existir antes de la contabilizacion definitiva de la factura.

## Provision tardia

Provision creada desde una factura cuando no existia provision previa compatible.

Es una excepcion auditada. Debe requerir motivo obligatorio y consumirse inmediatamente con la factura.

## Provisioning engine

Modulo central de ProvCore.

Encapsula reglas comunes de provision, consumo, regularizacion y trazabilidad.

Los modulos de entrada no deben duplicar estas reglas.

## Puerto

Contrato que define lo que una capa necesita sin acoplarse a una implementacion concreta.

Ejemplo:

- `ProvisionRepository`.
- `AuditRepository`.
- `UnitOfWork`.

## Regularizacion

Ajuste generado por diferencias entre provision y realidad final.

Puede venir de:

- diferencia de importe.
- impuestos.
- divisa.
- periodificacion.
- no deducible.
- ausencia de factura.

## Repository

Componente que encapsula acceso a datos.

La aplicacion usa el contrato. Infrastructure implementa el acceso real a SQL Server.

## Responsable

Usuario operativo que informa el compromiso de gasto y valida que la factura corresponde al servicio.

No debe conocer datos fiscales ni contables.

## SQL Server Management Studio

Herramienta usada para inspeccionar y validar manualmente la base de datos SQL Server durante el desarrollo.

No sustituye migraciones versionadas.

## SQLAlchemy ORM

Herramienta de mapeo objeto-relacional usada para representar tablas SQL Server como modelos de persistencia Python.

En ProvCore solo debe vivir en infrastructure. Los modelos ORM no son entidades de dominio.

## Unit of Work

Patron que coordina una operacion completa dentro de una transaccion.

Garantiza que un conjunto de cambios se confirma completo o se revierte completo.

## Value object

Objeto de dominio que representa un concepto sin identidad propia.

Ejemplos posibles:

- dinero.
- periodo.
- porcentaje.
- identificador de provision.
