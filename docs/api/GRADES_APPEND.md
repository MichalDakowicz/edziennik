# `Punkty z zachowania` — dodatkowa dokumentacja

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
