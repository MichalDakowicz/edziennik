````markdown
# `attendance` - Endpointy API dla zarządzania frekwencją i statusami obecności.

## `StatusyObecnosci`

-   GET (lista statusów)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/statusy/" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy status)

```ps
   curl.exe -X GET http://dziennik.polandcentral.cloudapp.azure.com/api/statusy/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie statusu)

```ps
   curl.exe -X POST http://dziennik.polandcentral.cloudapp.azure.com/api/statusy/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": "Obecny"}'
```

-   PUT (aktualizacja statusu)

```ps
   curl.exe -X PUT http://dziennik.polandcentral.cloudapp.azure.com/api/statusy/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"wartosc": "Nieobecny"}'
```

-   DELETE (usunięcie statusu)

```ps
   curl.exe -X DELETE http://dziennik.polandcentral.cloudapp.azure.com/api/statusy/1/ `
   -H "ADMIN-KEY: "
```

## `Frekwencja`

-   GET (lista wpisów frekwencji)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/frekwencja/" `
   -H "ADMIN-KEY: "
```

-   GET (lista frekwencji dla konkretnego ucznia)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/frekwencja/?uczen_id=1" `
   -H "ADMIN-KEY: "
```

-   GET (lista frekwencji dla konkretnej daty)

```ps
   curl.exe -X GET "http://dziennik.polandcentral.cloudapp.azure.com/api/frekwencja/?date=2025-11-24" `
   -H "ADMIN-KEY: "
```

-   GET (pojedynczy wpis frekwencji)

```ps
   curl.exe -X GET http://dziennik.polandcentral.cloudapp.azure.com/api/frekwencja/1/ `
   -H "ADMIN-KEY: "
```

-   POST (utworzenie wpisu frekwencji)

```ps
   curl.exe -X POST http://dziennik.polandcentral.cloudapp.azure.com/api/frekwencja/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"data":"2025-11-24", "uczen_id": 1, "godzina_lekcyjna_id": 2, "status_id": 1}'
```

-   PUT (aktualizacja wpisu frekwencji)

```ps
   curl.exe -X PUT http://dziennik.polandcentral.cloudapp.azure.com/api/frekwencja/1/ `  -H "ADMIN-KEY: " `
   -H "Content-Type: application/json" `
   -d '{"data":"2025-11-24", "uczen_id": 1, "godzina_lekcyjna_id": 2, "status_id": 2}'
```

-   DELETE (usunięcie wpisu frekwencji)

```ps
   curl.exe -X DELETE http://dziennik.polandcentral.cloudapp.azure.com/api/frekwencja/1/ `
   -H "ADMIN-KEY: "
```

````
