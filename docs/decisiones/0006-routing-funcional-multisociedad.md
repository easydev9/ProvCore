# Decision 0006 - Routing funcional multi-sociedad

## Estado

Aceptada.

## Contexto

ProvCore esta pensado para operar en grupos con multiples sociedades, paises, ERPs e infraestructuras posibles.

Una peticion puede afectar a una sociedad concreta, a una conexion ERP concreta o a una region concreta. Por tanto, el sistema debe saber decidir donde se procesa una peticion antes de aplicar balanceo tecnico.

## Problema

Si el reparto de peticiones se decide solo por carga tecnica, se pueden producir errores graves:

- procesar datos en una infraestructura no autorizada.
- cruzar datos entre tenants.
- enviar operaciones a una sociedad incorrecta.
- usar una conexion ERP que no corresponde.
- incumplir restricciones de residencia del dato.
- perder trazabilidad sobre por que una peticion se proceso en un destino concreto.

El balanceo tecnico es necesario, pero no puede sustituir a la decision funcional.

## Decision

ProvCore separara dos niveles:

1. Routing funcional.
2. Balanceo tecnico.

El routing funcional resuelve el contexto de negocio de la peticion:

- tenant.
- legal entity.
- usuario.
- rol.
- pais.
- residencia del dato.
- ERP asociado.
- tipo de operacion.
- pool de infraestructura autorizado.

Despues de resolver ese destino funcional, el balanceo tecnico distribuye la carga dentro del pool autorizado.

## Arquitectura conceptual

```text
Peticion API
-> autenticacion y autorizacion
-> resolucion de tenant y legal entity
-> politica de routing funcional
-> seleccion de pool autorizado
-> balanceo tecnico dentro del pool
-> instancia ProvCore
-> base de datos e integraciones permitidas
```

## Componentes

### RoutingContextResolver

Responsable de construir el contexto funcional de la peticion.

Debe obtener:

- tenant.
- legal entity.
- usuario.
- roles.
- permisos.
- operacion solicitada.
- correlacion de proceso.

### RoutingPolicy

Responsable de decidir el pool permitido.

Puede usar:

- tenant.
- legal entity.
- pais.
- tipo de operacion.
- ERP asociado.
- estado de integracion.
- reglas de residencia del dato.

### InfrastructurePool

Conjunto de instancias tecnicas autorizadas para procesar un contexto funcional.

Ejemplos:

- pool comun de MVP.
- pool por region.
- pool por grupo de sociedades.
- pool dedicado para una sociedad critica.

### TechnicalLoadBalancer

Responsable de repartir carga dentro del pool ya seleccionado.

Estrategias posibles:

- round robin ponderado.
- menor numero de conexiones.
- menor tiempo de respuesta.
- capacidad disponible.
- combinacion de metricas.

## Regla principal

```text
Routing funcional primero. Balanceo tecnico despues.
```

## Observabilidad requerida

Cada decision de routing relevante debe poder reconstruirse.

Datos minimos:

- tenant.
- legal entity.
- usuario o servicio.
- operacion.
- pool seleccionado.
- instancia seleccionada si aplica.
- motivo de seleccion.
- timestamp.
- correlacion de proceso.
- resultado.

## Seguridad

Reglas:

- Si no se puede resolver tenant, la peticion se rechaza.
- Si no se puede resolver legal entity cuando es obligatoria, la peticion se rechaza.
- Si no existe pool autorizado, la peticion se rechaza.
- Un fallback solo puede ocurrir dentro de un pool autorizado.
- El dominio no debe conocer reglas de infraestructura.

## MVP

El MVP no necesita un balanceador productivo avanzado.

Alcance minimo:

- tenant y legal entity presentes en el contexto de peticion.
- pool unico o simulado.
- politica de routing documentada.
- logs de decision basicos.
- health check basico de servicio.

No entra en MVP:

- balanceo multi-region real.
- autoscaling productivo.
- routing dinamico por CPU o memoria.
- aislamiento fisico por tenant.
- service mesh.

## Evolucion futura

Cuando el sistema crezca, se podra evolucionar a:

- API Gateway.
- balanceador por region.
- pools por legal entity o grupo de sociedades.
- circuit breakers para ERP.
- metricas de latencia, errores y saturacion.
- routing resource-aware dentro del pool.
- dashboards de salud por tenant y legal entity.

## Consecuencias

### Positivas

- Evita mezclar decisiones de negocio con balanceo tecnico.
- Prepara el sistema para despliegues por sociedad, pais o region.
- Refuerza seguridad y residencia del dato.
- Permite escalar sin romper el modelo tenant-aware.
- Deja trazabilidad de decisiones de infraestructura.

### Costes

- Exige modelar contexto de peticion desde el inicio.
- Requiere observabilidad minima.
- Aumenta la disciplina sobre permisos y legal entity.
- Las pruebas futuras deberan cubrir routing correcto y fallos de contexto.

## Reglas derivadas

- Toda peticion relevante debe tener contexto de tenant.
- Toda operacion fiscal o contable debe tener legal entity.
- El pool de infraestructura se selecciona por politica funcional.
- El balanceo tecnico solo opera dentro del pool seleccionado.
- Las decisiones de routing deben ser trazables.
- Las reglas de routing viven fuera del dominio.
