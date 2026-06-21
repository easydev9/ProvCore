# Setup backend

## Objetivo

Definir los pasos mínimos para preparar el entorno local del backend de ProvCore.

Este documento aplica cuando se cree la carpeta `backend/`.

## Versión de Python

Versión aprobada:

```text
Python 3.12.3
```

Comprobar versión instalada:

```powershell
py -3.12 --version
```

## Entorno virtual

Crear entorno virtual:

```powershell
py -3.12 -m venv .venv
```

Activar entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Dependencias

Actualizar `pip` e instalar `pip-tools`:

```powershell
python -m pip install --upgrade pip
python -m pip install pip-tools
```

Compilar dependencias:

```powershell
pip-compile requirements.in
pip-compile requirements-dev.in
```

Instalar entorno:

```powershell
pip-sync requirements.txt requirements-dev.txt
```

## Tests

Ejecutar tests:

```powershell
pytest
```

## Variables de entorno

Reglas:

- usar `.env` para valores locales.
- no subir `.env` al repositorio.
- mantener `.env.example` sin secretos.
- añadir variables nuevas solo cuando una issue las necesite.

`.gitignore` ya excluye `.env`, `.env.*`, `.venv/` y `venv/`.
