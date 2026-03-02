# API Ocen (Grades)

**Bazowy URL**: `/api/`

API Ocen umożliwia zarządzanie ocenami uczniów, ocenami okresowymi i końcowymi oraz punktami z zachowania.

## Uwierzytelnianie

Wymaga nagłówka `Authorization: Bearer <token>` LUB `ADMIN-KEY: <key>`.

## Oceny (Zwykłe)

Zarządzanie pojedynczymi ocenami cząstkowymi.

**Endpoint**: `/api/oceny/`

| Metoda | URL                | Opis                    |
| ------ | ------------------ | ----------------------- |
| GET    | `/api/oceny/`      | Pobierz listę ocen      |
| POST   | `/api/oceny/`      | Dodaj nową ocenę        |
| GET    | `/api/oceny/{id}/` | Pobierz szczegóły oceny |
| PUT    | `/api/oceny/{id}/` | Zaktualizuj ocenę       |
| DELETE | `/api/oceny/{id}/` | Usuń ocenę              |

### Filtrowanie

- `?uczen=<id>`: Filtruj po ID ucznia.

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `wartosc`: Liczba dziesiętna (np. 4.50)
- `waga`: Liczba całkowita (Domyślnie 1)
- `opis`: Ciąg znaków (Opcjonalny opis)
- `data_wystawienia`: Data i czas (Tylko do odczytu, generowane automatycznie)
- `uczen`: Liczba całkowita (Klucz obcy do Ucznia)
- `nauczyciel`: Liczba całkowita (Klucz obcy do Nauczyciela, Opcjonalne)
- `przedmiot`: Liczba całkowita (Klucz obcy do Przedmiotu)
- Flagi: `czy_punkty`, `czy_opisowa`, `czy_do_sredniej` (Wartości logiczne)

## Oceny Okresowe

Zarządzanie ocenami semestralnymi.

**Endpoint**: `/api/oceny-okresowe/`

### Filtrowanie

- `?uczen=<id>`: Filtruj po ID ucznia.

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `uczen`: Liczba całkowita (Klucz obcy do Ucznia)
- `wartosc`: Liczba dziesiętna
- `okres`: Liczba całkowita (Numer semestru, np. 1 lub 2)
- `przedmiot`: Liczba całkowita (Klucz obcy do Przedmiotu, Opcjonalne)
- `nauczyciel`: Liczba całkowita (Klucz obcy do Nauczyciela, Opcjonalne)

## Oceny Końcowe

Zarządzanie ocenami rocznymi.

**Endpoint**: `/api/oceny-koncowe/`

### Filtrowanie

- `?uczen=<id>`: Filtruj po ID ucznia.

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `uczen`: Liczba całkowita (Klucz obcy do Ucznia)
- `wartosc`: Liczba dziesiętna
- `przedmiot`: Liczba całkowita (Klucz obcy do Przedmiotu)
- `nauczyciel`: Liczba całkowita (Klucz obcy do Nauczyciela, Opcjonalne)

## Zachowanie (Punkty)

Zarządzanie punktami z zachowania uczniów.

**Endpoint**: `/api/zachowanie-punkty/`

### Filtrowanie

- `?uczen=<id>`: Filtruj po ID ucznia.

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `uczen`: Liczba całkowita (Klucz obcy do Ucznia)
- `punkty`: Liczba całkowita (Punkty dodatnie lub ujemne)
- `opis`: Ciąg znaków (Opis zdarzenia)
- `data_wpisu`: Data i czas (Tylko do odczytu)
- `nauczyciel_wpisujacy`: Liczba całkowita (Klucz obcy do Nauczyciela, Opcjonalne)
