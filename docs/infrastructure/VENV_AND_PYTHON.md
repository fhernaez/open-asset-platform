# Python .venv — instrucciones obligatorias para agentes

## Primer comando local
```bash
python3 -m venv .venv
.venv/bin/python -c 'import sys; assert sys.prefix != sys.base_prefix; print(sys.executable)'
.venv/bin/python -m pip --version
```
**No activar globalmente si hay riesgo de confusión:** usar rutas `.venv/bin/python` y `.venv/bin/pytest` siempre; Windows `\.venv\Scripts\python.exe` (ruta mostrada de forma indicativa, verificar en máquina). No instalar Django ni drivers hasta validar .venv. Si falta paquete Python `venv`, documentar bloqueo; no usar `sudo pip`.

## Gestión dependencias
Usar `pyproject.toml` + un lockfile reproducible con hashes o versiones pinneadas; `.venv/bin/python -m pip install -e '.[dev]'` sólo después de generar proyecto; no instalar dependencias sin actualizarlas. Python versión pinneada y compatible con Django/PostGIS drivers. Separar extras (`iot`, `rdf`, `ai`, `test`) y licencias. En Docker instalar dependencias dentro de imagen por etapa de build (no usar host .venv dentro del contenedor).

## Tests Django
`.venv/bin/python manage.py check --deploy`, `.venv/bin/python manage.py makemigrations --check --dry-run`, `.venv/bin/python manage.py migrate --plan`, `.venv/bin/python -m pytest`, `.venv/bin/python -m ruff check .`, `.venv/bin/python -m mypy ...` una vez que existan. CI debe reproducir `.venv` en runner y usar rutas explícitas.

## GitHub
`.venv/`, `__pycache__/`, caches nunca commit; `.env` real, secrets y volúmenes fuera de Git. Poner comandos reales en README y CI. No usar venv como justificación para saltar Docker integration tests.
