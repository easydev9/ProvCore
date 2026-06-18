# Decision 0002 - Formato del prototipo

## Estado

Aceptada y actualizada.

## Contexto

La Decision 0001 fija el alcance funcional del MVP. El siguiente paso es decidir como se construira el prototipo para evitar empezar a programar sin arquitectura ni criterios claros.

El prototipo debe servir para validar el flujo principal de ProvCore y preparar la ampliacion hacia provision tardia, mapeo proveedor operativo-fiscal y analitica minima.

## Problema

Existen varias formas de prototipar ProvCore:

1. Maqueta navegable sin backend.
2. Frontend con datos mock y logica en memoria.
3. API backend con base de datos y frontend simple.

La maqueta es rapida, pero no valida bien el dominio ni la arquitectura backend. El frontend con datos en memoria permite navegar el flujo, pero puede mezclar logica de negocio con interfaz. La API backend con base de datos exige mas decisiones, pero fuerza a modelar entidades, estados, contratos, persistencia y validaciones.

## Decision

El prototipo de ProvCore se construira como:

```text
FastAPI + SQL Server + SQL Server Management Studio + frontend simple
```

La ejecucion sera backend-first y con alcance controlado.

Esta decision sustituye la propuesta inicial de usar MySQL y HeidiSQL. El cambio se realiza para alinear el prototipo con un entorno corporativo mas habitual en administracion, finanzas y backoffice.

## Justificacion

### FastAPI

FastAPI encaja con el objetivo de desarrollar criterio backend:

- obliga a definir contratos HTTP.
- permite documentacion OpenAPI automatica.
- facilita separar rutas, modelos, servicios y persistencia.
- permite introducir testing de API de forma progresiva.
- ya es coherente con otros proyectos de referencia.

### SQL Server

SQL Server se elige como base de datos relacional del prototipo porque el dominio de ProvCore es claramente relacional y porque encaja mejor con entornos corporativos Windows, ERP y backoffice financiero:

- pedidos.
- provisiones.
- facturas.
- relaciones factura-provision.
- proveedores operativos.
- proveedores fiscales.
- auditoria.

El uso de SQL Server permite trabajar integridad referencial, claves, indices, normalizacion, T-SQL, consultas reales y criterios transferibles a proyectos internos de administracion y finanzas.

### SQL Server Management Studio

SQL Server Management Studio se usara como herramienta de inspeccion y administracion manual de la base de datos durante el desarrollo.

Su papel sera:

- revisar tablas.
- validar inserts.
- comprobar relaciones.
- ejecutar consultas de diagnostico.
- entender el modelo fisicamente.

No sustituye migraciones ni decisiones de modelado.

### Frontend simple

El frontend existira para navegar el flujo y validar la experiencia, pero no sera el centro inicial del proyecto.

Debe ser suficiente para:

- crear pedido interno.
- ver provision generada.
- registrar factura.
- seleccionar consumo.
- consultar auditoria basica.

No debe convertirse en una aplicacion compleja antes de cerrar el backend y el modelo de dominio.

## Fases de construccion

### Fase tecnica 0 - Preparacion

Objetivo:

Definir estructura tecnica sin implementar funcionalidad completa.

Incluye:

- decidir estructura de carpetas.
- definir convenciones de nombres.
- definir configuracion local.
- definir estrategia de migraciones.
- definir conexion a SQL Server.
- definir comandos minimos de ejecucion.

Resultado:

Proyecto arrancable con healthcheck y conexion validada a base de datos.

### Fase tecnica 1 - Dominio base

Objetivo:

Modelar el nucleo minimo del flujo principal.

Incluye:

- pedido interno.
- provision.
- factura.
- relacion factura-provision.
- auditoria de estado.

Resultado:

Modelo relacional minimo creado y validado en SQL Server.

### Fase tecnica 2 - API del flujo principal

Objetivo:

Exponer endpoints minimos para recorrer el primer incremento.

Incluye:

- crear pedido interno.
- generar provision.
- registrar factura.
- buscar provisiones compatibles.
- aprobar consumo.
- consultar auditoria.

Resultado:

Flujo principal ejecutable mediante API.

### Fase tecnica 3 - Frontend simple

Objetivo:

Crear una interfaz minima para navegar el flujo principal.

Incluye:

- pantalla de pedidos.
- pantalla de provisiones.
- pantalla de facturas.
- pantalla de consumo.
- vista simple de auditoria.

Resultado:

Flujo principal navegable sin depender de ejecutar requests manuales.

### Fase tecnica 4 - Excepcion auditada

Objetivo:

Implementar provision tardia cuando una factura no tenga provision compatible.

Incluye:

- detectar ausencia de provision.
- registrar motivo obligatorio.
- crear provision tardia.
- consumirla inmediatamente.
- auditar la decision.

Resultado:

Flujo excepcional ejecutable y consultable.

### Fase tecnica 5 - Ampliaciones MVP

Objetivo:

Incorporar mapeo proveedor operativo-fiscal basico y analitica minima.

Incluye:

- proveedor operativo.
- proveedor fiscal.
- mapeo validado por Administracion.
- vista de provisionado, consumido y pendiente.
- vista de excepciones.

Resultado:

MVP funcional completo segun Decision 0001.

## Requisitos minimos del prototipo

### Backend

- API REST con FastAPI.
- Endpoints versionados bajo un prefijo comun.
- Validacion de entrada.
- Errores HTTP coherentes.
- Separacion minima entre rutas, dominio/servicios y persistencia.
- Configuracion por variables de entorno.
- Documentacion OpenAPI disponible.

### Base de datos

- SQL Server como motor relacional.
- Tablas con claves primarias claras.
- Relaciones con claves foraneas cuando aplique.
- Campos monetarios con tipos decimales.
- Estados representados de forma controlada.
- Indices en campos de busqueda del flujo principal.
- Auditoria persistida.

### Frontend

- Interfaz simple.
- Flujo navegable.
- Sin complejidad visual innecesaria.
- Separacion clara de acciones por rol cuando aplique.
- Lectura facil de estados, importes y relaciones.

### Testing

- Tests minimos para reglas criticas del dominio.
- Tests de API para el flujo principal.
- Tests para provision tardia cuando se implemente.

## Reglas de ejecucion

- No se escribira codigo antes de definir la arquitectura tecnica minima.
- Cada fase tecnica debe tener una issue asociada.
- Cada endpoint debe responder a un caso de uso documentado.
- Cada tabla debe derivar del modelo de datos funcional.
- Cada estado debe existir en la documentacion de estados.
- No se añadira frontend complejo antes de tener flujo backend estable.
- No se introducira IA real en el prototipo inicial.

## Fuera de alcance tecnico inicial

- Docker obligatorio.
- Despliegue cloud.
- Autenticacion real con usuarios productivos.
- Integracion ERP real.
- OCR real.
- Motor de IA real.
- Multiempresa avanzado.
- Gestion documental avanzada.

## Decisiones pendientes derivadas

- Estructura de carpetas del backend.
- Estrategia de migraciones.
- Libreria de acceso a datos.
- Convencion de versionado de API.
- Formato exacto de errores.
- Stack del frontend simple.
- Estrategia inicial de testing.
