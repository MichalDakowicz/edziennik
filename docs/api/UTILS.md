# `utils` - Endpointy API dla pomocniczych modeli (Przedmioty, Tematy)

Wszystkie endpointy wymagają nagłówka `ADMIN-KEY` (tak jak inne moduły API w projekcie).

## `Przedmioty`

- GET (lista przedmiotów)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/przedmioty/" `
   -H "ADMIN-KEY: "
```

- GET (pojedynczy przedmiot)

```ps
   curl.exe -X GET http://dziennik.polandcentral.cloudapp.azure.com/api/przedmioty/1/ `
   -H "ADMIN-KEY: "
```

- POST (utworzenie przedmiotu)

```ps
   curl.exe -X POST http://dziennik.polandcentral.cloudapp.azure.com/api/przedmioty/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{\"nazwa\": \"Matematyka\", \"nazwa_skrocona\": \"Mat\", \"numer\": 1, \"czy_dodatkowy\": false, \"nauczyciele\": [2,3] }'
```

- PUT (aktualizacja przedmiotu)

```ps
   curl.exe -X PUT http://dziennik.polandcentral.cloudapp.azure.com/api/przedmioty/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{\"nazwa\": \"Matematyka - new\", \"nazwa_skrocona\": \"M\", \"nauczyciele\": [2] }'
```

- DELETE (usunięcie przedmiotu)

```ps
   curl.exe -X DELETE http://dziennik.polandcentral.cloudapp.azure.com/api/przedmioty/1/ `
   -H "ADMIN-KEY: "
```

## `Tematy`

- GET (lista tematów)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/tematy/" `
   -H "ADMIN-KEY: "
```

- GET (pojedynczy temat)

```ps
   curl.exe -X GET http://dziennik.polandcentral.cloudapp.azure.com/api/tematy/1/ `
   -H "ADMIN-KEY: "
```

- POST (utworzenie tematu)

```ps
   curl.exe -X POST http://dziennik.polandcentral.cloudapp.azure.com/api/tematy/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{\"tresc\": \"Wprowadzenie do równań\", \"data\": \"2025-11-24\", \"numer_lekcji\": 1, \"przedmiot_id\": 1, \"nauczyciel_id\": 5 }'
```

- PUT (aktualizacja tematu)

```ps
   curl.exe -X PUT http://dziennik.polandcentral.cloudapp.azure.com/api/tematy/1/ `
   -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{\"tresc\": \"Zaktualizowany temat\"}'
```

- DELETE (usunięcie tematu)

```ps
   curl.exe -X DELETE http://dziennik.polandcentral.cloudapp.azure.com/api/tematy/1/ `
   -H "ADMIN-KEY: "
```

## `Prace domowe` (Homework)

-   GET (lista prac domowych)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/prace-domowe/" `
   -H "ADMIN-KEY: "
```

-   GET (filtrowanie po klasie/przedmiocie/nauczycielu)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/prace-domowe/?klasa_id=1&przedmiot_id=2" `
   -H "ADMIN-KEY: "
```

-   GET (pojedyncza praca domowa)

```ps
   curl.exe -X GET http://dziennik.polandcentral.cloudapp.azure.com/api/prace-domowe/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie pracy domowej)

```ps
   curl.exe -X POST http://dziennik.polandcentral.cloudapp.azure.com/api/prace-domowe/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{\"klasa_id\":1, \"przedmiot_id\":2, \"nauczyciel_id\":5, \"opis\": \"Zadanie domowe\", \"termin\": \"2025-12-01\"}'
```

-   PUT (aktualizacja pracy domowej)

```ps
   curl.exe -X PUT http://dziennik.polandcentral.cloudapp.azure.com/api/prace-domowe/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{\"opis\":\"Zmienione zadanie\", \"termin\":\"2025-12-05\"}'
```

-   DELETE (usunięcie pracy domowej)

```ps
   curl.exe -X DELETE http://dziennik.polandcentral.cloudapp.azure.com/api/prace-domowe/1/ `
   -H "ADMIN-KEY: "
```

## `DataSource` (active data source / import info)

-   GET (get current active source and last import info)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/datasource/" `
   -H "ADMIN-KEY: "
```

-   POST (set active source and optional last_import_file)

```ps
   curl.exe -X POST http://dziennik.polandcentral.cloudapp.azure.com/api/datasource/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{\"active_source\": \"local\", \"last_import_file\": \"import.csv\" }'
```
