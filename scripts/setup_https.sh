#!/bin/bash
set -e

# Usage: sudo ./scripts/setup_https.sh

echo "--- Setting up HTTPS with Caddy ---"

# 1. Install Caddy (Ubuntu/Debian)
if ! command -v caddy &> /dev/null; then
    echo "Installing Caddy..."
    sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
    sudo apt update
    sudo apt install -y caddy
else
    echo "Caddy is already installed."
fi

# 2. Stop Apache to free port 80 temporarily
echo "Stopping Apache..."
sudo systemctl stop apache2

# 3. Configure Caddy
echo "Configuring Caddy..."
# Create Caddyfile
cat <<EOF | sudo tee /etc/caddy/Caddyfile
dziennik.polandcentral.cloudapp.azure.com {
    reverse_proxy localhost:8080
}
EOF

# 4. Reconfigure Apache to Listen on 8080
echo "Reconfiguring Apache..."

# Backup existing files if backup doesn't exist
if [ ! -f /etc/apache2/ports.conf.bak ]; then
    sudo cp /etc/apache2/ports.conf /etc/apache2/ports.conf.bak
fi
if [ ! -f /etc/apache2/sites-enabled/edziennik.conf.bak ]; then
    sudo cp /etc/apache2/sites-enabled/edziennik.conf /etc/apache2/sites-enabled/edziennik.conf.bak
fi

# Change Listen 80 to Listen 8080 in ports.conf
sudo sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf
# Ensure the VirtualHost is also updated
sudo sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8080>/g' /etc/apache2/sites-enabled/edziennik.conf

# 5. Start Apache
echo "Starting Apache on port 8080..."
sudo systemctl start apache2

# 6. Restart Caddy to apply config
echo "Restarting Caddy..."
sudo systemctl restart caddy

echo "--- HTTPS Setup Complete ---"
echo "Check status:"
echo "  Apache: sudo systemctl status apache2"
echo "  Caddy:  sudo systemctl status caddy"
echo "Visit: https://dziennik.polandcentral.cloudapp.azure.com"
