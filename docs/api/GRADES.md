# `grades` - Endpointy API dla zarządzania ocenami i ocenami z zachowania.

## `Oceny`

-   GET (lista ocen)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/oceny/" `
   -H "ADMIN-KEY: "
```

-   GET (lista ocen dla konkretnego użytkownika)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny/?user_id=1" `
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

## `Oceny okresowe`

-   GET (lista ocen okresowych)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny-okresowe/" `
   -H "ADMIN-KEY: "
```

-   GET (lista ocen okresowych dla konkretnego użytkownika)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny-okresowe/?user_id=1" `
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

## `Oceny końcowe`

-   GET (lista ocen końcowych)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny-koncowe/" `
   -H "ADMIN-KEY: "
```

-   GET (lista ocen końcowych dla konkretnego użytkownika)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/oceny-koncowe/?user_id=1" `
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

## `Punkty z zachowania` — dodatkowa dokumentacja

-   GET (lista punktów z zachowania)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/zachowanie-punkty/" `
   -H "ADMIN-KEY: "
```

-   GET (lista punktów z zachowania dla ucznia, filtr user_id)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/zachowanie-punkty/?user_id=1" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy wpis)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/zachowanie-punkty/1/ `
   -H "ADMIN-KEY: "
```

-   POST (dodaj punkty)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/zachowanie-punkty/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"uczen_id": 1, "punkty": 2, "opis": "Dodatkowe za pomoc", "nauczyciel_wpisujacy_id": 5}'
```

-   PUT (aktualizacja wpisu)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/zachowanie-punkty/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"punkty": -1, "opis": "Korekta"}'
```

-   DELETE (usuń wpis)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/zachowanie-punkty/1/ `
   -H "ADMIN-KEY: "
```
