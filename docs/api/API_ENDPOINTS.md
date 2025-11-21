# Odniesienia API dla dziennika

## `clients` - Endpointy API dla zarządzania urzytkownikami.

1. GET

```ps
   curl.exe -X GET http://127.0.0.1:8000/api/uczniowie/ `
   -H "ADMIN-KEY: ""
```

2. POST

```ps
   curl.exe -X POST http://127.0.0.1:8000/api/uczniowie/ `  -H "ADMIN-KEY: "" `
   -H "Content-Type: application/json" `
   -d '{\"username\": \"jan_kowalski\", \"password\": \"securepass123\", \"first_name\": \"Jan\", \"last_name\": \"Kowalski\", \"telefon\": \"123456789\", \"data_urodzenia\": \"2010-01-01\"}'
```

3. DELETE

```ps
   curl.exe -X DELETE http://127.0.0.1:8000/api/uczniowie/ `
   -H "ADMIN-KEY: ""
```
