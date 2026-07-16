#!/bin/sh

set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
RUNTIME_DIR="$ROOT_DIR/.runtime"
LOG_DIR="$RUNTIME_DIR/logs"
PID_DIR="$RUNTIME_DIR/pids"

BACKEND_PORT=8000
FRONTEND_PORT=5173
BACKEND_PID_FILE="$PID_DIR/backend.pid"
FRONTEND_PID_FILE="$PID_DIR/frontend.pid"
BACKEND_LOG="$LOG_DIR/backend.log"
FRONTEND_LOG="$LOG_DIR/frontend.log"

mkdir -p "$LOG_DIR" "$PID_DIR"

usage() {
  cat <<'EOF'
Usage:
  sh hagsyn-server.sh start
  sh hagsyn-server.sh stop
  sh hagsyn-server.sh restart
  sh hagsyn-server.sh status

  sh hagsyn-server.sh -front start
  sh hagsyn-server.sh -front stop
  sh hagsyn-server.sh -front restart
  sh hagsyn-server.sh -front status

  sh hagsyn-server.sh -backup start
  sh hagsyn-server.sh -backup stop
  sh hagsyn-server.sh -backup restart
  sh hagsyn-server.sh -backup status

Optional selectors:
  -front   only frontend
  -backup  only backend
  -all     frontend + backend
  -mix     frontend + backend

Without selector, default target is frontend + backend.
EOF
}

selector="all"
if [ "${1:-}" = "-front" ] || [ "${1:-}" = "-backup" ] || [ "${1:-}" = "-all" ] || [ "${1:-}" = "-mix" ]; then
  case "$1" in
    -front) selector="front" ;;
    -backup) selector="backend" ;;
    -all|-mix) selector="all" ;;
  esac
  shift
fi

action="${1:-status}"

case "$action" in
  start|stop|restart|status) ;;
  -h|--help|help) usage; exit 0 ;;
  *) echo "Unknown action: $action" >&2; usage; exit 1 ;;
esac

port_pid() {
  lsof -tiTCP:"$1" -sTCP:LISTEN 2>/dev/null | head -n 1
}

wait_for_port() {
  port="$1"
  retries="${2:-10}"
  while [ "$retries" -gt 0 ]; do
    pid="$(port_pid "$port")"
    if [ -n "$pid" ]; then
      echo "$pid"
      return 0
    fi
    retries=$((retries - 1))
    sleep 1
  done
  return 1
}

is_pid_running() {
  pid="$1"
  [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null
}

read_pid_file() {
  file="$1"
  if [ -f "$file" ]; then
    tr -d '[:space:]' < "$file"
  fi
}

clear_pid_file_if_stale() {
  file="$1"
  pid="$(read_pid_file "$file")"
  if [ -n "$pid" ] && ! is_pid_running "$pid"; then
    rm -f "$file"
  fi
}

start_backend() {
  clear_pid_file_if_stale "$BACKEND_PID_FILE"
  pid="$(read_pid_file "$BACKEND_PID_FILE")"
  if [ -n "$pid" ] && is_pid_running "$pid"; then
    echo "backend already running (pid $pid) at http://127.0.0.1:$BACKEND_PORT"
    return 0
  fi

  listen_pid="$(port_pid "$BACKEND_PORT")"
  if [ -n "$listen_pid" ]; then
    echo "backend port $BACKEND_PORT already in use by pid $listen_pid" >&2
    return 1
  fi

  if [ ! -x "$BACKEND_DIR/.venv/bin/uvicorn" ]; then
    echo "backend/.venv/bin/uvicorn not found. Please prepare backend/.venv first." >&2
    return 1
  fi

  (
    cd "$BACKEND_DIR"
    nohup "$BACKEND_DIR/.venv/bin/uvicorn" app.main:app --reload --host 127.0.0.1 --port "$BACKEND_PORT" </dev/null >>"$BACKEND_LOG" 2>&1 &
  )

  if pid="$(wait_for_port "$BACKEND_PORT" 12)"; then
    echo "$pid" > "$BACKEND_PID_FILE"
    echo "backend started (pid $pid) at http://127.0.0.1:$BACKEND_PORT"
  else
    echo "backend failed to start, check $BACKEND_LOG" >&2
    return 1
  fi
}

start_frontend() {
  clear_pid_file_if_stale "$FRONTEND_PID_FILE"
  pid="$(read_pid_file "$FRONTEND_PID_FILE")"
  if [ -n "$pid" ] && is_pid_running "$pid"; then
    echo "frontend already running (pid $pid) at http://127.0.0.1:$FRONTEND_PORT/?v=video-compressor-v1"
    return 0
  fi

  listen_pid="$(port_pid "$FRONTEND_PORT")"
  if [ -n "$listen_pid" ]; then
    echo "frontend port $FRONTEND_PORT already in use by pid $listen_pid" >&2
    return 1
  fi

  (
    cd "$FRONTEND_DIR"
    nohup python3 -m http.server "$FRONTEND_PORT" </dev/null >>"$FRONTEND_LOG" 2>&1 &
  )

  if pid="$(wait_for_port "$FRONTEND_PORT" 8)"; then
    echo "$pid" > "$FRONTEND_PID_FILE"
    echo "frontend started (pid $pid) at http://127.0.0.1:$FRONTEND_PORT/?v=video-compressor-v1"
  else
    echo "frontend failed to start, check $FRONTEND_LOG" >&2
    return 1
  fi
}

stop_service() {
  name="$1"
  pid_file="$2"
  port="$3"
  stopped="0"

  clear_pid_file_if_stale "$pid_file"
  pid="$(read_pid_file "$pid_file")"
  if [ -n "$pid" ] && is_pid_running "$pid"; then
    kill "$pid" 2>/dev/null || true
    sleep 1
    if is_pid_running "$pid"; then
      kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$pid_file"
    stopped="1"
  fi

  remaining_pids="$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)"
  if [ -n "$remaining_pids" ]; then
    echo "$remaining_pids" | xargs kill 2>/dev/null || true
    sleep 1
    remaining_pids="$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)"
    if [ -n "$remaining_pids" ]; then
      echo "$remaining_pids" | xargs kill -9 2>/dev/null || true
    fi
    rm -f "$pid_file"
    stopped="1"
  fi

  if [ "$stopped" = "1" ]; then
    echo "$name stopped"
    return 0
  fi

  echo "$name not running"
}

status_service() {
  name="$1"
  pid_file="$2"
  port="$3"
  url="$4"

  clear_pid_file_if_stale "$pid_file"
  pid="$(read_pid_file "$pid_file")"
  listen_pid="$(port_pid "$port")"

  if [ -n "$pid" ] && is_pid_running "$pid"; then
    echo "$name running (pid $pid) at $url"
    return 0
  fi

  if [ -n "$listen_pid" ]; then
    echo "$name running on port $port by pid $listen_pid (not managed by pid file) at $url"
    return 0
  fi

  echo "$name not running"
}

do_start() {
  case "$selector" in
    front) start_frontend ;;
    backend) start_backend ;;
    all)
      start_backend
      start_frontend
      ;;
  esac
}

do_stop() {
  case "$selector" in
    front) stop_service "frontend" "$FRONTEND_PID_FILE" "$FRONTEND_PORT" ;;
    backend) stop_service "backend" "$BACKEND_PID_FILE" "$BACKEND_PORT" ;;
    all)
      stop_service "frontend" "$FRONTEND_PID_FILE" "$FRONTEND_PORT"
      stop_service "backend" "$BACKEND_PID_FILE" "$BACKEND_PORT"
      ;;
  esac
}

do_status() {
  case "$selector" in
    front) status_service "frontend" "$FRONTEND_PID_FILE" "$FRONTEND_PORT" "http://127.0.0.1:$FRONTEND_PORT/?v=video-compressor-v1" ;;
    backend) status_service "backend" "$BACKEND_PID_FILE" "$BACKEND_PORT" "http://127.0.0.1:$BACKEND_PORT/api/health" ;;
    all)
      status_service "backend" "$BACKEND_PID_FILE" "$BACKEND_PORT" "http://127.0.0.1:$BACKEND_PORT/api/health"
      status_service "frontend" "$FRONTEND_PID_FILE" "$FRONTEND_PORT" "http://127.0.0.1:$FRONTEND_PORT/?v=video-compressor-v1"
      ;;
  esac
}

case "$action" in
  start) do_start ;;
  stop) do_stop ;;
  restart)
    do_stop
    do_start
    ;;
  status) do_status ;;
esac
