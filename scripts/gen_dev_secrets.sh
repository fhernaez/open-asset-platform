#!/usr/bin/env bash
# Generate local development secrets (never committed). Idempotent.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p secrets
for name in db_admin_password db_app_password django_secret bootstrap_admin_password; do
  file="secrets/${name}.txt"
  if [[ ! -f "$file" ]]; then
    openssl rand -base64 32 > "$file"
    echo "generated $file"
  else
    echo "exists   $file"
  fi
done

if [[ ! -f .env ]]; then
  {
    echo "DB_ADMIN_PASSWORD=$(cat secrets/db_admin_password.txt)"
    echo "DB_APP_PASSWORD=$(cat secrets/db_app_password.txt)"
    echo "DJANGO_SECRET_KEY=$(cat secrets/django_secret.txt)"
    echo "AUTH_BOOTSTRAP_ADMIN_PASSWORD=$(cat secrets/bootstrap_admin_password.txt)"
  } > .env
  echo "generated .env"
else
  echo "exists   .env (not overwritten)"
fi
