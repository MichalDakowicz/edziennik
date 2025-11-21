# Postgresql (Docker Compose)

Krótko: obraz `postgres:15-alpine`, kontener `edziennik_postgres`, port `5432`, wolumen `postgres_data`, plik env `../../.env`.

Zmiennie (domyślnie):

-   DB_NAME = `edziennik`
-   DB_USER = `edziennik_user`
-   DB_PASSWORD = `changeme`

Przykład `.env` (katalog główny repo):

```ini
DB_NAME=edziennik
DB_USER=edziennik_user
DB_PASSWORD=twoje_haslo
```

Szybkie polecenia (PowerShell, z katalogu repo):

```powershell
docker compose -f .\docker\postgresql\docker-compose.yml up -d    # uruchom
docker compose -f .\docker\postgresql\docker-compose.yml logs -f  # logi
docker compose -f .\docker\postgresql\docker-compose.yml down   # zatrzymaj
```

Połączenie:

-   Z hosta (psql):

```powershell
psql "postgresql://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>"
```

-   W kontenerze:

```powershell
docker exec -it edziennik_postgres sh
psql -U edziennik_user -d edziennik
```

Healthcheck: używa `pg_isready` (interval 10s, timeout 5s, retries 5).

Trwałość: dane przechowywane w wolumenie `postgres_data` przetrwają restart kontenera.

Krótkie wskazówki:

-   Sprawdź logi (`docker compose ... logs -f`) i status (`docker ps --filter "name=edziennik_postgres"`).
-   Po zmianie DB_USER/DB_NAME po inicjalizacji wolumenu możesz potrzebować ręcznie utworzyć użytkownika/bazę lub usunąć wolumen (utrata danych).
