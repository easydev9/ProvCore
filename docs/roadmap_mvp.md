# Roadmap MVP

## Objetivo

Definir una secuencia de trabajo para convertir ProvCore en un prototipo funcional defendible, manteniendo el foco en el flujo principal y en las excepciones que demuestran valor contable.

## Criterios de priorizacion

- Validar primero el principio central: todo gasto pasa por provision.
- Separar usuario de campo y gobierno contable.
- Demostrar trazabilidad completa con `id_provision`.
- Incluir una excepcion auditada para mostrar control realista.
- Evitar automatizacion contable sin revision humana.
- Mantener alcance acotado y sin datos internos sensibles.

## Fase 0 - Consolidacion funcional

Objetivo:

Cerrar la base documental antes de construir maqueta o prototipo.

Incluye:

- Revisar modelo de datos inicial.
- Revisar estados por entidad.
- Validar casos de uso principales.
- Ajustar diagramas de arquitectura y flujo.
- Priorizar backlog P0.
- Definir roles minimos: Responsable y Administracion.

Entregables:

- Documentacion funcional coherente.
- Diagrama de arquitectura.
- Diagrama entidad-relacion funcional.
- Backlog P0 listo para prototipo.

Riesgos a resolver:

- Estados demasiado numerosos para MVP.
- Dudas sobre si la periodificacion entra en primera version.
- Nivel de detalle de reglas contables.

## Fase 1 - Prototipo del flujo principal

Objetivo:

Demostrar el circuito completo desde compromiso de gasto hasta consumo de provision con factura.

Incluye:

- Crear pedido interno.
- Generar `id_provision`.
- Registrar proveedor operativo.
- Simular mapeo a proveedor fiscal.
- Crear provision abierta.
- Subir o registrar factura manualmente.
- Buscar provision compatible.
- Aprobar consumo.
- Actualizar importes provisionados, consumidos y pendientes.
- Registrar auditoria basica.

No incluye:

- Integracion real con ERP.
- OCR real.
- Reglas fiscales complejas.
- Tarjetas corporativas.
- Automatizacion de asientos.

Resultado esperado:

Un usuario puede recorrer el flujo:

```text
Pedido interno -> Provision -> Factura -> Consumo -> Cierre
```

Valor demostrado:

- Trazabilidad de `id_provision`.
- Separacion entre dato operativo y dato fiscal.
- Validacion por Administracion.
- Consumo total o parcial.

## Fase 2 - Excepcion de provision tardia

Objetivo:

Demostrar que el sistema no bloquea la operacion cuando llega una factura sin provision, pero mide y audita el incumplimiento.

Incluye:

- Registrar factura sin provision compatible.
- Marcar factura como pendiente de provision.
- Solicitar motivo obligatorio.
- Crear provision tardia desde factura.
- Consumir provision tardia inmediatamente.
- Registrar auditoria completa.
- Mostrar reporte de provisiones tardias.

Resultado esperado:

Un usuario puede recorrer el flujo:

```text
Factura sin provision -> Justificacion -> Provision tardia -> Consumo inmediato -> Reporting de excepcion
```

Valor demostrado:

- Control sin bloqueo operativo.
- Auditoria de excepciones.
- Indicador de cumplimiento del proceso.

## Fase 3 - Mapeo proveedor operativo-fiscal

Objetivo:

Demostrar el gobierno del dato maestro de proveedor sin exigir conocimiento fiscal al usuario de campo.

Incluye:

- Crear alias operativo.
- Sugerir proveedor fiscal.
- Mostrar confianza y origen de sugerencia.
- Validar o rechazar mapeo por Administracion.
- Reutilizar mapeo validado en futuros pedidos y facturas.

Resultado esperado:

El responsable trabaja con nombres operativos y Administracion gobierna la verdad fiscal.

Valor demostrado:

- UX simple para negocio.
- Control contable.
- IA como ayuda, no como autoridad.

## Fase 4 - Analitica minima

Objetivo:

Mostrar seguimiento operativo y contable del ciclo de provisiones.

Incluye:

- Vista general por responsable.
- Vista de provisiones abiertas.
- Vista de consumos y pendientes.
- Reporte de provisiones tardias.
- Reporte de diferencias o regularizaciones pendientes.

Resultado esperado:

Administracion puede identificar:

- gasto provisionado.
- gasto consumido.
- gasto pendiente.
- excepciones.
- casos bloqueados.

## Fase 5 - Tarjetas corporativas

Objetivo:

Extender el motor comun a un segundo origen operativo para demostrar que ProvCore no depende del pedido interno.

Incluye:

- Importar o simular movimiento de tarjeta.
- Generar provision desde movimiento.
- Asociar factura soporte.
- Marcar movimiento sin factura con motivo.
- Regularizar diferencias basicas.

Resultado esperado:

El mismo motor consume provisiones generadas por pedidos internos y por movimientos de tarjeta.

Valor demostrado:

- Arquitectura extensible.
- Reutilizacion del motor comun.
- Cobertura de un caso operativo frecuente.

## MVP definido

Alcance aprobado:

- Fase 1 completa.
- Fase 2 completa.
- Parte esencial de Fase 3.
- Analitica minima de Fase 4.

Motivo:

Este alcance permite explicar un producto completo sin construir un ERP. Demuestra criterio funcional, arquitectura, gobierno contable, trazabilidad, IA asistida y gestion de excepciones.

Decision documentada:

- [Decision 0001 - Alcance del MVP](decisiones/0001-alcance-mvp.md)
- [Decision 0002 - Formato del prototipo](decisiones/0002-formato-prototipo.md)
- [Decision 0003 - Arquitectura tecnica minima del backend](decisiones/0003-arquitectura-backend.md)

## Fuera de alcance inicial

- Integracion real con ERP.
- OCR productivo.
- Reglas fiscales multipais completas.
- Conciliacion bancaria real.
- Contabilizacion automatica sin revision.
- Aprendizaje automatico que valide proveedores sin Administracion.

## Formato del prototipo

El prototipo se construira con:

- FastAPI como backend.
- SQL Server como base de datos relacional.
- SQL Server Management Studio como herramienta de inspeccion y validacion manual.
- Frontend simple para navegar el flujo.

La ejecucion sera backend-first y por fases.

## Arquitectura backend

El backend usara una arquitectura modular orientada a clean architecture:

- dominio separado de FastAPI y SQL Server.
- modulo central `provisioning_engine`.
- modulos de entrada como adaptadores del motor comun.
- capas de dominio, application, ports, infrastructure e interface.
- implementacion pragmatica durante el MVP.
- evolucion a clean architecture mas estricta tras cerrar el MVP.

## Siguiente decision

Definir las decisiones tecnicas derivadas:

- estrategia de migraciones.
- acceso a datos.
- convencion de API.
- formato de errores.
- estrategia de testing inicial.
