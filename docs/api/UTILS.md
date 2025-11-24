# `utils` - Endpointy API dla pomocniczych modeli (Przedmioty, Tematy)

Wszystkie endpointy wymagają nagłówka `ADMIN-KEY` (tak jak inne moduły API w projekcie).

## `Przedmioty`

- GET (lista przedmiotów)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/przedmioty/" `
   -H "ADMIN-KEY: "
```

- GET (pojedynczy przedmiot)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/przedmioty/1/ `
   -H "ADMIN-KEY: "
```

- POST (utworzenie przedmiotu)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/przedmioty/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"nazwa": "Matematyka", "nazwa_skrocona": "Mat", "numer": 1, "czy_dodatkowy": false, "nauczyciele": [2,3] }'
```

- PUT (aktualizacja przedmiotu)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/przedmioty/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"nazwa": "Matematyka - new", "nazwa_skrocona": "M", "nauczyciele": [2] }'
```

- DELETE (usunięcie przedmiotu)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/przedmioty/1/ `
   -H "ADMIN-KEY: "
```

## `Tematy`

- GET (lista tematów)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/tematy/" `
   -H "ADMIN-KEY: "
```

- GET (pojedynczy temat)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/tematy/1/ `
   -H "ADMIN-KEY: "
```

- POST (utworzenie tematu)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/tematy/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"tresc": "Wprowadzenie do równań", "data": "2025-11-24", "numer_lekcji": 1, "przedmiot_id": 1, "nauczyciel_id": 5 }'
```

- PUT (aktualizacja tematu)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/tematy/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"tresc": "Zaktualizowany temat"}'
```

- DELETE (usunięcie tematu)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/tematy/1/ `
   -H "ADMIN-KEY: "
```

## `Prace domowe` (Homework)

-   GET (lista prac domowych)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/prace-domowe/" `
   -H "ADMIN-KEY: "
```

-   GET (filtrowanie po klasie/przedmiocie/nauczycielu)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/prace-domowe/?klasa_id=1&przedmiot_id=2" `
   -H "ADMIN-KEY: "
```

-   GET (pojedyncza praca domowa)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/prace-domowe/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie pracy domowej)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/prace-domowe/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"klasa_id":1, "przedmiot_id":2, "nauczyciel_id":5, "opis": "Zadanie domowe", "termin": "2025-12-01"}'
```

-   PUT (aktualizacja pracy domowej)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/prace-domowe/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"opis":"Zmienione zadanie", "termin":"2025-12-05"}'
```

-   DELETE (usunięcie pracy domowej)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/prace-domowe/1/ `
   -H "ADMIN-KEY: "
```
