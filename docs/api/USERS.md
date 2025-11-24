# `users` - Endpointy API dla zarządzania użytkownikami.

## `Uczniowie`

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

## `Nauczyciele`

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

## `Rodzice`

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

## `Profile użytkowników`

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
