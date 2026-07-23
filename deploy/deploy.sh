#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

SERVER_HOST="${SERVER_HOST:-}"
SERVER_USER="${SERVER_USER:-ubuntu}"
SERVER_PORT="${SERVER_PORT:-22}"
DEPLOY_DIR="${DEPLOY_DIR:-/opt/hagsyn/Hagsyn-Graph}"
SITE_ADDRESS="${SITE_ADDRESS:-http://$SERVER_HOST}"
SERVICE_NAME="${SERVICE_NAME:-hagsyn}"
APP_USER="${APP_USER:-$SERVER_USER}"
APP_GROUP="${APP_GROUP:-$SERVER_USER}"
DATA_DIR="${DATA_DIR:-/opt/hagsyn/data}"
DEPLOY_SSH_PASSWORD="${DEPLOY_SSH_PASSWORD:-}"
ENV_SOURCE_FILE="${ENV_SOURCE_FILE:-$ROOT_DIR/backend/.env.server}"

if [[ -z "$SERVER_HOST" ]]; then
  echo "SERVER_HOST is required" >&2
  exit 1
fi

run_expect() {
  local cmd="$1"
  if [[ -n "$DEPLOY_SSH_PASSWORD" ]]; then
    expect <<EOF
set timeout -1
spawn bash -lc {$cmd}
expect {
  "*password:" { send "$DEPLOY_SSH_PASSWORD\r"; exp_continue }
  eof
}
EOF
  else
    bash -lc "$cmd"
  fi
}

render_template() {
  local src="$1"
  local dest="$2"
  sed \
    -e "s|__DEPLOY_DIR__|$DEPLOY_DIR|g" \
    -e "s|__SITE_ADDRESS__|$SITE_ADDRESS|g" \
    -e "s|__APP_USER__|$APP_USER|g" \
    -e "s|__APP_GROUP__|$APP_GROUP|g" \
    "$src" > "$dest"
}

render_template "$ROOT_DIR/deploy/templates/hagsyn.service.template" "$TMP_DIR/${SERVICE_NAME}.service"
render_template "$ROOT_DIR/deploy/templates/Caddyfile.template" "$TMP_DIR/Caddyfile"

if [[ -f "$ENV_SOURCE_FILE" ]]; then
  cp "$ENV_SOURCE_FILE" "$TMP_DIR/backend.env"
else
  cp "$ROOT_DIR/backend/.env.server.example" "$TMP_DIR/backend.env"
fi

SSH_BASE="ssh -o StrictHostKeyChecking=no -p ${SERVER_PORT} ${SERVER_USER}@${SERVER_HOST}"
RSYNC_BASE="rsync -az --delete --exclude '.git/' --exclude 'backend/.venv/' --exclude 'backend/__pycache__/' --exclude 'backend/.pytest_cache/' --exclude 'backend/storage/' --exclude 'backend/hagsyn_graph.db' --exclude 'backend/.env.server' --exclude 'frontend/.DS_Store' --exclude '__pycache__/' --exclude '.codegraph/'"

run_expect "$SSH_BASE 'sudo mkdir -p \"$DEPLOY_DIR\" \"$DATA_DIR/uploads\" \"$DATA_DIR/compressed\" \"$DATA_DIR/subtitles\" && sudo chown -R \"$APP_USER\":\"$APP_GROUP\" \"$DEPLOY_DIR\" \"$DATA_DIR\"'"
run_expect "$RSYNC_BASE '$ROOT_DIR/' '${SERVER_USER}@${SERVER_HOST}:$DEPLOY_DIR/'"
run_expect "scp -P ${SERVER_PORT} -o StrictHostKeyChecking=no '$TMP_DIR/backend.env' '${SERVER_USER}@${SERVER_HOST}:$DEPLOY_DIR/backend/.env'"
run_expect "scp -P ${SERVER_PORT} -o StrictHostKeyChecking=no '$TMP_DIR/${SERVICE_NAME}.service' '${SERVER_USER}@${SERVER_HOST}:/tmp/${SERVICE_NAME}.service'"
run_expect "scp -P ${SERVER_PORT} -o StrictHostKeyChecking=no '$TMP_DIR/Caddyfile' '${SERVER_USER}@${SERVER_HOST}:/tmp/Caddyfile.${SERVICE_NAME}'"

run_expect "$SSH_BASE '
set -e
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip ffmpeg caddy
cd \"$DEPLOY_DIR/backend\"
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sudo mv /tmp/${SERVICE_NAME}.service /etc/systemd/system/${SERVICE_NAME}.service
sudo mv /tmp/Caddyfile.${SERVICE_NAME} /etc/caddy/Caddyfile
sudo systemctl daemon-reload
sudo systemctl enable --now ${SERVICE_NAME}.service
sudo systemctl restart ${SERVICE_NAME}.service
sudo systemctl restart caddy
for attempt in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS http://127.0.0.1:8000/api/health; then
    exit 0
  fi
  sleep 2
done
echo \"backend health check failed after retries\" >&2
exit 1
'"

echo "Deploy complete:"
if [[ "$SITE_ADDRESS" == http://* || "$SITE_ADDRESS" == https://* ]]; then
  PUBLIC_URL="${SITE_ADDRESS%/}"
else
  PUBLIC_URL="https://${SITE_ADDRESS%/}"
fi
echo "  Frontend: ${PUBLIC_URL}/"
echo "  Health:   ${PUBLIC_URL}/api/health"
