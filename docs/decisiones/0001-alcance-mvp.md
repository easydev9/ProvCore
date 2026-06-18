# Decision 0001 - Alcance del MVP

## Estado

Aceptada.

## Contexto

ProvCore ya tiene una base funcional definida: motor comun de provisiones, pedido interno, facturas, mapeo de proveedores, tarjetas corporativas, auditoria, analitica y roadmap.

Antes de decidir stack tecnico o empezar un prototipo, es necesario cerrar que debe demostrar el primer MVP. Esta decision evita construir pantallas o codigo sin una intencion funcional clara.

## Problema

El MVP puede interpretarse de varias formas:

1. Un flujo minimo centrado solo en pedido interno, provision, factura y consumo.
2. Un flujo funcional mas completo que incluya provision tardia, mapeo proveedor operativo-fiscal y analitica minima.
3. Una maqueta navegable sin logica real de dominio.

Si el alcance es demasiado pequeno, ProvCore no demuestra su valor diferencial. Si el alcance es demasiado grande, se corre el riesgo de bloquear el desarrollo por exceso de ambicion.

## Decision

El MVP objetivo de ProvCore sera la opcion 2:

```text
Flujo principal
+ provision tardia auditada
+ mapeo proveedor operativo-fiscal basico
+ auditoria
+ analitica minima
```

La construccion sera incremental. El primer incremento implementable sera:

```text
Pedido interno -> Provision -> Factura -> Consumo -> Auditoria
```

Despues se añadiran:

1. Provision tardia auditada.
2. Mapeo proveedor operativo-fiscal basico.
3. Analitica minima de provisionado, consumido, pendiente y excepciones.

## Alcance incluido

### Flujo principal

- Crear pedido interno.
- Generar `id_provision`.
- Crear provision asociada al pedido.
- Registrar factura.
- Buscar provisiones compatibles.
- Aprobar consumo total o parcial.
- Actualizar importe consumido e importe pendiente.
- Auditar cambios de estado y decisiones.

### Provision tardia

- Detectar factura sin provision compatible.
- Solicitar motivo obligatorio.
- Crear provision tardia desde la factura.
- Consumirla inmediatamente.
- Registrar auditoria completa.
- Mostrarla en reporting de excepciones.

### Mapeo proveedor operativo-fiscal basico

- Registrar proveedor operativo informado por usuario.
- Simular o registrar proveedor fiscal validado.
- Mantener separacion entre dato operativo y dato fiscal.
- Dejar claro que la IA sugiere y Administracion valida.

### Analitica minima

- Mostrar importes provisionados.
- Mostrar importes consumidos.
- Mostrar importes pendientes.
- Mostrar provisiones tardias.
- Mostrar casos bloqueados o pendientes de revision.

## Fuera de alcance inicial

- Integracion real con ERP.
- OCR productivo.
- Reglas fiscales multipais completas.
- Conciliacion bancaria real.
- Automatizacion contable sin revision humana.
- Tarjetas corporativas completas.
- Motor de IA real para validar proveedores.
- Gestion documental avanzada.

## Consecuencias

### Positivas

- El MVP demuestra el valor diferencial de ProvCore sin intentar construir un ERP.
- El flujo principal queda protegido como primer incremento.
- La provision tardia muestra control de excepciones, no solo happy path.
- El mapeo operativo-fiscal refuerza la separacion entre usuario de campo y Administracion.
- La analitica minima permite explicar impacto y seguimiento.

### Costes

- El MVP requiere mas analisis que un CRUD simple.
- Hay que definir bien estados y transiciones antes de implementar.
- La experiencia de usuario debe diferenciar roles y decisiones.
- La auditoria no puede dejarse para el final.

## Reglas derivadas

- No se empezara a programar el prototipo sin definir antes su formato y arquitectura.
- Toda funcionalidad del MVP debe vincularse a una issue.
- Cada decision relevante debe documentarse antes de ejecutarse.
- El primer incremento debe ser pequeño, verificable y trazable.
