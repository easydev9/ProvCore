# Casos de uso detallados

## Objetivo

Describir los casos principales del motor de provisiones desde una perspectiva funcional, con actores, precondiciones, flujo esperado, excepciones y resultado auditable.

## Actores

- Responsable: usuario que compromete el gasto o valida funcionalmente el servicio.
- Usuario financiero autorizado: usuario con permisos para validar proveedor fiscal, impuestos, cuentas, consumo y contabilizacion.
- Administrador de tenant: usuario que gestiona usuarios, roles, legal entities y configuracion funcional del tenant.
- Administrador tecnico: usuario que gestiona integraciones, routing y configuracion tecnica.
- Auditor: usuario que consulta trazabilidad sin modificar decisiones.
- Sistema: motor de provisiones, reglas, integraciones y busquedas.
- IA/OCR: componente de extraccion y sugerencia.
- ERP: fuente de datos maestros e integracion contable.

## CU-01 Crear pedido interno y provision

Objetivo:

Crear un compromiso de gasto antes de recibir la factura y generar una provision trazable.

Actores:

- Responsable.
- Sistema.
- IA/OCR si hay soporte documental.
- Usuario financiero autorizado si requiere validacion.

Precondiciones:

- El responsable tiene permisos sobre sociedad y area.
- El gasto aun no esta contabilizado.

Flujo principal:

1. El responsable crea un pedido interno.
2. Informa proveedor conocido, descripcion, sociedad, area, importe estimado, moneda, tipo de gasto y periodo.
3. El sistema valida campos obligatorios.
4. El sistema genera `id_provision`.
5. El sistema crea provision con origen `PedidoInternoProveedor`.
6. El sistema intenta localizar proveedor operativo y mapeo fiscal existente.
7. Si el mapeo esta validado, la provision queda pendiente de integracion.
8. Si falta mapeo, queda pendiente de validacion financiera.
9. El usuario financiero autorizado valida proveedor fiscal y datos contables si procede.
10. La provision queda integrada o preparada para integracion.

Excepciones:

- Proveedor desconocido: se crea proveedor operativo pendiente de mapeo.
- Importe o periodo incompleto: el pedido queda en borrador.
- Sociedad no permitida: el sistema bloquea envio.

Resultado:

- Pedido interno enviado.
- Provision creada con `id_provision`.
- Auditoria de creacion y validaciones.

## CU-02 Mapear proveedor operativo a proveedor fiscal

Objetivo:

Convertir un alias operativo informado por usuario en proveedor fiscal validado.

Actores:

- Sistema.
- IA/OCR.
- Usuario financiero autorizado.

Precondiciones:

- Existe un proveedor operativo o alias pendiente.
- Existen datos maestros ERP o historico suficiente para sugerir candidatos.

Flujo principal:

1. El sistema normaliza alias informado.
2. La IA o reglas buscan candidatos por historico, similitud, NIF/VAT, categoria, sociedad y responsable.
3. El sistema muestra candidatos con confianza y explicacion.
4. El usuario financiero autorizado selecciona proveedor fiscal correcto.
5. El sistema guarda mapeo validado.
6. El sistema desbloquea pedidos o provisiones dependientes.

Excepciones:

- Confianza baja: se exige revision manual.
- Candidato incorrecto: el usuario financiero autorizado rechaza y registra motivo.
- Proveedor no existe en ERP: queda pendiente de alta o regularizacion de maestro.

Resultado:

- Mapeo validado o rechazado.
- Historico utilizable en futuros matching.
- Auditoria completa de sugerencia y decision.

## CU-03 Subir factura y sugerir consumo de provision

Objetivo:

Procesar una factura recibida, detectar proveedor fiscal y sugerir provisiones compatibles.

Actores:

- Usuario financiero autorizado.
- Sistema.
- IA/OCR.
- Responsable.

Precondiciones:

- La factura esta disponible en buzon o carga manual.
- La sociedad puede identificarse.

Flujo principal:

1. El usuario financiero autorizado sube o recibe factura.
2. OCR/IA extrae numero, proveedor, NIF/VAT, fechas, bases, impuestos, total y moneda.
3. El sistema consulta datos maestros ERP.
4. El sistema valida o propone proveedor fiscal.
5. El sistema busca provisiones abiertas por sociedad, proveedor, responsable, periodo, importe y tipo de gasto.
6. El sistema sugiere una o varias provisiones.
7. Responsable valida que la factura corresponde al servicio.
8. El usuario financiero autorizado revisa datos contables, impuestos y consumo propuesto.
9. Se aprueba la relacion factura-provision.
10. La factura pasa a revision contable o validada.

Excepciones:

- No hay provision compatible: se activa CU-06 provision tardia.
- Proveedor detectado no coincide: se envia a mapeo o correccion.
- Proveedor fiscal no existe para la sociedad: se activa CU-13 alta de proveedor fiscal.
- Importe con diferencia: se propone regularizacion.

Resultado:

- Factura procesada.
- Provisiones sugeridas o seleccionadas.
- Auditoria de OCR, sugerencias y decisiones.

## CU-04 Una factura consume una provision

Objetivo:

Consumir total o parcialmente una provision con una factura.

Actores:

- Sistema.
- Responsable.
- Usuario financiero autorizado.

Precondiciones:

- Existe factura validable.
- Existe provision abierta compatible.

Flujo principal:

1. El sistema propone consumir una provision.
2. Responsable valida correspondencia funcional.
3. El usuario financiero autorizado confirma importe de consumo.
4. El sistema crea relacion factura-provision.
5. El sistema actualiza importe consumido e importe pendiente.
6. Si el importe pendiente es cero, la provision pasa a consumida totalmente.
7. Si queda saldo, pasa a consumida parcialmente.
8. Si hay diferencia, se marca regularizacion.

Excepciones:

- Consumo superior a provision: se exige regularizacion o aprobacion explicita.
- Provision equivocada: se rechaza sugerencia con motivo.

Resultado:

- Consumo aprobado.
- Factura vinculada a `id_provision`.
- Provision actualizada.

## CU-05 Una factura consume varias provisiones

Objetivo:

Permitir que una factura agrupada consuma varios pedidos, servicios o movimientos.

Actores:

- Sistema.
- Usuario financiero autorizado.
- Responsable.

Precondiciones:

- Existen varias provisiones abiertas compatibles.
- La factura agrupa conceptos o periodos.

Flujo principal:

1. El sistema identifica varias provisiones candidatas.
2. El usuario financiero autorizado selecciona provisiones aplicables.
3. El sistema calcula suma provisionada y compara con total/base factura.
4. Se asigna importe de consumo por provision.
5. Responsable o responsables validan los servicios si procede.
6. El usuario financiero autorizado aprueba consumos.
7. El sistema crea varias relaciones factura-provision.
8. El sistema calcula diferencias y regularizaciones.

Excepciones:

- Responsables distintos: cada responsable valida su parte o se aplica regla de delegacion.
- Diferencia no explicada: se bloquea registro hasta comentario o ajuste.

Resultado:

- Factura vinculada a varias provisiones.
- Consumos individuales auditados.

## CU-06 Factura sin provision previa

Objetivo:

Permitir continuidad operativa cuando llega una factura sin provision, dejando constancia de excepcion.

Actores:

- Usuario financiero autorizado.
- Responsable.
- Sistema.

Precondiciones:

- Existe una factura recibida.
- No se encuentra provision abierta compatible.

Flujo principal:

1. El sistema marca factura como `PendienteProvision`.
2. Responsable justifica por que no existia pedido interno.
3. El usuario financiero autorizado revisa la justificacion.
4. El usuario financiero autorizado crea provision tardia desde la factura.
5. El sistema registra `origen_provision = ProvisionTardiaDesdeFactura`.
6. La provision tardia se consume inmediatamente con la factura.
7. La factura puede continuar a validacion y registro.

Datos obligatorios:

- Motivo.
- Responsable.
- Usuario que crea.
- Fecha y hora.
- Factura origen.
- Proveedor.
- Sociedad.
- Importe.
- Comentario obligatorio.

Resultado:

- Provision tardia creada y consumida.
- Excepcion disponible en reporting.
- Auditoria completa.

## CU-07 Movimiento de tarjeta con factura

Objetivo:

Gestionar un gasto de tarjeta corporativa con provision y factura soporte.

Actores:

- Titular o responsable.
- Usuario financiero autorizado.
- Sistema.

Precondiciones:

- Existe movimiento importado de tarjeta.

Flujo principal:

1. El sistema importa movimiento.
2. El usuario clasifica gasto y confirma responsable, sociedad y area.
3. El sistema genera provision de tarjeta.
4. El usuario adjunta factura o el usuario financiero autorizado la asocia.
5. OCR/IA extrae datos de factura.
6. El sistema relaciona factura con provision del movimiento.
7. El usuario financiero autorizado valida impuestos, base y deducibilidad.
8. El sistema regulariza diferencias si procede.
9. El movimiento queda conciliado con liquidacion.

Excepciones:

- Factura agrupada: se aplica CU-08.
- Diferencia por divisa: se genera regularizacion.

Resultado:

- Movimiento con provision consumida.
- Factura soporte asociada.
- Liquidacion conciliable.

## CU-08 Factura agrupada para varios movimientos de tarjeta

Objetivo:

Permitir que una factura justifique varios movimientos de tarjeta.

Actores:

- Usuario financiero autorizado.
- Sistema.
- Responsable.

Precondiciones:

- Existen varios movimientos con provisiones abiertas.
- Existe una factura agrupada.

Flujo principal:

1. El usuario financiero autorizado selecciona factura agrupada.
2. El sistema busca movimientos compatibles por proveedor, fechas, importes y titular.
3. El usuario financiero autorizado selecciona movimientos incluidos.
4. El sistema compara total factura contra suma de movimientos.
5. Se crean consumos contra cada provision.
6. Se calculan diferencias por impuestos, base o divisa.
7. Se aprueban regularizaciones.

Resultado:

- Factura asociada a N movimientos.
- N provisiones consumidas total o parcialmente.
- Diferencias trazadas.

## CU-09 Movimiento sin factura

Objetivo:

Cerrar un movimiento de tarjeta sin factura soporte cuando el proceso lo permita.

Actores:

- Responsable.
- Usuario financiero autorizado.
- Sistema.

Precondiciones:

- Existe movimiento de tarjeta con provision.
- No se ha recibido factura tras plazo o por naturaleza del gasto.

Flujo principal:

1. El responsable marca movimiento como sin factura.
2. Informa motivo obligatorio.
3. El usuario financiero autorizado revisa deducibilidad y tratamiento fiscal.
4. El sistema genera regularizacion si procede.
5. El movimiento queda reportado como sin factura.

Resultado:

- Movimiento cerrado o regularizado.
- Importe disponible en reporting de sin factura/no deducible.

## CU-10 Periodificar factura

Objetivo:

Distribuir un gasto entre periodos cuando factura o provision cubren mas de un periodo.

Actores:

- Sistema.
- Usuario financiero autorizado.

Precondiciones:

- Factura o provision tiene periodo de servicio superior a un periodo contable.

Flujo principal:

1. El sistema detecta periodo plurimensual o anual.
2. El sistema sugiere reparto por dias, meses o criterio configurado.
3. El usuario financiero autorizado acepta, modifica o rechaza periodificacion.
4. El sistema crea lineas de periodificacion.
5. La integracion contable usa el reparto aprobado.

Resultado:

- Periodificacion aprobada o descartada.
- Auditoria de criterio aplicado.

## CU-11 Regularizar diferencias

Objetivo:

Ajustar diferencias entre provision y realidad de factura, impuestos, divisa, liquidacion o deducibilidad.

Actores:

- Sistema.
- Usuario financiero autorizado.

Precondiciones:

- Existe consumo aprobado con diferencia o clasificacion fiscal especial.

Flujo principal:

1. El sistema calcula diferencia.
2. Clasifica tipo de regularizacion.
3. El usuario financiero autorizado revisa importe, signo, cuenta conceptual y motivo.
4. Se aprueba regularizacion.
5. Se integra o registra asiento conceptual.

Resultado:

- Regularizacion aprobada e integrada.
- Provision y factura coherentes para analitica.

## CU-12 Consultar analitica

Objetivo:

Permitir seguimiento operativo y contable de provisiones, facturas, consumos y excepciones.

Actores:

- Responsable.
- Usuario financiero autorizado.

Precondiciones:

- El usuario tiene permisos sobre su ambito.

Flujo principal:

1. El usuario accede a vista general.
2. Filtra por periodo, proveedor, sociedad, area, estado o moneda.
3. El sistema muestra importes provisionados, consumidos y pendientes.
4. El usuario baja a vista detallada.
5. El usuario financiero autorizado puede acceder a vista contable analitica dentro de su alcance.

Resultado:

- Seguimiento por responsable y usuario financiero autorizado.
- Exportacion o reporting de excepciones.

## CU-13 Alta de proveedor fiscal desde factura

Objetivo:

Bloquear y resolver una factura cuyo proveedor fiscal no existe en ERP para la legal entity correspondiente.

Actores:

- Usuario financiero autorizado.
- Sistema.
- IA/OCR.
- ERP.

Precondiciones:

- Existe una factura procesada por OCR o carga manual.
- El proveedor fiscal detectado no existe o no esta validado para la legal entity.

Flujo principal:

1. OCR/IA o el usuario financiero autorizado detecta datos fiscales del proveedor.
2. El sistema consulta el ERP o maestro simulado por tenant y legal entity.
3. El sistema confirma que el proveedor no existe para esa sociedad.
4. La factura pasa a `PendienteAltaProveedor`.
5. El sistema crea `solicitud_alta_proveedor`.
6. El usuario financiero autorizado valida datos minimos del proveedor.
7. El sistema marca la solicitud como lista para envio ERP.
8. El adaptador ERP envia la solicitud o simula la respuesta en MVP.
9. El ERP confirma creacion o validacion satisfactoria.
10. El sistema asocia proveedor fiscal resultante a la factura.
11. La factura se desbloquea y continua hacia busqueda de provision.

Excepciones:

- ERP rechaza la creacion: la solicitud queda en `FallidaERP` con motivo.
- Datos fiscales incompletos: el usuario financiero autorizado corrige antes de enviar.
- Ya existe proveedor equivalente: el usuario financiero autorizado vincula el proveedor correcto y cancela la solicitud.

Resultado:

- Proveedor fiscal validado para la legal entity.
- Factura desbloqueada.
- Auditoria de bloqueo, validacion, envio y confirmacion.
- Evento de proceso para medir tiempo de alta proveedor.

## CU-14 Generar alertas de cierre operativo

Objetivo:

Avisar a usuarios o grupos responsables sobre pendientes que pueden afectar al cierre.

Actores:

- Sistema.
- Usuario financiero autorizado.
- Responsable.
- Grupo comprador.

Precondiciones:

- Existe un periodo de cierre configurado.
- Existen proveedores, grupos responsables o asignaciones vigentes.

Flujo principal:

1. El sistema identifica el periodo de cierre activo o proximo.
2. Busca provisiones abiertas, facturas bloqueadas, proveedores pendientes, movimientos sin factura y regularizaciones pendientes.
3. Determina el grupo responsable mediante `supplier_responsibility`.
4. Crea alertas por usuario o buyer group.
5. Notifica a responsables.
6. El responsable reconoce o resuelve la alerta.
7. El usuario financiero autorizado revisa pendientes criticos antes del cierre.
8. El sistema registra resolucion o escalado.

Excepciones:

- No existe grupo responsable: la alerta se dirige a usuario financiero autorizado.
- La alerta vence sin respuesta: el sistema escala.
- El periodo ya esta cerrado: cualquier reapertura exige motivo auditado.

Resultado:

- Pendientes de cierre visibles y asignados.
- Tiempos de resolucion medibles.
- Auditoria y eventos de proceso disponibles para analitica.
