# Definition of Done

## Objetivo

Definir cuando una tarea de ProvCore puede considerarse terminada.

Esta definicion aplica a documentacion, decisiones, issues e implementacion futura.

## Regla general

Una tarea no esta terminada solo porque el cambio funcione localmente.

Debe quedar:

- entendida.
- documentada cuando aplique.
- vinculada a una decision o issue.
- revisable por otro agente o desarrollador.
- alineada con la arquitectura aprobada.

## Para cualquier tarea

Una tarea esta terminada si cumple:

- La issue relacionada esta identificada.
- El cambio responde al objetivo de la issue.
- No introduce cambios no relacionados.
- No contradice decisiones existentes.
- La documentacion afectada esta actualizada.
- El repositorio queda sin cambios pendientes no intencionados.
- El commit es pequeño y descriptivo.

## Para decisiones

Una decision esta terminada si cumple:

- Tiene documento en `docs/decisiones/`.
- Explica contexto, problema, decision, consecuencias y reglas derivadas.
- Indica alternativas cuando sean relevantes.
- Esta enlazada desde `README.md` si afecta al proyecto general.
- Esta enlazada desde `docs/roadmap_mvp.md` si afecta al MVP o arquitectura.
- La issue de decision queda comentada y cerrada en GitHub.

## Para documentacion funcional

Una tarea documental esta terminada si cumple:

- Usa lenguaje consistente con el glosario.
- No introduce nombres internos sensibles.
- No usa em dash.
- Mantiene tono de proyecto real.
- Explica el por que ademas del que cuando afecta a diseño o arquitectura.
- Mantiene coherencia con principios, estados y casos de uso.

## Para cambios de dominio

Un cambio de dominio esta terminado si cumple:

- La regla de negocio esta documentada.
- La entidad o caso de uso afectado esta identificado.
- Los estados afectados estan revisados.
- Las excepciones relevantes estan contempladas.
- Auditoria queda considerada si hay decision, cambio de estado o excepcion.
- Tenant y legal entity quedan considerados si el cambio toca datos operativos, fiscales o analiticos.
- El dominio no depende de FastAPI, SQL Server, ORM ni frameworks.

## Para cambios de base de datos

Un cambio de base de datos estara terminado si cumple:

- Existe migracion o script versionado segun la decision de persistencia vigente.
- Las claves primarias estan definidas.
- Las claves foraneas estan definidas cuando aplique.
- Los tipos monetarios usan precision decimal.
- Los campos de estado tienen valores controlados.
- Los indices necesarios para el flujo principal estan identificados.
- Las claves o filtros de tenant y legal entity estan contemplados cuando aplique.
- El cambio se puede validar en SQL Server Management Studio.

## Para cambios de API

Un cambio de API estara terminado si cumple:

- El endpoint responde a un caso de uso documentado.
- La ruta sigue la convencion de versionado vigente.
- Los schemas de entrada y salida estan definidos.
- Los errores esperados estan definidos.
- Los limites de acceso por tenant, legal entity y rol estan considerados cuando aplique.
- La ruta no contiene logica de negocio.
- La ruta llama a application, no a infrastructure directamente.

## Para cambios de backend

Un cambio de backend estara terminado si cumple:

- Respeta la arquitectura modular aprobada.
- Mantiene separacion entre domain, application, ports, infrastructure e interface.
- No introduce acceso directo a SQL Server fuera de infrastructure.
- No introduce FastAPI fuera de interface.
- No usa modelos ORM como entidades de dominio.
- Incluye tests cuando toca reglas de dominio o casos de uso.
- Mantiene trazabilidad con auditoria cuando aplica.

## Para tests

Una tarea con logica debe tener pruebas proporcionales al riesgo.

Minimos esperados:

- Reglas de dominio: tests unitarios sin base de datos.
- Casos de uso: tests con repositorios fake o dobles.
- Endpoints: tests de API para flujos principales.
- Persistencia: tests de integracion cuando se validen repositories reales.

## Para cierre de issue

Una issue puede cerrarse si:

- El criterio de aceptacion esta cubierto.
- Hay comentario de cierre cuando representa una decision.
- La documentacion asociada esta enlazada.
- Los commits relevantes estan subidos.
- No quedan dudas abiertas dentro de la propia issue.

## Criterio de rechazo

Un cambio no debe aceptarse si:

- Mezcla negocio con persistencia.
- Mezcla negocio con HTTP.
- Duplica reglas del motor `provisioning_engine` en modulos de entrada.
- Introduce una dependencia sin justificar.
- Cierra una decision sin documentarla.
- Genera codigo antes de cerrar la decision arquitectonica correspondiente.
