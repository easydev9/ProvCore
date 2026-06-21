# Backlog de issues inicial

## Objetivo

Convertir el backlog funcional en issues accionables para fases de discovery, prototipo y validacion con usuarios financieros autorizados.

Las prioridades son orientativas:

- P0: imprescindible para validar el flujo central.
- P1: necesario para un MVP serio.
- P2: mejora o ampliacion posterior.

## Epic 0 - Base SaaS y dominio comun

### P0 - Modelar tenant y legal entity

Como equipo de producto, quiero distinguir tenant y legal entity desde el inicio, para que el sistema pueda evolucionar a SaaS y multipais sin redisenar el dominio.

Criterios de aceptacion:

- Define tenant como frontera funcional y futura frontera de seguridad.
- Define legal entity como sociedad juridica dentro del tenant.
- Identifica entidades que deben llevar `tenant_id`.
- Identifica entidades que deben llevar `legal_entity_id`.
- Documenta impacto en permisos, reporting e integraciones ERP.

### P0 - Definir movimiento provisionable como abstraccion central

Como equipo de arquitectura, quiero que pedidos, tarjetas, facturas tardias y origenes futuros implementen un contrato comun, para que el motor de provisiones no dependa de cada caso concreto.

Criterios de aceptacion:

- Define metodos conceptuales de `ProvisionableMovement`.
- Identifica origen, tenant, legal entity, responsable, proveedor, importe, moneda y periodo.
- Explica que cada origen aporta datos a su manera.
- Evita convertir la API en CRUD de tablas.

### P1 - Definir routing funcional multi-sociedad

Como equipo de arquitectura, quiero separar routing funcional y balanceo tecnico, para poder operar multiples sociedades sin mezclar contexto de negocio, permisos e infraestructura.

Criterios de aceptacion:

- Define contexto minimo de routing.
- Diferencia routing funcional de balanceo tecnico.
- Define pool autorizado.
- Indica que el dominio no conoce reglas de infraestructura.
- Incluye observabilidad minima de decisiones de routing.
- Deja alcance MVP y evolucion futura documentados.

### P0 - Definir contratos API MVP

Como equipo de arquitectura, quiero definir endpoints orientados a casos de uso, para implementar FastAPI manteniendo separadas las responsabilidades de interface, application y dominio.

Criterios de aceptacion:

- Define prefijo `/api/v1`.
- Define endpoints P0 para pedido interno, provision, factura, consumo, provision tardia y auditoria.
- Declara actor, permiso y contexto requerido por endpoint.
- Define formato comun de respuesta y error.
- Traduce errores de dominio a HTTP desde interface.
- Mantiene reglas de negocio fuera de routers.

## Epic 1 - Modelo comun de provisiones

### P0 - Definir contrato funcional de Provisionable

Como equipo de producto, quiero definir un contrato comun para cualquier origen de provision, para que pedidos internos, tarjetas y provisiones tardias usen el mismo motor.

Criterios de aceptacion:

- Incluye origen, sociedad, responsable, proveedor operativo, proveedor fiscal, importe, moneda, periodo y estado.
- Define reglas minimas de consumo y regularizacion.
- Distingue datos obligatorios del origen y datos validados por usuario financiero autorizado.

### P0 - Crear entidad provision

Como sistema, quiero registrar provisiones con ID unico, para trazar todo el ciclo desde compromiso hasta contabilizacion.

Criterios de aceptacion:

- Genera `id_provision` unico.
- Guarda importe provisionado, consumido y pendiente.
- Guarda origen y entidad origen.
- Soporta estados iniciales definidos.
- Registra auditoria de creacion.

### P0 - Consumir provision total o parcialmente

Como usuario financiero autorizado, quiero aprobar consumos de provision contra factura, para reflejar la realidad del gasto.

Criterios de aceptacion:

- Permite consumo total.
- Permite consumo parcial.
- Actualiza importe pendiente.
- Cambia estado segun saldo.
- Registra usuario, fecha y motivo si hay diferencia.

### P1 - Regularizar diferencias

Como usuario financiero autorizado, quiero generar regularizaciones cuando provision y factura no coincidan, para mantener coherencia contable y analitica.

Criterios de aceptacion:

- Detecta diferencia de importe.
- Permite clasificar tipo de regularizacion.
- Requiere motivo.
- Mantiene estado de revision e integracion.

## Epic 2 - Pedido interno

### P0 - Crear pedido interno de gasto

Como responsable, quiero notificar un gasto comprometido sin conocer datos fiscales, para que el sistema genere la provision antes de la factura.

Criterios de aceptacion:

- Solicita sociedad, area, proveedor conocido, descripcion, importe, moneda, tipo de gasto y periodo.
- No exige NIF/VAT ni codigo ERP al responsable.
- Permite adjuntar soporte opcional.
- Genera o reserva `id_provision` al enviar.

### P0 - Enviar pedido y generar provision

Como sistema, quiero crear provision automaticamente al enviar pedido, para asegurar trazabilidad.

Criterios de aceptacion:

- Crea provision con origen `PedidoInternoProveedor`.
- Copia responsable, sociedad, area, importe, moneda y periodo.
- Evalua si proveedor fiscal esta mapeado.
- Deja estado pendiente si requiere validacion.

### P1 - Cancelar pedido con motivo

Como responsable o usuario financiero autorizado, quiero cancelar un pedido con motivo, para evitar provisiones abiertas incorrectas.

Criterios de aceptacion:

- Permite cancelar antes de integracion sin asiento.
- Si hay provision integrada, exige tratamiento de anulacion.
- Audita motivo y usuario.

## Epic 3 - Mapeo de proveedores

### P0 - Registrar proveedor operativo

Como sistema, quiero guardar el proveedor tal como lo informa el usuario, para no exigir datos fiscales en campo.

Criterios de aceptacion:

- Guarda alias informado.
- Normaliza alias para busqueda.
- Lo asocia a responsable, area y categoria si aplica.

### P0 - Sugerir proveedor fiscal

Como usuario financiero autorizado, quiero ver candidatos de proveedor fiscal con confianza y explicacion, para validar mas rapido.

Criterios de aceptacion:

- Sugiere por historico, alias, NIF/VAT, sociedad, categoria o similitud.
- Muestra nivel de confianza.
- Muestra origen de la sugerencia.
- No valida automaticamente.

### P0 - Validar mapeo proveedor

Como usuario financiero autorizado, quiero validar el proveedor fiscal correcto, para convertirlo en fuente de verdad operativa.

Criterios de aceptacion:

- Solo roles autorizados pueden validar.
- Guarda proveedor fiscal validado.
- Desbloquea provisiones pendientes.
- Audita decision.

### P1 - Rechazar o corregir mapeo

Como usuario financiero autorizado, quiero rechazar sugerencias incorrectas, para mejorar la calidad futura del matching.

Criterios de aceptacion:

- Requiere motivo.
- Guarda candidato rechazado.
- Permite seleccionar candidato alternativo.

### P1 - Alta de proveedor fiscal para legal entity

Como usuario financiero autorizado, quiero solicitar alta o validacion de proveedor fiscal cuando una factura llega con proveedor inexistente en ERP, para no continuar el registro sin maestro valido.

Criterios de aceptacion:

- Detecta proveedor fiscal inexistente por tenant y legal entity.
- Bloquea factura afectada.
- Crea solicitud de alta proveedor.
- Permite validacion de usuario financiero autorizado antes de envio ERP.
- Permite simular confirmacion ERP en MVP.
- Desbloquea factura tras confirmacion satisfactoria.
- Audita bloqueo, envio, confirmacion o fallo.

## Epic 4 - Facturas de proveedor

### P0 - Procesar factura con OCR/IA

Como usuario financiero autorizado, quiero extraer datos de factura, para buscar provisiones compatibles y preparar validacion.

Criterios de aceptacion:

- Extrae proveedor, NIF/VAT, numero, fechas, base, impuestos, total y moneda.
- Permite correccion manual.
- Consulta datos maestros ERP.

### P0 - Buscar provisiones abiertas compatibles

Como sistema, quiero buscar provisiones abiertas al recibir factura, para sugerir consumo.

Criterios de aceptacion:

- Filtra por sociedad, proveedor fiscal, proveedor operativo, responsable, periodo, moneda e importe.
- Devuelve candidatos ordenados por confianza.
- Explica criterio de coincidencia.

### P0 - Aprobar relacion factura-provision

Como usuario financiero autorizado, quiero aprobar la relacion entre factura y provision, para consumir la provision correcta.

Criterios de aceptacion:

- Permite una factura contra una provision.
- Permite una factura contra varias provisiones.
- Permite una provision contra varias facturas.
- Audita aprobacion.

### P0 - Crear provision tardia

Como usuario financiero autorizado, quiero crear una provision tardia cuando no exista provision previa, para no bloquear la operacion y medir incumplimientos.

Criterios de aceptacion:

- Solo se crea desde factura.
- Requiere motivo, responsable, usuario, fecha, factura, sociedad, proveedor e importe.
- Se consume inmediatamente.
- Aparece en reporting de excepciones.

### P1 - Registrar factura para integracion

Como usuario financiero autorizado, quiero marcar una factura como registrada, para enviarla al ERP cuando este validada.

Criterios de aceptacion:

- Requiere proveedor fiscal validado.
- Requiere consumo de provision o provision tardia.
- Requiere revision contable completada.

## Epic 5 - Tarjetas corporativas

### P1 - Importar movimiento de tarjeta

Como sistema, quiero importar movimientos de tarjeta, para iniciar provision y seguimiento documental.

Criterios de aceptacion:

- Guarda fecha, comercio, importe, moneda, titular y sociedad.
- Permite clasificacion por usuario.
- Genera provision.

### P1 - Asociar factura a movimiento de tarjeta

Como usuario financiero autorizado, quiero asociar factura soporte a un movimiento, para consumir la provision de tarjeta.

Criterios de aceptacion:

- Relaciona factura con movimiento.
- Consume provision asociada.
- Calcula diferencias de base, impuestos o divisa.

### P1 - Marcar movimiento sin factura

Como responsable, quiero marcar un movimiento sin factura con motivo, para cerrar casos permitidos y reportarlos.

Criterios de aceptacion:

- Motivo obligatorio.
- Revision de usuario financiero autorizado.
- Clasificacion deducible/no deducible/pendiente.
- Reporting especifico.

### P2 - Asociar factura agrupada a varios movimientos

Como usuario financiero autorizado, quiero asociar una factura a varios movimientos, para gestionar cargos agrupados.

Criterios de aceptacion:

- Selecciona N movimientos.
- Compara total factura contra suma movimientos.
- Genera consumos por provision.
- Regulariza diferencias.

## Epic 6 - Auditoria y gobierno

### P0 - Auditar cambios de estado

Como auditor, quiero consultar cambios de estado, para reconstruir el ciclo de decision.

Criterios de aceptacion:

- Guarda entidad, estado anterior, estado nuevo, usuario, fecha y motivo.
- Aplica a pedido, provision, factura, relacion, mapeo y regularizacion.

### P0 - Auditar decisiones financieras autorizadas

Como auditor, quiero ver decisiones contables y fiscales, para justificar la verdad final.

Criterios de aceptacion:

- Audita validacion de proveedor fiscal.
- Audita aprobacion de consumo.
- Audita regularizaciones.
- Audita provision tardia.

### P1 - Reportar excepciones

Como usuario financiero autorizado, quiero reportar provisiones tardias, sin factura y no deducibles, para medir cumplimiento del proceso.

Criterios de aceptacion:

- Filtro por periodo, responsable, sociedad, area y proveedor.
- Exportable.
- Incluye motivo y usuario.

## Epic 7 - Analitica

### P1 - Vista general por responsable

Como responsable, quiero ver mis proveedores, provisiones y facturas pendientes, para gestionar mi ambito.

Criterios de aceptacion:

- Muestra provisionado, consumido y pendiente.
- Muestra facturas pendientes de validar.
- Muestra provisiones abiertas y tardias.
- Respeta permisos.

### P1 - Vista detallada por provision

Como usuario financiero autorizado, quiero consultar cada provision con sus facturas, consumos y regularizaciones, para revisar trazabilidad.

Criterios de aceptacion:

- Muestra pedido/movimiento origen.
- Muestra proveedor operativo y fiscal.
- Muestra factura_provision.
- Muestra auditoria relevante.

### P2 - Vista contable analitica

Como usuario financiero autorizado, quiero analizar gasto provisionado, consumido, pendiente, no deducible y regularizado, para seguimiento contable.

Criterios de aceptacion:

- Filtros por sociedad, area, proveedor, periodo, moneda, estado y deducibilidad.
- Incluye regularizaciones.
- Exportable.

### P1 - Registrar eventos de proceso

Como equipo de producto, quiero registrar eventos estructurados del flujo, para medir tiempos, bloqueos, conversiones y eficiencia operativa.

Criterios de aceptacion:

- Registra eventos de movimiento identificado, provision creada, proveedor bloqueado, matching sugerido, consumo aprobado y alerta resuelta.
- Incluye tenant, legal entity, entidad, id entidad y correlacion de proceso.
- Distingue evento analitico de auditoria de decision.
- Permite calcular metricas basicas de cierre y operacion.

### P1 - Generar alertas de cierre

Como usuario financiero autorizado, quiero generar alertas por proveedor, grupo comprador y periodo, para limpiar pendientes antes del cierre.

Criterios de aceptacion:

- Detecta provisiones abiertas, facturas bloqueadas, proveedores pendientes y regularizaciones pendientes.
- Determina grupo responsable por supplier responsibility.
- Crea alerta con fecha objetivo.
- Permite resolver, cerrar o escalar.
- Alimenta reporting de cumplimiento de cierre.

## Epic 8 - Integracion ERP conceptual

### P1 - Preparar asiento conceptual de provision

Como usuario financiero autorizado, quiero preparar el asiento conceptual de provision, para integrarlo segun reglas ERP.

Criterios de aceptacion:

- Define debe/haber conceptual.
- Usa proveedor fiscal validado y dimension financiera.
- Mantiene estado de integracion.

### P1 - Preparar asiento conceptual de factura

Como usuario financiero autorizado, quiero preparar asiento de factura consumiendo provision, para evitar doble impacto en resultados.

Criterios de aceptacion:

- Usa relacion factura-provision aprobada.
- Registra consumo de provision.
- Marca factura como registrada antes de contabilizar.

### P2 - Versionar reglas contables y fiscales

Como usuario financiero autorizado, quiero versionar reglas, para explicar por que se aplico un criterio en una fecha concreta.

Criterios de aceptacion:

- Guarda version de regla.
- Guarda vigencia.
- Relaciona regla aplicada con provision, factura o regularizacion.
