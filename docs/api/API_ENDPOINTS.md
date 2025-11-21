# Odniesienia API dla dziennika

## `users` - Endpointy API dla zarządzania użytkownikami.

### `Uczniowie`

-   GET (lista uczniów)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/uczniowie/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy uczeń)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/uczniowie/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie ucznia)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/uczniowie/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"username": "jan_kowalski", "password": "securepass123", "email": "jan.kowalski@example.com", "first_name": "Jan", "last_name": "Kowalski", "telefon": "123456789", "data_urodzenia": "2010-01-01"}'
```

-   DELETE (usunięcie ucznia)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/uczniowie/1/ `
   -H "ADMIN-KEY: "
```

-   PUT (aktualizacja ucznia)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/uczniowie/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"email": "jan.nowak@example.com", "first_name": "Jan", "last_name": "Nowak", "telefon": "987654321", "data_urodzenia": "2010-01-01"}'
```

### `Nauczyciele`

-   GET (lista nauczycieli)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/nauczyciele/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy nauczyciel)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/nauczyciele/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie nauczyciela)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/nauczyciele/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"username": "anna_nowak", "password": "securepass123", "email": "anna.nowak@example.com", "first_name": "Anna", "last_name": "Nowak", "telefon": "123456789"}'
```

-   PUT (aktualizacja nauczyciela)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/nauczyciele/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"email": "anna.kowalska@example.com", "first_name": "Anna", "last_name": "Kowalska", "telefon": "987654321"}'
```

-   DELETE (usunięcie nauczyciela)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/nauczyciele/1/ `
   -H "ADMIN-KEY: "
```

### `Rodzice`

-   GET (lista rodziców)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/rodzice/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy rodzic)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/rodzice/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie rodzica)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/rodzice/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"username": "piotr_kowalski", "password": "securepass123", "email": "piotr.kowalski@example.com", "first_name": "Piotr", "last_name": "Kowalski", "telefon": "123456789"}'
```

-   PUT (aktualizacja rodzica)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/rodzice/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"email": "piotr.nowak@example.com", "first_name": "Piotr", "last_name": "Nowak", "telefon": "987654321"}'
```

-   DELETE (usunięcie rodzica)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/rodzice/1/ `
   -H "ADMIN-KEY: "
```

### `Profile użytkowników`

-   GET (lista profili)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/userprofiles/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy profil)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/userprofiles/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie profilu)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/userprofiles/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"user_id": 1, "theme_preference": "dark"}'
```

-   PUT (aktualizacja profilu)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/userprofiles/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"theme_preference": "light"}'
```

-   DELETE (usunięcie profilu)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/userprofiles/1/ `
   -H "ADMIN-KEY: "
```

## `grades` - Endpointy API dla zarządzania ocenami.

### `Oceny`
-   GET (lista ocen)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedyncza ocena)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/oceny/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie oceny)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/oceny/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": 5, "data": "2025-11-20", "uczen_id": 1, "przedmiot": "Matematyka"}'
```

-   PUT (aktualizacja oceny)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/oceny/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": 4, "data": "2025-11-21", "uczen_id": 1, "przedmiot": "Matematyka"}'
```

-   DELETE (usunięcie oceny)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/oceny/1/ `
   -H "ADMIN-KEY: "
```

### `Oceny okresowe`
-   GET (lista ocen okresowych)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny-okresowe/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedyncza ocena okresowa)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/oceny-okresowe/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie oceny okresowej)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/oceny-okresowe/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": 4, "okres": "I", "uczen_id": 1, "przedmiot": "Fizyka"}'
```

-   PUT (aktualizacja oceny okresowej)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/oceny-okresowe/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": 5, "okres": "II", "uczen_id": 1, "przedmiot": "Fizyka"}'
```

-   DELETE (usunięcie oceny okresowej)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/oceny-okresowe/1/ `
   -H "ADMIN-KEY: "
```

### `Oceny końcowe`
-   GET (lista ocen końcowych)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny-koncowe/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedyncza ocena końcowa)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/oceny-koncowe/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie oceny końcowej)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/oceny-koncowe/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": 5, "rok_szkolny": "2024/2025", "uczen_id": 1, "przedmiot": "Historia"}'
```

-   PUT (aktualizacja oceny końcowej)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/oceny-koncowe/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": 4, "rok_szkolny": "2024/2025", "uczen_id": 1, "przedmiot": "Historia"}'
```

-   DELETE (usunięcie oceny końcowej)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/oceny-koncowe/1/ `
   -H "ADMIN-KEY: "
```
