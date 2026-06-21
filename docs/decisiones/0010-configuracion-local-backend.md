# Decisión 0010 - Configuración local del backend

## Estado

Aceptada.

## Contexto

La Decisión 0009 fija que el primer desarrollo empezará por `CreateInternalOrder`, con dominio, application y tests antes de implementar FastAPI o SQLAlchemy.

Antes de crear el esqueleto backend, debe quedar definida la configuración local mínima para que el proyecto sea reproducible y entendible.

## Decisión

La configuración local del backend usará:

```text
Python 3.12.3
venv
pip-tools
pytest
```

## Justificación

### Python 3.12.3

Python 3.12.3 será la versión base del backend.

Motivos:

- versión moderna y estable.
- compatible con FastAPI, SQLAlchemy, Alembic, pyodbc y pytest.
- suficientemente actual para un proyecto backend nuevo.
- evita mezclar comportamientos entre versiones de Python.

### venv

`venv` será la herramienta base para crear el entorno virtual local.

Motivos:

- viene incluido con Python.
- permite entender claramente qué es un entorno virtual.
- no introduce una capa adicional de gestión de proyecto.
- es suficiente para el MVP.

### pip-tools

`pip-tools` gestionará dependencias directas y dependencias bloqueadas.

Motivos:

- separa lo que el proyecto pide de lo que se instala realmente.
- permite mantener archivos bloqueados reproducibles.
- es profesional sin ocultar demasiado el funcionamiento de `pip`.
- facilita revisar cambios de dependencias en Git.

## Archivos previstos

Cuando se cree el backend, la estructura de dependencias será:

```text
backend/
  pyproject.toml
  requirements.in
  requirements-dev.in
  requirements.txt
  requirements-dev.txt
  .env.example
```

Reglas:

- `requirements.in` contendrá dependencias productivas directas.
- `requirements-dev.in` contendrá dependencias de desarrollo y testing.
- `requirements.txt` será generado desde `requirements.in`.
- `requirements-dev.txt` será generado desde `requirements-dev.in`.
- `.env.example` se subirá al repositorio sin secretos.
- `.env` no se subirá al repositorio.

## Dependencias iniciales

Para el primer microincremento solo se instalará lo necesario.

Dependencia inicial de desarrollo:

```text
pytest
```

FastAPI, SQLAlchemy, Alembic y pyodbc ya están aprobados, pero se añadirán cuando la issue correspondiente los necesite.

## Comandos previstos

Crear entorno virtual:

```powershell
py -3.12 -m venv .venv
```

Activar entorno virtual en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Actualizar herramientas base:

```powershell
python -m pip install --upgrade pip
python -m pip install pip-tools
```

Compilar dependencias:

```powershell
pip-compile requirements.in
pip-compile requirements-dev.in
```

Instalar dependencias de desarrollo:

```powershell
pip-sync requirements.txt requirements-dev.txt
```

Ejecutar tests:

```powershell
pytest
```

## Variables de entorno

El proyecto usará variables de entorno para configuración local.

Reglas:

- `.env` queda fuera de Git.
- `.env.example` documenta nombres esperados sin valores sensibles.
- ninguna credencial real debe aparecer en documentación ni commits.
- la configuración de SQL Server se añadirá cuando exista infrastructure.

## Consecuencias

### Positivas

- El entorno local es simple y reproducible.
- Las dependencias quedan bloqueadas.
- Se evita introducir herramientas demasiado pesadas al inicio.
- El flujo es compatible con aprendizaje backend real.

### Costes

- Hay que ejecutar `pip-compile` cuando cambien dependencias.
- `venv` no gestiona por sí solo metadatos de proyecto como Poetry.
- El equipo debe respetar la diferencia entre archivos `.in` y `.txt`.

## Reglas derivadas

- No subir `.env`.
- No instalar dependencias sin añadirlas al archivo `.in` correspondiente.
- No añadir FastAPI, SQLAlchemy, Alembic o pyodbc hasta que una issue lo requiera.
- No crear configuración de SQL Server antes de crear infrastructure.
- Documentar cualquier nueva dependencia en la issue que la introduce.
