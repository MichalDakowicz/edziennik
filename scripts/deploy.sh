#!/bin/bash

# --- CONFIGURATION ---
# The folder where your code is currently sitting
SOURCE_DIR="/home/mdakowicz/edziennik"
# The folder where Apache looks for the site
TARGET_DIR="/var/www/html/edziennik"
# ---------------------

echo "--- Starting Deployment ---"

# 1. PRESERVE DATABASE
# We assume you are using SQLite. If we don't back it up, the next step deletes it.
if [ -f "$TARGET_DIR/db.sqlite3" ]; then
    echo "Backing up production database..."
    cp "$TARGET_DIR/db.sqlite3" "/tmp/db.sqlite3.bak"
fi

# 2. UPDATE CODE
# We create the directory if it doesn't exist
if [ ! -d "$TARGET_DIR" ]; then
    sudo mkdir -p "$TARGET_DIR"
fi

echo "Syncing files..."
# We use rsync instead of 'rm -rf' + 'cp'. 
# It updates files without nuking the folder.
# We exclude .venv so we can build it fresh on the server.
sudo rsync -av --delete \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='db.sqlite3' \
    "$SOURCE_DIR/" "$TARGET_DIR/"

# 3. RESTORE DATABASE
if [ -f "/tmp/db.sqlite3.bak" ]; then
    echo "Restoring production database..."
    sudo mv "/tmp/db.sqlite3.bak" "$TARGET_DIR/db.sqlite3"
elif [ -f "$SOURCE_DIR/db.sqlite3" ]; then
    # If this is the VERY first deploy, use the local DB
    echo "Copying initial database..."
    sudo cp "$SOURCE_DIR/db.sqlite3" "$TARGET_DIR/db.sqlite3"
fi

# 4. VIRTUAL ENVIRONMENT
# Check if venv exists in target, if not create it
if [ ! -d "$TARGET_DIR/.venv" ]; then
    echo "Creating Virtual Environment..."
    sudo python3 -m venv "$TARGET_DIR/.venv"
fi

echo "Installing requirements..."
sudo "$TARGET_DIR/.venv/bin/pip" install -r "$TARGET_DIR/requirements.txt"

# 5. DJANGO COMMANDS
echo "Collecting static files..."
sudo "$TARGET_DIR/.venv/bin/python" "$TARGET_DIR/manage.py" collectstatic --noinput

echo "Making migrations..."
sudo "$TARGET_DIR/.venv/bin/python" "$TARGET_DIR/manage.py" makemigrations

echo "Migrating database..."
sudo "$TARGET_DIR/.venv/bin/python" "$TARGET_DIR/manage.py" migrate

# 6. PERMISSIONS (UBUNTU FIX)
# Ubuntu uses 'www-data', not 'apache'
echo "Setting Permissions..."
sudo chown -R www-data:www-data "$TARGET_DIR"
sudo chmod -R 775 "$TARGET_DIR"

# Special handling for SQLite to prevent "Attempt to write a readonly database"
if [ -f "$TARGET_DIR/db.sqlite3" ]; then
    sudo chown www-data:www-data "$TARGET_DIR/db.sqlite3"
    sudo chmod 664 "$TARGET_DIR/db.sqlite3"
    # The FOLDER containing the db must also be writable
    sudo chmod g+w "$TARGET_DIR"
fi

# 7. RESTART SERVICES (UBUNTU FIX)
# Ubuntu uses 'apache2', not 'httpd'
echo "Restarting Apache..."
sudo systemctl restart apache2

echo "--- Deployment Complete ---"