#!/bin/bash
# ============================================================
# Backup automatizado de MongoDB para Ciudad Robot
# Programar con cron: 0 2 * * * /path/to/mongodb-backup.sh
# ============================================================

set -euo pipefail

BACKUP_DIR="/backups/mongodb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
MONGO_HOST="${MONGO_HOST:-mongodb}"
MONGO_PORT="${MONGO_PORT:-27017}"
MONGO_USER="${MONGO_USER:-ciudad_backup}"
MONGO_PASS="${MONGO_PASS:-backup_secure_password}"
DB_NAME="ciudad_robot"

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Iniciando backup de MongoDB..."

mongodump \
  --host="${MONGO_HOST}" \
  --port="${MONGO_PORT}" \
  --username="${MONGO_USER}" \
  --password="${MONGO_PASS}" \
  --authenticationDatabase=admin \
  --db="${DB_NAME}" \
  --out="${BACKUP_DIR}/dump_${TIMESTAMP}" \
  --gzip

# Comprimir en tar
tar -czf "${BACKUP_DIR}/ciudad_robot_${TIMESTAMP}.tar.gz" \
  -C "${BACKUP_DIR}" "dump_${TIMESTAMP}"
rm -rf "${BACKUP_DIR}/dump_${TIMESTAMP}"

echo "[$(date)] Backup completado: ciudad_robot_${TIMESTAMP}.tar.gz"

# Limpiar backups viejos
find "${BACKUP_DIR}" -name "ciudad_robot_*.tar.gz" -mtime +"${RETENTION_DAYS}" -delete
echo "[$(date)] Backups con más de ${RETENTION_DAYS} días eliminados."
