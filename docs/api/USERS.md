# API Użytkowników (Users)

**Bazowy URL**: `/api/`

API Użytkowników obsługuje zarządzanie kontami Uczniów, Nauczycieli, Rodziców oraz profilami użytkowników.

## Uwierzytelnianie

Wymaga nagłówka `Authorization: Bearer <token>` LUB `ADMIN-KEY: <key>`.

## Uczniowie

Zarządzanie kontami i danymi uczniów.

**Endpoint**: `/api/uczniowie/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `user`: Zagnieżdżony obiekt User (username, email, first_name, last_name, password - hasło tylko przy zapisie)
- `klasa`: Liczba całkowita (Klucz obcy do Klasy)
- `adres`: Liczba całkowita (Klucz obcy do Adresu)
- `telefon`: Ciąg znaków (Opcjonalny)
- `data_urodzenia`: Data (RRRR-MM-DD)

## Nauczyciele

Zarządzanie kontami nauczycieli.

**Endpoint**: `/api/nauczyciele/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `user`: Zagnieżdżony obiekt User
- `telefon`: Ciąg znaków (Opcjonalny)

## Rodzice

Zarządzanie kontami rodziców i powiązywanie ich z uczniami.

**Endpoint**: `/api/rodzice/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `user`: Zagnieżdżony obiekt User
- `telefon`: Ciąg znaków (Opcjonalny)
- `dzieci`: Lista ID uczniów (Uczen)

## Profile Użytkowników

Zarządzanie ustawieniami profilu (motywy, 2FA).

**Endpoint**: `/api/profile/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `user`: Liczba całkowita (Tylko do odczytu, powiązane ID użytkownika)
- `theme_preference`: Wybór ('light', 'dark', 'system')
- `totp_enabled`: Wartość logiczna (Tylko do odczytu)

## Klasy

Zarządzanie klasami szkolnymi (np. 1A, 2B).

**Endpoint**: `/api/klasy/`

### Pola

- `id`: Liczba całkowita (Tylko do odczytu)
- `nazwa`: Ciąg znaków (np. "1A")
- `numer`: Liczba całkowita (Rocznik/Poziom)
- `wychowawca`: Liczba całkowita (Klucz obcy do Nauczyciela, Opcjonalne)

## Adresy

Zarządzanie bazą adresów przypisanych do uczniów.

**Endpoint**: `/api/adresy/`

## Wiadomości

Zarządzanie wiadomościami systemowymi.

**Endpoint**: `/api/wiadomosci/`
