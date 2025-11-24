# `timetables` - Endpointy API dla zarządzania planami zajęć.

Poniżej znajdują się opisane endpointy dostępne dla modułu planów zajęć. Wzorzec requestów i nagłówków zgodny z innymi dokumentacjami API (zob. `USERS.md`, `GRADES.md`). Wszystkie żądania wymagają nagłówka `ADMIN-KEY`.

## `Godziny Lekcyjne`

-   GET (lista godzin lekcyjnych)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/godziny-lekcyjne/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedyncza godzina lekcyjna)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/godziny-lekcyjne/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie godziny lekcyjnej)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/godziny-lekcyjne/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"Numer": 1, "CzasOd": "08:00", "CzasDo": "08:45", "CzasTrwania": "00:45:00"}'
```

-   PUT (aktualizacja godziny lekcyjnej)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/godziny-lekcyjne/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"Numer": 2, "CzasOd": "08:15", "CzasDo": "09:00", "CzasTrwania": "00:45:00"}'
```

-   DELETE (usunięcie godziny lekcyjnej)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/godziny-lekcyjne/1/ `
   -H "ADMIN-KEY: "
```

## `Dni Tygodnia`

-   GET (lista dni tygodnia)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/dni-tygodnia/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy dzień)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/dni-tygodnia/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie dnia tygodnia)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/dni-tygodnia/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"Nazwa": "Poniedziałek", "Numer": 1}'
```

-   PUT (aktualizacja dnia tygodnia)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/dni-tygodnia/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"Nazwa": "Poniedziałek", "Numer": 1}'
```

-   DELETE (usunięcie dnia tygodnia)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/dni-tygodnia/1/ `
   -H "ADMIN-KEY: "
```

## `Zajęcia`

-   GET (lista zajęć)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/zajecia/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedyncze zajęcia)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/zajecia/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie zajęć)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/zajecia/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"nauczyciel_id": 5}'
```

-   PUT (aktualizacja zajęć)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/zajecia/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"nauczyciel_id": 6}'
```

-   DELETE (usunięcie zajęć)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/zajecia/1/ `
   -H "ADMIN-KEY: "
```

## `Plan Wpisy` (pozycje w planie)

-   GET (lista wpisów)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/plan-wpisy/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy wpis)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/plan-wpisy/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie wpisu w planie)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/plan-wpisy/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"godzina_lekcyjna_id": 1, "dzien_tygodnia_id": 1, "zajecia_id": 3}'
```

-   PUT (aktualizacja wpisu)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/plan-wpisy/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"godzina_lekcyjna_id": 2, "dzien_tygodnia_id": 1, "zajecia_id": 4}'
```

-   DELETE (usunięcie wpisu)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/plan-wpisy/1/ `
   -H "ADMIN-KEY: "
```

## `Plany Zajęć`

-   GET (lista planów zajęć)

```ps
   curl.exe -X GET "http://127.0.0.1:8000/api/plany-zajec/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy plan)

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/plany-zajec/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie planu)

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/plany-zajec/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"ObowiazujeOdDnia": "2025-09-01", "wpisy": [1,2,3]}'
```

-   PUT (aktualizacja planu)

```ps
   curl.exe -X PUT http://127.0.0.1:8000/api/plany-zajec/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"ObowiazujeOdDnia": "2025-09-15", "wpisy": [2,4]}'
```

-   DELETE (usunięcie planu)

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/plany-zajec/1/ `
   -H "ADMIN-KEY: "
```
