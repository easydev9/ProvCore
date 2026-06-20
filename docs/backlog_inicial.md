# Backlog inicial

Este documento mantiene la vision por epicas. Para una lista mas accionable de issues, ver [Backlog de issues inicial](issues_backlog.md).

## Epicas

### Pedido interno

- Crear pedido interno o compromiso de gasto.
- Generar ID de provision.
- Asociar responsable, sociedad, area, importe, moneda y proveedor informado.
- Permitir proveedor fiscal pendiente de validacion.

### Motor de provisiones

- Crear provisiones desde distintos origenes.
- Consumir provisiones total o parcialmente.
- Relacionar una factura con una o varias provisiones.
- Relacionar una provision con una o varias facturas.
- Calcular regularizaciones.

### Mapeo de proveedores

- Guardar proveedor informado por usuario.
- Sugerir proveedor fiscal mediante IA/historico.
- Validar mapeo por usuario financiero autorizado.
- Mantener tabla de alias operativos.

### Modulo de facturas de proveedor

- Buscar provisiones abiertas al subir factura.
- Sugerir consumo de provision.
- Crear provision tardia como excepcion auditada.
- Guardar ID_PROVISION en factura.

### Modulo de tarjetas corporativas

- Generar provisiones desde movimientos de tarjeta corporativa.
- Gestionar movimientos sin factura.
- Asociar facturas agrupadas a varios movimientos.
- Regularizar por IVA/base y divisa.
- Conciliar con liquidacion bancaria.

### Analitica de proveedores y provisiones

- Crear vista general por responsable, proveedor, sociedad, area y periodo.
- Crear vista detallada de provisiones, consumos, facturas y regularizaciones.
- Crear vista contable analitica con gasto provisionado, gasto consumido, gasto pendiente, no deducibles y movimientos sin factura.
- Permitir filtros tipo ERP por estado, proveedor, responsable, moneda, periodo, sociedad y tipo de gasto.
- Permitir exportacion para seguimiento operativo, fiscal y contable.

### Auditoria y reporting

- Auditar cambios de estado y decisiones.
- Reportar provisiones tardias.
- Reportar movimientos sin factura.
- Reportar no deducibles y parcialmente deducibles.
