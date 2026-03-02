# API Frekwencji (Attendance)

**Bazowy URL**: `/api/`

API Frekwencji umożliwia zarządzanie rekordami obecności uczniów oraz statusami obecności.

## Uwierzytelnianie

Wymaga nagłówka `Authorization: Bearer <token>` LUB `ADMIN-KEY: <key>`.

## Statusy Obecności

Zarządzanie typami statusów obecności (np. Obecny, Nieobecny, Spóźniony).

**Endpoint**: `/api/statusy/`

| Metoda | URL                  | Opis                                    |
| ------ | -------------------- | --------------------------------------- |
| GET    | `/api/statusy/`      | Pobierz listę wszystkich statusów       |
| POST   | `/api/statusy/`      | Utwórz nowy status                      |
| GET    | `/api/statusy/{id}/` | Pobierz szczegóły statusu               |
| PUT    | `/api/statusy/{id}/` | Zaktualizuj status (pełna aktualizacja) |
| PATCH  | `/api/statusy/{id}/` | Częściowo zaktualizuj status            |
| DELETE | `/api/statusy/{id}/` | Usuń status                             |

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `Wartosc`: Ciąg znaków (Maks. 45 znaków) — Nazwa statusu (np. "Obecny")

## Frekwencja

Zarządzanie indywidualnymi wpisami obecności dla uczniów.

**Endpoint**: `/api/frekwencja/`

| Metoda | URL                     | Opis                           |
| ------ | ----------------------- | ------------------------------ |
| GET    | `/api/frekwencja/`      | Pobierz listę wpisów obecności |
| POST   | `/api/frekwencja/`      | Utwórz nowy wpis obecności     |
| GET    | `/api/frekwencja/{id}/` | Pobierz szczegóły wpisu        |
| PUT    | `/api/frekwencja/{id}/` | Zaktualizuj wpis               |
| PATCH  | `/api/frekwencja/{id}/` | Częściowo zaktualizuj wpis     |
| DELETE | `/api/frekwencja/{id}/` | Usuń wpis                      |

### Filtrowanie

Możesz filtrować listę wpisów używając parametrów w adresie URL:

- `?uczen_id=<id>`: Filtruj po ID ucznia
- `?date=<YYYY-MM-DD>`: Filtruj po dacie

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `Data`: Data (RRRR-MM-DD)
- `uczen`: Liczba całkowita (Klucz obcy do Ucznia)
- `godzina_lekcyjna`: Liczba całkowita (Klucz obcy do GodzinyLekcyjne, Opcjonalne)
- `status`: Liczba całkowita (Klucz obcy do StatusyObecnosci, Opcjonalne)
