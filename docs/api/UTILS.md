# API Narzędzi (Utils)

**Bazowy URL**: `/api/`

API Utils zapewnia dostęp do zasobów pomocniczych, takich jak przedmioty, tematy lekcji, prace domowe oraz konfiguracja źródeł danych.

## Uwierzytelnianie

Wymaga nagłówka `Authorization: Bearer <token>` LUB `ADMIN-KEY: <key>`.

## Przedmioty

Zarządzanie przedmiotami szkolnymi.

**Endpoint**: `/api/przedmioty/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `nazwa`: Ciąg znaków (Unikalna nazwa)
- `nazwa_skrocona`: Ciąg znaków (Skrót)
- `numer`: Liczba całkowita (Liczba porządkowa)
- `czy_dodatkowy`: Wartość logiczna
- `nauczyciele`: Lista ID Nauczycieli (Relacja wiele-do-wielu)

## Tematy

Zarządzanie tematami lekcji dla poszczególnych przedmiotów.

**Endpoint**: `/api/tematy/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `tresc`: Ciąg znaków (Treść tematu)
- `data`: Data (RRRR-MM-DD)
- `numer_lekcji`: Liczba całkowita
- `czas_realizacji`: Liczba całkowita (Minuty)
- `przedmiot`: Liczba całkowita (Klucz obcy do Przedmiotu)
- `nauczyciel`: Liczba całkowita (Klucz obcy do Nauczyciela, Opcjonalne)

## Prace Domowe

Zarządzanie zadaniami domowymi.

**Endpoint**: `/api/prace-domowe/`

### Filtrowanie

- `?klasa_id=<id>`: Filtruj po Klasie.
- `?przedmiot_id=<id>`: Filtruj po Przedmiocie.
- `?nauczyciel_id=<id>`: Filtruj po Nauczycielu.

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `opis`: Ciąg znaków (Treść zadania HTML/Tekst)
- `termin`: Data (Termin oddania)
- `data_wystawienia`: Data i czas (Tylko do odczytu)
- `klasa`: Liczba całkowita (Klucz obcy do Klasy)
- `przedmiot`: Liczba całkowita (Klucz obcy do Przedmiotu)
- `nauczyciel`: Liczba całkowita (Klucz obcy do Nauczyciela)

## Źródło Danych (Konfiguracja)

Zarządzanie konfiguracją źródła importu danych.

**Endpoint**: `/api/datasource/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `active_source`: Wybór (`local`, `external`)
- `last_import_file`: Ciąg znaków (Ostatni plik importu)
- `last_imported_at`: Data i czas (Tylko do odczytu)
