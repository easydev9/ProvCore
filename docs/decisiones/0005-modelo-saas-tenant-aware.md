# Decision 0005 - Modelo SaaS tenant-aware

## Estado

Aceptada.

## Contexto

ProvCore se plantea como una solucion SaaS que puede implantarse en grupos empresariales con multiples sociedades y conectarse a sistemas ERP existentes.

El proyecto debe contemplar desde el diseno que un cliente puede tener varias sociedades, paises, monedas, reglas fiscales e integraciones ERP.

## Problema

Si el modelo nace como una aplicacion de una sola sociedad, sera costoso adaptarlo despues a un escenario SaaS o multipais.

El riesgo principal es mezclar datos de clientes, sociedades o paises sin una frontera clara.

## Decision

ProvCore sera tenant-aware desde el diseno.

Esto significa:

- `tenant` representa el cliente, grupo empresarial o unidad aislada del SaaS.
- `legal_entity` representa una sociedad dentro del tenant.
- las entidades operativas principales deberan poder asociarse a tenant.
- las entidades contables y fiscales deberan poder asociarse a legal entity.
- ninguna consulta futura debe cruzar tenants por accidente.

## Definiciones

### Tenant

Cliente o grupo empresarial dentro del SaaS.

Ejemplo:

```text
Tenant: Grupo empresarial
```

### Legal entity

Sociedad juridica dentro del tenant.

Ejemplo:

```text
Legal entity: Sociedad Espana
Legal entity: Sociedad Francia
Legal entity: Sociedad Alemania
```

## Reglas de modelado

Entidades que deben contemplar `tenant_id`:

- usuarios.
- legal entities.
- proveedores.
- pedidos internos.
- provisiones.
- facturas.
- eventos de auditoria.
- sugerencias de matching.
- alertas.
- eventos de integracion.

Entidades que deben contemplar `legal_entity_id`:

- pedidos internos.
- provisiones.
- facturas.
- proveedores fiscales por sociedad.
- periodos contables.
- reglas fiscales futuras.
- grupos compradores cuando aplique.
- integraciones ERP.
- alertas de cierre.

## Seguridad

El tenant es frontera de seguridad.

Regla:

```text
Un usuario no puede acceder a datos de otro tenant.
```

El MVP puede trabajar con un solo tenant inicial, pero el modelo no debe impedir anadir aislamiento real despues.

## ERP e integraciones

Cada tenant puede tener una o varias conexiones ERP.

Cada legal entity puede mapearse a una sociedad del ERP.

El routing hacia infraestructura, pools tecnicos o integraciones se define en la Decision 0006. Esta decision solo fija el modelo tenant-aware de dominio y datos.

Conceptos futuros:

- `erp_connection`.
- `erp_legal_entity_mapping`.
- `erp_supplier_mapping`.
- `integration_event`.

La integracion debe hacerse mediante puertos y adaptadores.

## Buyer groups

Los grupos compradores pueden venir del ERP o de configuracion interna.

ProvCore los modela porque son necesarios para:

- alertas.
- control de cierre.
- responsabilidad por proveedor.
- seguimiento de movimientos abiertos.
- escalado de excepciones.

La fuente de verdad puede variar por tenant.

## Consecuencias

### Positivas

- El modelo queda preparado para SaaS.
- El sistema puede soportar grupos con muchas sociedades.
- La seguridad por cliente se contempla desde el inicio.
- La analitica podra agregarse por tenant, sociedad, pais y grupo.
- Las integraciones ERP podran variar por cliente.

### Costes

- Las entidades tendran mas contexto desde el inicio.
- Las queries futuras deberan filtrar por tenant y legal entity.
- Los tests deberan validar aislamiento de datos cuando exista autenticacion real.
- El modelo fisico debe contemplar claves y relaciones adicionales.

## Reglas derivadas

- No crear entidades operativas sin considerar tenant.
- No crear entidades fiscales sin considerar legal entity.
- No asumir una sola sociedad global.
- No asumir una unica instancia ERP.
- No exponer datos cross-tenant.
- No acoplar buyer groups a un unico origen.

## Fuera de alcance inicial

- aislamiento multi-tenant productivo completo.
- facturacion SaaS.
- gestión de tenants.
- provisionamiento automatico de tenants.
- integracion real con multiples ERPs.

El MVP puede simular un tenant y varias legal entities, pero debe mantener el modelo preparado.
