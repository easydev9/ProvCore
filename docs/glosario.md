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

## Auditoria

Registro trazable de acciones, decisiones, cambios de estado y motivos.

Debe permitir reconstruir quien hizo que, cuando y por que.

## Contabilizacion definitiva

Momento en que una factura queda registrada contablemente de forma final en el circuito previsto.

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

## Origen provisionable

Cualquier origen capaz de generar una provision bajo un contrato comun.

Ejemplos:

- pedido interno.
- movimiento de tarjeta.
- factura sin provision previa.
- suscripcion recurrente.

## Pedido interno

Compromiso de gasto informado por el responsable antes de recibir la factura.

No debe exigir datos fiscales al usuario operativo.

## Periodificacion

Distribucion de un gasto entre varios periodos.

Puede aplicarse cuando el servicio o factura cubre mas de un periodo contable.

## Persistencia

Forma en que el sistema guarda y recupera informacion estable.

En ProvCore se realizara sobre SQL Server, aislada en infrastructure.

## Proveedor fiscal

Proveedor validado fiscalmente.

Puede incluir razon social, NIF/VAT y codigo ERP.

La fuente de verdad es Administracion y los datos maestros.

## Proveedor operativo

Proveedor tal como lo conoce el usuario.

Puede ser alias, nombre comercial o denominacion habitual. No sustituye al proveedor fiscal.

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
