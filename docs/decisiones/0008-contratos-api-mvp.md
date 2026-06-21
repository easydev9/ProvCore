# Decisión 0008 - Contratos API del MVP

## Estado

Aceptada.

## Contexto

ProvCore ya tiene definidas las decisiones principales de dominio, arquitectura, persistencia, modelo SaaS tenant-aware, routing multi-sociedad y autorización.

El siguiente paso es transformar los casos de uso del MVP en contratos API suficientemente concretos para poder implementar el backend con FastAPI sin convertir el sistema en un CRUD de tablas.

## Problema

Si la API se diseña directamente desde las tablas, aparecerán problemas:

- reglas de negocio dentro de routers.
- endpoints acoplados a persistencia.
- operaciones críticas sin auditoría clara.
- permisos ambiguos.
- falta de contexto tenant y legal entity.
- dificultad para representar acciones como aprobar consumo, crear provisión tardía o validar proveedor fiscal.

ProvCore necesita una API orientada a casos de uso y no a edición genérica de entidades.

## Decisión

La API del MVP expondrá casos de uso.

Regla:

```text
La API ejecuta intenciones de negocio. No expone CRUD libre de tablas.
```

La convención base será:

```text
/api/v1
```

Cada endpoint deberá declarar:

- actor esperado.
- permiso requerido.
- contexto obligatorio.
- caso de uso de application.
- auditoría o evento generado.
- errores esperados.

## Contexto obligatorio

Toda petición protegida deberá resolverse con:

- `tenant_id`.
- `user_id`.
- roles.
- permisos.
- `correlation_id`.

Las operaciones fiscales, contables o de provisión deberán incluir además:

- `legal_entity_id`.

## Formato estándar de respuesta

Las respuestas de comandos devolverán el recurso principal afectado y metadatos mínimos:

```json
{
  "data": {},
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_123"
  }
}
```

Las respuestas de consulta devolverán:

```json
{
  "data": [],
  "meta": {
    "correlation_id": "corr_123",
    "pagination": {
      "limit": 50,
      "offset": 0,
      "total": 120
    }
  }
}
```

## Formato estándar de error

Los errores seguirán un formato común:

```json
{
  "error": {
    "code": "PROVISION_NOT_CONSUMABLE",
    "message": "La provisión no puede consumirse en su estado actual.",
    "details": {},
    "correlation_id": "corr_123"
  }
}
```

## Códigos HTTP

Uso base:

- `200 OK`: consulta o acción completada.
- `201 Created`: recurso creado.
- `202 Accepted`: operación aceptada para proceso posterior o simulación externa.
- `400 Bad Request`: payload inválido o regla básica incumplida.
- `401 Unauthorized`: usuario no autenticado.
- `403 Forbidden`: usuario autenticado sin permiso o alcance suficiente.
- `404 Not Found`: recurso inexistente dentro del alcance permitido.
- `409 Conflict`: conflicto de estado o concurrencia funcional.
- `422 Unprocessable Entity`: datos formalmente válidos pero no procesables por regla de dominio.
- `500 Internal Server Error`: error inesperado.

## Endpoints P0 del MVP

El primer bloque implementable cubrirá:

- crear pedido interno.
- generar provisión desde pedido interno.
- registrar factura.
- buscar provisiones compatibles.
- aprobar consumo factura-provisión.
- crear provisión tardía auditada.
- consultar auditoría básica.

## Endpoints P1 del MVP ampliado

El segundo bloque cubrirá:

- validar mapeo proveedor operativo-fiscal.
- solicitar alta de proveedor fiscal.
- confirmar alta ERP simulada.
- consultar analítica mínima.
- generar alertas de cierre.

## Seguridad

La API no confiará en campos enviados por el cliente para determinar autoridad.

El cliente puede enviar `tenant_id` y `legal_entity_id` como contexto funcional, pero el backend debe validar:

- que el usuario pertenece al tenant.
- que tiene acceso a la legal entity.
- que tiene el permiso requerido.
- que la operación es válida para el estado actual.

## Auditoría

Toda acción que cambie estado o represente una decisión debe generar auditoría.

Como mínimo:

- usuario.
- rol usado.
- permiso usado.
- tenant.
- legal entity cuando aplique.
- entidad.
- acción.
- estado anterior.
- estado posterior.
- motivo cuando aplique.
- `correlation_id`.

## Consecuencias

### Positivas

- La API queda alineada con casos de uso.
- Se protege el dominio frente a HTTP.
- Se prepara seguridad real desde el diseño.
- Se mantiene trazabilidad.
- Se facilita implementar FastAPI con routers finos y application use cases.

### Costes

- Hay más trabajo inicial de contrato.
- Cada endpoint debe declarar permisos y errores.
- Los schemas deben diferenciar comandos de consultas.
- El frontend tendrá que trabajar con acciones explícitas.

## Reglas derivadas

- No crear endpoints genéricos de actualización libre para entidades críticas.
- No aprobar consumos con un simple `PATCH` de estado.
- No crear provisiones tardías sin motivo.
- No registrar factura definitivamente sin flujo de provisión.
- No resolver permisos en dominio.
- No acceder a repositories desde routers.
- Traducir errores de dominio a HTTP en interface.
