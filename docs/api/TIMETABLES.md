# API Planów Lekcji (Timetables)

**Bazowy URL**: `/api/`

API Planów Lekcji zarządza strukturą dnia szkolnego, zajęciami oraz kalendarzem wydarzeń.

## Uwierzytelnianie

Wymaga nagłówka `Authorization: Bearer <token>` LUB `ADMIN-KEY: <key>`.

## Plany Zajęć

Zarządzanie tygodniowymi planami lekcji dla klas.

**Endpoint**: `/api/plany-zajec/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `klasa`: Liczba całkowita (Klucz obcy do Klasy)
- `ObowiazujeOdDnia`: Data (np. "2023-09-01")
- `wpisy`: Lista liczb całkowitych (ID obiektów PlanWpis)

## Godziny Lekcyjne

Zarządzanie siatką godzin lekcyjnych.

**Endpoint**: `/api/godziny-lekcyjne/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `Numer`: Liczba całkowita (Numer lekcji, np. 1, 2)
- `CzasOd`: Czas (np. "08:00")
- `CzasDo`: Czas (np. "08:45")
- `CzasTrwania`: Liczba całkowita (Długość w minutach)

## Dni Tygodnia

Metadane dni tygodnia.

**Endpoint**: `/api/dni-tygodnia/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `Nazwa`: Ciąg znaków (np. "Poniedziałek")
- `Numer`: Liczba całkowita (1-7)

## Zajęcia

Definicja konkretnych zajęć (Przedmiot + Nauczyciel).

**Endpoint**: `/api/zajecia/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `przedmiot`: Liczba całkowita (Klucz obcy do Przedmiotu)
- `nauczyciel`: Liczba całkowita (Klucz obcy do Nauczyciela, Opcjonalne)

## Wpisy do Planu (Plan Wpis)

Łączy `Zajęcia` z konkretną `Godziną Lekcyjną` i `Dniem Tygodnia`.

**Endpoint**: `/api/plan-wpisy/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `godzina_lekcyjna`: Liczba całkowita (Klucz obcy)
- `dzien_tygodnia`: Liczba całkowita (Klucz obcy)
- `zajecia`: Liczba całkowita (Klucz obcy)

## Wydarzenia (Kalendarz)

Zarządzanie wydarzeniami szkolnymi (sprawdziany, święta, wycieczki).

**Endpoint**: `/api/wydarzenia/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `tytul`: Ciąg znaków (Tytuł wydarzenia)
- `opis`: Ciąg znaków (Opis)
- `data`: Data i czas (Data wydarzenia)
- `klasa`: Liczba całkowita (Klucz obcy, Opcjonalne)
- `przedmiot`: Liczba całkowita (Klucz obcy, Opcjonalne)
- `nauczyciel`: Liczba całkowita (Klucz obcy, Opcjonalne)
