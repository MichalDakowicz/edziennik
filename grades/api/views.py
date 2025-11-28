import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from grades.models import Ocena, OcenaOkresowa, OcenaKoncowa, ZachowaniePunkty
from authentication.api.services import admin_key_required


def _to_string(value):
    return str(value) if value is not None else None


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class OcenaApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                ocena = Ocena.objects.get(pk=pk)
                data = {
                    "id": ocena.id,
                    "wartosc": _to_string(ocena.wartosc),
                    "data": _to_string(getattr(ocena, "data_wystawienia", None)),
                    "uczen_id": ocena.uczen_id,
                    "przedmiot_id": getattr(ocena, "przedmiot_id", None),
                }
                return JsonResponse(data)
            except Ocena.DoesNotExist:
                return JsonResponse({"error": "Ocena not found"}, status=404)
        else:
            oceny = Ocena.objects.all()

            user_id = request.GET.get("user_id")
            if user_id:
                oceny = oceny.filter(uczen_id=user_id)

            oceny = oceny.values(
                "id",
                "wartosc",
                "data_wystawienia",
                "uczen_id",
                "przedmiot_id",
            )

            data = [
                {
                    "id": entry["id"],
                    "wartosc": _to_string(entry["wartosc"]),
                    "data": _to_string(entry["data_wystawienia"]),
                    "uczen_id": entry["uczen_id"],
                    "przedmiot_id": entry.get("przedmiot_id"),
                }
                for entry in oceny
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("wartosc", "uczen_id", "przedmiot_id")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            ocena = Ocena.objects.create(
                wartosc=data["wartosc"],
                uczen_id=data["uczen_id"],
                przedmiot_id=data["przedmiot_id"],
                data_wystawienia=data.get("data"),
            )
            return JsonResponse(
                {
                    "id": ocena.id,
                    "wartosc": _to_string(ocena.wartosc),
                    "data": _to_string(getattr(ocena, "data_wystawienia", None)),
                    "uczen_id": ocena.uczen_id,
                    "przedmiot_id": getattr(ocena, "przedmiot_id", None),
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            ocena = Ocena.objects.get(pk=pk)
            data = json.loads(request.body)

            ocena.wartosc = data.get("wartosc", ocena.wartosc)
            # map incoming 'data' to model's 'data_wystawienia'
            if "data" in data:
                ocena.data_wystawienia = data["data"]
            ocena.uczen_id = data.get("uczen_id", ocena.uczen_id)
            if "przedmiot_id" in data:
                ocena.przedmiot_id = data.get(
                    "przedmiot_id", getattr(ocena, "przedmiot_id", None)
                )
            ocena.save()

            return JsonResponse(
                {
                    "id": ocena.id,
                    "wartosc": _to_string(ocena.wartosc),
                    "data": _to_string(getattr(ocena, "data_wystawienia", None)),
                    "uczen_id": ocena.uczen_id,
                    "przedmiot_id": getattr(ocena, "przedmiot_id", None),
                }
            )
        except Ocena.DoesNotExist:
            return JsonResponse({"error": "Ocena not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            ocena = Ocena.objects.get(pk=pk)
            ocena.delete()
            return JsonResponse({"message": "Ocena deleted"})
        except Ocena.DoesNotExist:
            return JsonResponse({"error": "Ocena not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class OcenaOkresowaApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                ocena_okresowa = OcenaOkresowa.objects.get(pk=pk)
                data = {
                    "id": ocena_okresowa.id,
                    "wartosc": _to_string(ocena_okresowa.wartosc),
                    "okres": ocena_okresowa.okres,
                    "uczen_id": ocena_okresowa.uczen_id,
                    "nauczyciel_id": getattr(ocena_okresowa, "nauczyciel_id", None),
                }
                return JsonResponse(data)
            except OcenaOkresowa.DoesNotExist:
                return JsonResponse({"error": "OcenaOkresowa not found"}, status=404)
        else:
            oceny_okresowe = OcenaOkresowa.objects.all()

            user_id = request.GET.get("user_id")
            if user_id:
                oceny_okresowe = oceny_okresowe.filter(uczen_id=user_id)

            oceny_okresowe = oceny_okresowe.values(
                "id",
                "wartosc",
                "okres",
                "uczen_id",
                "nauczyciel_id",
            )

            data = [
                {
                    "id": entry["id"],
                    "wartosc": _to_string(entry["wartosc"]),
                    "okres": entry["okres"],
                    "uczen_id": entry["uczen_id"],
                    "nauczyciel_id": entry.get("nauczyciel_id"),
                }
                for entry in oceny_okresowe
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("wartosc", "okres", "uczen_id")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            ocena_okresowa = OcenaOkresowa.objects.create(
                wartosc=data["wartosc"],
                okres=data["okres"],
                uczen_id=data["uczen_id"],
                nauczyciel_id=data.get("nauczyciel_id"),
            )
            return JsonResponse(
                {
                    "id": ocena_okresowa.id,
                    "wartosc": _to_string(ocena_okresowa.wartosc),
                    "okres": ocena_okresowa.okres,
                    "uczen_id": ocena_okresowa.uczen_id,
                    "nauczyciel_id": getattr(ocena_okresowa, "nauczyciel_id", None),
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            ocena_okresowa = OcenaOkresowa.objects.get(pk=pk)
            data = json.loads(request.body)

            ocena_okresowa.wartosc = data.get("wartosc", ocena_okresowa.wartosc)
            ocena_okresowa.okres = data.get("okres", ocena_okresowa.okres)
            ocena_okresowa.uczen_id = data.get("uczen_id", ocena_okresowa.uczen_id)
            if "nauczyciel_id" in data:
                ocena_okresowa.nauczyciel_id = data.get("nauczyciel_id")
            ocena_okresowa.save()

            return JsonResponse(
                {
                    "id": ocena_okresowa.id,
                    "wartosc": _to_string(ocena_okresowa.wartosc),
                    "okres": ocena_okresowa.okres,
                    "uczen_id": ocena_okresowa.uczen_id,
                    "nauczyciel_id": getattr(ocena_okresowa, "nauczyciel_id", None),
                }
            )
        except OcenaOkresowa.DoesNotExist:
            return JsonResponse({"error": "OcenaOkresowa not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            ocena_okresowa = OcenaOkresowa.objects.get(pk=pk)
            ocena_okresowa.delete()
            return JsonResponse({"message": "OcenaOkresowa deleted"})
        except OcenaOkresowa.DoesNotExist:
            return JsonResponse({"error": "OcenaOkresowa not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class OcenaKoncowaApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                ocena_koncowa = OcenaKoncowa.objects.get(pk=pk)
                data = {
                    "id": ocena_koncowa.id,
                    "wartosc": _to_string(ocena_koncowa.wartosc),
                    "uczen_id": ocena_koncowa.uczen_id,
                    "przedmiot_id": getattr(ocena_koncowa, "przedmiot_id", None),
                    "nauczyciel_id": getattr(ocena_koncowa, "nauczyciel_id", None),
                }
                return JsonResponse(data)
            except OcenaKoncowa.DoesNotExist:
                return JsonResponse({"error": "OcenaKoncowa not found"}, status=404)
        else:
            oceny_koncowe = OcenaKoncowa.objects.all()

            user_id = request.GET.get("user_id")
            if user_id:
                oceny_koncowe = oceny_koncowe.filter(uczen_id=user_id)

            oceny_koncowe = oceny_koncowe.values(
                "id",
                "wartosc",
                "uczen_id",
                "przedmiot_id",
                "nauczyciel_id",
            )

            data = [
                {
                    "id": entry["id"],
                    "wartosc": _to_string(entry["wartosc"]),
                    "uczen_id": entry["uczen_id"],
                    "przedmiot_id": entry.get("przedmiot_id"),
                    "nauczyciel_id": entry.get("nauczyciel_id"),
                }
                for entry in oceny_koncowe
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("wartosc", "uczen_id", "przedmiot_id")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            ocena_koncowa = OcenaKoncowa.objects.create(
                wartosc=data["wartosc"],
                uczen_id=data["uczen_id"],
                przedmiot_id=data["przedmiot_id"],
            )
            return JsonResponse(
                {
                    "id": ocena_koncowa.id,
                    "wartosc": _to_string(ocena_koncowa.wartosc),
                    "uczen_id": ocena_koncowa.uczen_id,
                    "przedmiot_id": getattr(ocena_koncowa, "przedmiot_id", None),
                    "nauczyciel_id": getattr(ocena_koncowa, "nauczyciel_id", None),
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            ocena_koncowa = OcenaKoncowa.objects.get(pk=pk)
            data = json.loads(request.body)

            ocena_koncowa.wartosc = data.get("wartosc", ocena_koncowa.wartosc)
            ocena_koncowa.uczen_id = data.get("uczen_id", ocena_koncowa.uczen_id)
            if "przedmiot_id" in data:
                ocena_koncowa.przedmiot_id = data.get("przedmiot_id")
            if "nauczyciel_id" in data:
                ocena_koncowa.nauczyciel_id = data.get("nauczyciel_id")
            ocena_koncowa.save()

            return JsonResponse(
                {
                    "id": ocena_koncowa.id,
                    "wartosc": _to_string(ocena_koncowa.wartosc),
                    "uczen_id": ocena_koncowa.uczen_id,
                    "przedmiot_id": getattr(ocena_koncowa, "przedmiot_id", None),
                    "nauczyciel_id": getattr(ocena_koncowa, "nauczyciel_id", None),
                }
            )
        except OcenaKoncowa.DoesNotExist:
            return JsonResponse({"error": "OcenaKoncowa not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            ocena_koncowa = OcenaKoncowa.objects.get(pk=pk)
            ocena_koncowa.delete()
            return JsonResponse({"message": "OcenaKoncowa deleted"})
        except OcenaKoncowa.DoesNotExist:
            return JsonResponse({"error": "OcenaKoncowa not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class ZachowaniePunktyApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                zp = ZachowaniePunkty.objects.get(pk=pk)
                data = {
                    "id": zp.id,
                    "uczen_id": zp.uczen_id,
                    "punkty": zp.punkty,
                    "opis": zp.opis,
                    "data_wpisu": _to_string(getattr(zp, "data_wpisu", None)),
                    "nauczyciel_wpisujacy_id": getattr(
                        zp, "nauczyciel_wpisujacy_id", None
                    ),
                }
                return JsonResponse(data)
            except ZachowaniePunkty.DoesNotExist:
                return JsonResponse({"error": "ZachowaniePunkty not found"}, status=404)
        else:
            user_id = request.GET.get("user_id")
            qs = ZachowaniePunkty.objects.all()
            if user_id:
                qs = qs.filter(uczen_id=user_id)
            qs = qs.values(
                "id",
                "uczen_id",
                "punkty",
                "opis",
                "data_wpisu",
                "nauczyciel_wpisujacy_id",
            )

            data = [
                {
                    "id": entry["id"],
                    "uczen_id": entry["uczen_id"],
                    "punkty": entry["punkty"],
                    "opis": entry.get("opis"),
                    "data_wpisu": _to_string(entry.get("data_wpisu")),
                    "nauczyciel_wpisujacy_id": entry.get(
                        "nauczyciel_wpisujacy_id"
                    ),
                }
                for entry in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("uczen_id", "punkty")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            zp = ZachowaniePunkty.objects.create(
                uczen_id=data["uczen_id"],
                punkty=data["punkty"],
                opis=data.get("opis"),
                nauczyciel_wpisujacy_id=data.get("nauczyciel_wpisujacy_id"),
            )
            return JsonResponse(
                {"id": zp.id, "message": "ZachowaniePunkty created"}, status=201
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            zp = ZachowaniePunkty.objects.get(pk=pk)
            data = json.loads(request.body)
            if "punkty" in data:
                zp.punkty = data["punkty"]
            if "opis" in data:
                zp.opis = data["opis"]
            if "nauczyciel_wpisujacy_id" in data:
                zp.nauczyciel_wpisujacy_id = data["nauczyciel_wpisujacy_id"]
            zp.save()
            return JsonResponse({"message": "ZachowaniePunkty updated"})
        except ZachowaniePunkty.DoesNotExist:
            return JsonResponse({"error": "ZachowaniePunkty not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            zp = ZachowaniePunkty.objects.get(pk=pk)
            zp.delete()
            return JsonResponse({"message": "ZachowaniePunkty deleted"}, status=204)
        except ZachowaniePunkty.DoesNotExist:
            return JsonResponse({"error": "ZachowaniePunkty not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
