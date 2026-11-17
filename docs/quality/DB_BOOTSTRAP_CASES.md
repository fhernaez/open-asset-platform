# Pruebas obligatorias de DB automanaged en Docker

1. `DB-001` Volumen NUEVO: imagen PostGIS aprobada, secrets montados, `docker compose up -d --build`, job db-bootstrap -> migrate -> API; `SELECT current_database()`, verificar `pg_extension`, tablas; login y API funcionan.
2. `DB-002` Idempotencia: `docker compose down` sin -v, up nuevamente 3 veces; JSON plugin config y activos idénticos, no duplicate schema, no recrear extensión.
3. `DB-003` Volumen ya con cluster pero sin DB OAP: preparar DB postgres en volumen test con otro DB de sentinel; start job crea DB OAP y conserva sentinel.
4. `DB-004` Dos bootstrap job paralelos: lock/disciplina evita race y no genera 500 ni inconsistent db owner.
5. `DB-005` PostGIS ausente: bootstrap falla con error claro; API NO green; no fallback silent.
6. `DB-006` Credenciales: API usa usuario limitado y no administra DB global; no secrets en logs de `docker compose config` ni Git.
7. `DB-007` Migrations: producción no corre makemigrations, migrations versionadas; migrate repeated no produce cambios inesperados.
8. `DB-008` En upgrade: backup, deploy nueva imagen, plugin settings y telemetry mantienen contenido, SHACL/RDF rebuild no altera master.
9. `DB-009` Restore: backup real staging reproduce count assets, 5 puntos historicos, 2 escenas, plugin enable desde GUI.
10. `DB-010` Readiness: API inicia solo tras migrate completed_successfully; 503 transitoria es aceptable, ready con DB a medias NO.

Cada caso con script de CI que usa `COMPOSE_PROJECT_NAME` único; tests destructivos solo en proyecto/volúmenes de test y consentimiento explícito. Documentar imagen/extension/versiones de PostgreSQL y resultados de `SELECT extname,extversion FROM pg_extension`.
