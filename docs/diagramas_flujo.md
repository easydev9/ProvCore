# Diagramas de flujo

## Objetivo

Representar visualmente los flujos principales del motor de provisiones. Los diagramas usan Mermaid para poder versionarse como texto.

## Arquitectura funcional por modulos

```mermaid
flowchart LR
    PI[Pedido interno] --> MP[Motor comun de provisiones]
    TC[Tarjetas corporativas] --> MP
    FT[Facturas proveedor] --> MP
    IA[OCR / IA] --> FT
    IA --> MAP[Mapeo proveedor operativo-fiscal]
    MAP --> MP
    ERP[ERP y datos maestros] --> MAP
    MP --> REG[Regularizaciones y periodificaciones]
    MP --> AUD[Auditoria]
    REG --> AUD
    MP --> ANA[Analitica y reporting]
    FT --> AUD
    TC --> AUD
    ADM[Administracion] --> MAP
    ADM --> FT
    ADM --> REG
    RESP[Responsable] --> PI
    RESP --> TC
    RESP --> FT
    REG --> ERP
    FT --> ERP
```

## Modelo SaaS tenant-aware

```mermaid
flowchart TD
    T[Tenant] --> LE1[Legal entity A]
    T --> LE2[Legal entity B]
    T --> BG[Buyer groups]
    LE1 --> ERP1[ERP company A]
    LE2 --> ERP2[ERP company B]
    LE1 --> MP1[Provisiones, facturas y proveedores]
    LE2 --> MP2[Provisiones, facturas y proveedores]
    BG --> ALT[Alertas y responsabilidades]
    MP1 --> AUD[Auditoria y eventos]
    MP2 --> AUD
```

## Routing funcional multi-sociedad

```mermaid
flowchart TD
    A[Peticion API] --> B[Autenticacion]
    B --> C[Autorizacion]
    C --> D[Resolver tenant y legal entity]
    D --> E[Aplicar politica de routing]
    E --> F[Seleccionar pool autorizado]
    F --> G[Balanceo tecnico dentro del pool]
    G --> H[Instancia ProvCore]
    H --> I[Caso de uso application]
    H --> J[Adaptador ERP permitido]
    H --> K[Base de datos permitida]
    F --> L[Health checks y metricas]
    L --> G
    E --> M[Log de decision de routing]
```

## Flujo principal de gasto provisionado

```mermaid
flowchart TD
    A[Responsable compromete gasto] --> B[Crea pedido interno]
    B --> C[Se genera ID_PROVISION]
    C --> D{Proveedor fiscal validado?}
    D -- No --> E[Administracion valida mapeo y datos contables]
    D -- Si --> F[Provision pendiente de integracion]
    E --> F
    F --> G[Provision integrada y abierta]
    G --> H[Llega factura]
    H --> I[OCR/IA extrae datos]
    I --> J[Sistema busca provisiones compatibles]
    J --> K[Sugiere consumo]
    K --> L[Responsable valida servicio]
    L --> M[Administracion revisa contabilidad e impuestos]
    M --> N[Aprueba consumo]
    N --> O{Diferencias?}
    O -- Si --> P[Genera regularizacion]
    O -- No --> Q[Factura registrada]
    P --> Q
    Q --> R[Factura contabilizada]
    R --> S[Provision cerrada o parcialmente abierta]
```

## Factura sin provision previa

```mermaid
flowchart TD
    A[Llega factura] --> B[OCR/IA extrae datos]
    B --> C[Sistema busca provisiones abiertas]
    C --> D{Existe provision compatible?}
    D -- Si --> E[Continua flujo de consumo]
    D -- No --> F[Marca factura como pendiente de provision]
    F --> G[Responsable justifica excepcion]
    G --> H[Administracion revisa motivo]
    H --> I[Crea provision tardia]
    I --> J[Consume provision tardia inmediatamente]
    J --> K[Registra auditoria completa]
    K --> L[Factura continua a validacion contable]
```

## Mapeo proveedor operativo a proveedor fiscal

```mermaid
flowchart TD
    A[Usuario informa alias proveedor] --> B[Sistema normaliza alias]
    B --> C[Busca historico y datos maestros]
    C --> D[IA/reglas sugieren candidatos]
    D --> E{Confianza suficiente?}
    E -- No --> F[Revision manual obligatoria]
    E -- Si --> G[Muestra candidato y explicacion]
    F --> H[Administracion decide]
    G --> H
    H --> I{Proveedor correcto?}
    I -- Si --> J[Valida mapeo]
    I -- No --> K[Rechaza o corrige]
    J --> L[Mapeo usable en futuros casos]
    K --> M[Auditoria y aprendizaje historico]
```

## Alta de proveedor fiscal desde factura

```mermaid
flowchart TD
    A[Llega factura] --> B[OCR/IA detecta proveedor fiscal]
    B --> C[Consulta ERP por legal entity]
    C --> D{Proveedor existe?}
    D -- Si --> E[Asocia proveedor fiscal validado]
    D -- No --> F[Bloquea factura]
    F --> G[Crea solicitud de alta proveedor]
    G --> H[Administracion valida datos]
    H --> I[Envia o simula alta ERP]
    I --> J{ERP confirma?}
    J -- Si --> K[Desbloquea factura]
    J -- No --> L[Marca fallo y motivo]
    K --> M[Continua busqueda de provision]
    L --> H
```

## Consumo N a N entre facturas y provisiones

```mermaid
flowchart LR
    P1[Provision A] --> R1[Relacion factura-provision]
    P2[Provision B] --> R2[Relacion factura-provision]
    P3[Provision C] --> R3[Relacion factura-provision]
    R1 --> F[Factura agrupada]
    R2 --> F
    R3 --> F
    F --> C[Consumos aprobados]
    C --> D{Diferencia contra total factura?}
    D -- Si --> E[Regularizacion]
    D -- No --> G[Registro de factura]
```

## Movimiento de tarjeta con factura

```mermaid
flowchart TD
    A[Movimiento tarjeta importado] --> B[Usuario clasifica gasto]
    B --> C[Se genera provision tarjeta]
    C --> D[Provision integrada y abierta]
    D --> E{Factura recibida?}
    E -- Si --> F[Adjunta o asocia factura]
    F --> G[OCR/IA extrae datos]
    G --> H[Consume provision de tarjeta]
    H --> I{Diferencias base, impuestos o divisa?}
    I -- Si --> J[Regularizacion]
    I -- No --> K[Pendiente de liquidacion]
    J --> K
    K --> L[Conciliacion con liquidacion bancaria]
    L --> M[Cierre movimiento]
    E -- No --> N[Recordatorios y seguimiento]
```

## Movimiento de tarjeta sin factura

```mermaid
flowchart TD
    A[Movimiento pendiente de factura] --> B{Se recibe factura?}
    B -- Si --> C[Asociar factura]
    B -- No --> D[Responsable marca sin factura]
    D --> E[Motivo obligatorio]
    E --> F[Administracion revisa deducibilidad]
    F --> G{Regularizacion necesaria?}
    G -- Si --> H[Crear regularizacion]
    G -- No --> I[Cerrar como sin factura]
    H --> I
    I --> J[Reporting de sin factura/no deducible]
```

## Alertas de cierre operativo

```mermaid
flowchart TD
    A[Periodo de cierre proximo] --> B[Busca pendientes]
    B --> C[Provisiones abiertas]
    B --> D[Facturas bloqueadas]
    B --> E[Proveedores pendientes de alta]
    B --> F[Movimientos sin factura]
    B --> G[Regularizaciones pendientes]
    C --> H[Determina buyer group]
    D --> H
    E --> H
    F --> H
    G --> H
    H --> I[Crea alerta]
    I --> J[Usuario reconoce o resuelve]
    J --> K{Resuelta a tiempo?}
    K -- Si --> L[Cierra alerta]
    K -- No --> M[Escala a Administracion]
```

## Ciclo de estados de provision

```mermaid
stateDiagram-v2
    [*] --> Creada
    Creada --> PendienteMapeoProveedor
    Creada --> PendienteValidacion
    Creada --> PendienteIntegracion
    PendienteMapeoProveedor --> PendienteValidacion
    PendienteValidacion --> PendienteIntegracion
    PendienteIntegracion --> Integrada
    Integrada --> Abierta
    Abierta --> ConsumoSugerido
    ConsumoSugerido --> ConsumoPreparado
    ConsumoPreparado --> ConsumidaParcialmente
    ConsumoPreparado --> ConsumidaTotalmente
    ConsumidaParcialmente --> ConsumoSugerido
    ConsumidaParcialmente --> ConsumidaTotalmente
    ConsumidaTotalmente --> PendienteRegularizacion
    PendienteRegularizacion --> Regularizada
    Regularizada --> Cerrada
    ConsumidaTotalmente --> Cerrada
    Creada --> Anulada
    PendienteValidacion --> Anulada
    Abierta --> Anulada
    Cerrada --> [*]
    Anulada --> [*]
```

## Responsabilidades de gobierno

```mermaid
flowchart LR
    R[Responsable] -->|Informa compromiso y valida servicio| PI[Pedido interno / factura]
    IA[IA/OCR] -->|Sugiere proveedor, datos y matching| S[Sugerencias]
    S --> A[Administracion]
    A -->|Valida verdad contable| ERP[ERP y datos maestros]
    A -->|Aprueba consumos y regularizaciones| MP[Motor de provisiones]
    MP -->|Trazabilidad| AU[Auditoria]
```

## Modelo entidad-relacion funcional

```mermaid
erDiagram
    TENANT ||--o{ LEGAL_ENTITY : contiene
    TENANT ||--o{ BUYER_GROUP : agrupa
    LEGAL_ENTITY ||--o{ PEDIDO_INTERNO : opera
    LEGAL_ENTITY ||--o{ PROVISION : registra
    LEGAL_ENTITY ||--o{ FACTURA : recibe
    LEGAL_ENTITY ||--o{ PROVEEDOR_FISCAL : valida
    PEDIDO_INTERNO ||--|| PROVISION : genera
    MOVIMIENTO_TARJETA ||--|| PROVISION : genera
    LIQUIDACION_TARJETA ||--o{ MOVIMIENTO_TARJETA : agrupa
    FACTURA ||--o{ FACTURA_PROVISION : consume
    PROVISION ||--o{ FACTURA_PROVISION : es_consumida_por
    PROVEEDOR_OPERATIVO ||--o{ MAPEO_PROVEEDOR : tiene_alias
    PROVEEDOR_FISCAL ||--o{ MAPEO_PROVEEDOR : valida
    FACTURA ||--o{ SOLICITUD_ALTA_PROVEEDOR : bloquea
    PROVEEDOR_FISCAL ||--o{ SUPPLIER_RESPONSIBILITY : asigna
    BUYER_GROUP ||--o{ SUPPLIER_RESPONSIBILITY : gestiona
    BUYER_GROUP ||--o{ ALERTA : recibe
    PERIODO_CIERRE ||--o{ ALERTA : genera
    PROVEEDOR_OPERATIVO ||--o{ PROVISION : informa
    PROVEEDOR_FISCAL ||--o{ PROVISION : gobierna
    PROVISION ||--o{ REGULARIZACION : genera
    FACTURA ||--o{ REGULARIZACION : origina
    FACTURA ||--o{ PERIODIFICACION : distribuye
    PROVISION ||--o{ PERIODIFICACION : soporta
    PROVISION ||--o{ AUDITORIA_ESTADO : audita
    FACTURA ||--o{ AUDITORIA_ESTADO : audita
    MAPEO_PROVEEDOR ||--o{ AUDITORIA_ESTADO : audita
    PROVISION ||--o{ EVENTO_PROCESO : emite
    FACTURA ||--o{ EVENTO_PROCESO : emite

    TENANT {
        string id_tenant
        string nombre_tenant
        string estado_tenant
    }

    LEGAL_ENTITY {
        string id_legal_entity
        string id_tenant
        string codigo_sociedad_erp
        string pais
    }

    PEDIDO_INTERNO {
        string id_pedido_interno
        string id_tenant
        string id_legal_entity
        string id_provision
        string sociedad
        string responsable
        decimal importe_estimado
        string estado_pedido
    }

    PROVISION {
        string id_provision
        string id_tenant
        string id_legal_entity
        string origen_provision
        decimal importe_provisionado
        decimal importe_consumido
        decimal importe_pendiente
        string estado_provision
    }

    FACTURA {
        string id_factura
        string id_tenant
        string id_legal_entity
        string numero_factura
        string proveedor_fiscal_validado
        decimal total_factura
        string estado_factura
    }

    FACTURA_PROVISION {
        string id_factura_provision
        string id_tenant
        string id_legal_entity
        string id_factura
        string id_provision
        decimal importe_consumido
        string estado_relacion
    }

    PROVEEDOR_OPERATIVO {
        string id_proveedor_operativo
        string id_tenant
        string alias_principal
        string alias_normalizado
    }

    PROVEEDOR_FISCAL {
        string id_proveedor_fiscal
        string id_tenant
        string id_legal_entity
        string codigo_proveedor_erp
        string razon_social
        string nif_vat
    }

    SOLICITUD_ALTA_PROVEEDOR {
        string id_solicitud_alta_proveedor
        string id_factura
        string estado_solicitud
        string codigo_respuesta_erp
    }

    MAPEO_PROVEEDOR {
        string id_mapeo_proveedor
        string id_tenant
        string id_legal_entity
        string alias_informado
        decimal confianza_matching
        string estado_mapeo
    }

    BUYER_GROUP {
        string id_buyer_group
        string id_tenant
        string nombre_buyer_group
    }

    SUPPLIER_RESPONSIBILITY {
        string id_supplier_responsibility
        string id_proveedor_fiscal
        string id_buyer_group
        string estado_asignacion
    }

    ALERTA {
        string id_alerta
        string tipo_alerta
        string estado_alerta
        datetime fecha_objetivo
    }

    MOVIMIENTO_TARJETA {
        string id_movimiento_tarjeta
        string id_tenant
        string id_legal_entity
        string id_provision
        decimal importe_movimiento
        string estado_movimiento
    }

    REGULARIZACION {
        string id_regularizacion
        string tipo_regularizacion
        decimal importe_regularizacion
        string estado_regularizacion
    }

    PERIODIFICACION {
        string id_periodificacion
        string periodo
        decimal importe_periodificado
        string estado_periodificacion
    }

    AUDITORIA_ESTADO {
        string id_auditoria
        string id_tenant
        string id_legal_entity
        string entidad
        string accion
        string usuario
        datetime fecha_hora
    }

    EVENTO_PROCESO {
        string id_evento_proceso
        string tipo_evento
        string entidad
        datetime fecha_hora
    }

    PERIODO_CIERRE {
        string id_periodo_cierre
        string id_legal_entity
        string periodo
        string estado_periodo
    }
```
