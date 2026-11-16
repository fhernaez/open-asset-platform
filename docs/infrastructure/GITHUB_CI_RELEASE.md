# GitHub CI, PR, releases y calidad de supply chain

## CI en cada PR
1. Validar estructura de specification kit y links internos.
2. Crear `.venv` en runner ANTES de cualquier instalación Python, instalar lock, Django check, Ruff, mypy.
3. DB service PostgreSQL Timescale/PostGIS para integración; correr migrations + pytest unit/integration/contract y coverage.
4. Node frontend npm ci/lock, ESLint, tsc, vitest y Playwright contra stack test.
5. Docker Compose config/build/smoke, test DB first create y idempotencia en CI aislado (nunca run destructive contra volúmenes reales).
6. Security: Bandit/Semgrep si pertinente, pip-audit, npm audit, Trivy imágenes, secret scanner, SBOM/licencias; fail críticos/alto según política.
7. API compatibility OpenAPI diff, event contracts, migrations compatibility, plugin semver; no merging si gate bloqueante.

## Release
Semver core, version de Extension API, manifest plugin, imágenes por digest, changelog, release notes, Known limitations, backup/restore validated, integrity hashes. No etiquetar "paridad completa" sin source audit y suite de pruebas.

## Checks de rendimiento
Telemetría 100k+ eventos fixture determinista (escala ajustable por máquina), recepción vs accept/drop counters consistentes; 1000 assets UI paginada; memory/CPU and p95 lat. Configurar thresholds realistas tras baselines, no números mágicos.

## PR template
REQ IDs, screenshots/E2E, riesgo DB, migración, security, demo, tests logs, breaking changes, dependence license, rollback plan.
