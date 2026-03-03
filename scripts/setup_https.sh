#!/usr/bin/env bash
set -Eeuo pipefail

# Usage:
#   sudo ./scripts/setup_https.sh
# Optional:
#   DOMAIN=dziennik.polandcentral.cloudapp.azure.com APACHE_BACKEND_PORT=8080 sudo ./scripts/setup_https.sh

DOMAIN="${DOMAIN:-dziennik.polandcentral.cloudapp.azure.com}"
APACHE_BACKEND_PORT="${APACHE_BACKEND_PORT:-8080}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root: sudo ./scripts/setup_https.sh"
  exit 1
fi

echo "--- Setting up HTTPS with Caddy (safe mode) ---"

BACKUP_DIR=""
CHANGED=0

rollback() {
  if [[ "${CHANGED}" -eq 1 && -n "${BACKUP_DIR}" && -d "${BACKUP_DIR}" ]]; then
    echo "Error detected. Restoring Apache config from backup: ${BACKUP_DIR}"
    cp -a "${BACKUP_DIR}/ports.conf" /etc/apache2/ports.conf || true
    if [[ -d "${BACKUP_DIR}/sites-enabled" ]]; then
      cp -a "${BACKUP_DIR}/sites-enabled/." /etc/apache2/sites-enabled/ || true
    fi
    systemctl restart apache2 || true
  fi
}
trap rollback ERR

print_failure_diagnostics() {
  echo
  echo "--- Diagnostics ---"
  apache2ctl configtest || true
  systemctl --no-pager --full status apache2 | sed -n '1,40p' || true
  journalctl -xeu apache2 -n 80 --no-pager || true
  echo "-------------------"
}

install_caddy_if_needed() {
  if command -v caddy >/dev/null 2>&1; then
    echo "Caddy is already installed."
    return
  fi

  echo "Installing Caddy..."
  apt-get update
  apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl gnupg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
    | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
    | tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
  apt-get update
  apt-get install -y caddy
}

pick_free_port() {
  local p="${APACHE_BACKEND_PORT}"
  while ss -ltn "( sport = :${p} )" | grep -q ":${p}"; do
    p=$((p + 1))
  done
  echo "${p}"
}

backup_apache_configs() {
  local ts
  ts="$(date +%Y%m%d_%H%M%S)"
  BACKUP_DIR="/var/backups/edziennik_https_${ts}"
  mkdir -p "${BACKUP_DIR}"
  cp -a /etc/apache2/ports.conf "${BACKUP_DIR}/ports.conf"
  mkdir -p "${BACKUP_DIR}/sites-enabled"
  cp -a /etc/apache2/sites-enabled/. "${BACKUP_DIR}/sites-enabled/" || true
  echo "Backup created at: ${BACKUP_DIR}"
}

rewrite_apache_port() {
  local port="$1"

  echo "Rewriting Apache to 127.0.0.1:${port}..."

  # ports.conf: replace active Listen 80 with loopback backend listen.
  sed -E -i \
    -e "s|^[[:space:]]*Listen[[:space:]]+80([[:space:]]*)$|Listen 127.0.0.1:${port}\1|g" \
    /etc/apache2/ports.conf

  # Ensure Apache is not binding to 443 (Caddy owns HTTPS).
  sed -E -i \
    -e "s|^[[:space:]]*Listen[[:space:]]+443([[:space:]]*)$|# Listen 443 disabled by setup_https.sh\1|g" \
    /etc/apache2/ports.conf

  # If still no loopback Listen, add it.
  if ! grep -Eq "^[[:space:]]*Listen[[:space:]]+127\.0\.0\.1:${port}([[:space:]]*)$" /etc/apache2/ports.conf; then
    echo "Listen 127.0.0.1:${port}" >> /etc/apache2/ports.conf
  fi

  # Update all enabled virtual hosts *:80 -> 127.0.0.1:<port>
  # Also rewrite legacy NameVirtualHost *:80.
  shopt -s nullglob
  local f
  for f in /etc/apache2/sites-enabled/*.conf; do
    sed -E -i \
      -e "s|<VirtualHost[[:space:]]+\*:80([[:space:]]*)>|<VirtualHost 127.0.0.1:${port}\1>|g" \
      -e "s|<VirtualHost[[:space:]]+0\.0\.0\.0:80([[:space:]]*)>|<VirtualHost 127.0.0.1:${port}\1>|g" \
      -e "s|<VirtualHost[[:space:]]+\[::\]:80([[:space:]]*)>|<VirtualHost 127.0.0.1:${port}\1>|g" \
      -e "s|^[[:space:]]*NameVirtualHost[[:space:]]+\*:80([[:space:]]*)$|NameVirtualHost 127.0.0.1:${port}\1|g" \
      "$f"
  done
  shopt -u nullglob
}

write_caddyfile() {
  local port="$1"
  echo "Writing Caddyfile..."
  cat >/etc/caddy/Caddyfile <<EOF
${DOMAIN} {
    reverse_proxy 127.0.0.1:${port}
}
EOF
}

validate_caddyfile() {
  caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
}

# 1) Install Caddy if needed
install_caddy_if_needed

# 2) Stop Apache before changing ports (frees :80 for Caddy challenge/http)
echo "Stopping Apache..."
systemctl stop apache2 || true

# 3) Backup + rewrite Apache config
backup_apache_configs
CHANGED=1

FREE_PORT="$(pick_free_port)"
rewrite_apache_port "${FREE_PORT}"

# 4) Validate Apache config before starting
echo "Validating Apache config..."
apache2ctl configtest

# 5) Apply Caddy config
write_caddyfile "${FREE_PORT}"
echo "Validating Caddy config..."
validate_caddyfile

# 6) Start Apache on backend port
echo "Starting Apache on ${FREE_PORT}..."
if ! systemctl restart apache2; then
  print_failure_diagnostics
  exit 1
fi
systemctl --no-pager --full status apache2 | sed -n '1,12p'

# 7) Restart Caddy
echo "Restarting Caddy..."
systemctl daemon-reload || true
systemctl restart caddy
systemctl --no-pager --full status caddy | sed -n '1,12p'

CHANGED=0
trap - ERR

echo "--- HTTPS setup complete ---"
echo "Domain: ${DOMAIN}"
echo "Apache backend: 127.0.0.1:${FREE_PORT}"
echo "Checks:"
echo "  sudo apache2ctl configtest"
echo "  sudo systemctl status apache2 caddy"
echo "  sudo journalctl -xeu apache2 -n 80 --no-pager"
echo "  sudo journalctl -xeu caddy -n 80 --no-pager"