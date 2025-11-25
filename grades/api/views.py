import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from grades.models import Ocena, OcenaOkresowa, OcenaKoncowa, ZachowaniePunkty
from authentication.api.services import admin_key_required


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class OcenaApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                ocena = Ocena.objects.get(pk=pk)
                data = {
                    "id": ocena.id,
                    "wartosc": ocena.wartosc,
                    "data": ocena.data,
                    "uczen_id": ocena.uczen.id,
                    "przedmiot": ocena.przedmiot,
                }
                return JsonResponse(data)
            except Ocena.DoesNotExist:
                return JsonResponse({"error": "Ocena not found"}, status=404)
        else:
            oceny = Ocena.objects.all()

            # Filter by user_id if provided
            user_id = request.GET.get("user_id")
            if user_id:
                oceny = oceny.filter(uczen_id=user_id)

            data = []
            for ocena in oceny:
                data.append(
                    {
                        "id": ocena.id,
                        "wartosc": ocena.wartosc,
                        "data": ocena.data,
                        "uczen_id": ocena.uczen.id,
                        "przedmiot": ocena.przedmiot,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("wartosc", "data", "uczen_id", "przedmiot")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            ocena = Ocena.objects.create(
                wartosc=data["wartosc"],
                data=data["data"],
                uczen_id=data["uczen_id"],
                przedmiot=data["przedmiot"],
            )
            return JsonResponse(
                {
                    "id": ocena.id,
                    "wartosc": ocena.wartosc,
                    "data": ocena.data,
                    "uczen_id": ocena.uczen.id,
                    "przedmiot": ocena.przedmiot,
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
            ocena.data = data.get("data", ocena.data)
            ocena.uczen_id = data.get("uczen_id", ocena.uczen.id)
            ocena.przedmiot = data.get("przedmiot", ocena.przedmiot)
            ocena.save()

            return JsonResponse(
                {
                    "id": ocena.id,
                    "wartosc": ocena.wartosc,
                    "data": ocena.data,
                    "uczen_id": ocena.uczen.id,
                    "przedmiot": ocena.przedmiot,
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
                    "wartosc": ocena_okresowa.wartosc,
                    "okres": ocena_okresowa.okres,
                    "uczen_id": ocena_okresowa.uczen.id,
                    "przedmiot": ocena_okresowa.przedmiot,
                }
                return JsonResponse(data)
            except OcenaOkresowa.DoesNotExist:
                return JsonResponse({"error": "OcenaOkresowa not found"}, status=404)
        else:
            oceny_okresowe = OcenaOkresowa.objects.all()

            # Filter by user_id if provided
            user_id = request.GET.get("user_id")
            if user_id:
                oceny_okresowe = oceny_okresowe.filter(uczen_id=user_id)

            data = []
            for ocena_okresowa in oceny_okresowe:
                data.append(
                    {
                        "id": ocena_okresowa.id,
                        "wartosc": ocena_okresowa.wartosc,
                        "okres": ocena_okresowa.okres,
                        "uczen_id": ocena_okresowa.uczen.id,
                        "przedmiot": ocena_okresowa.przedmiot,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(
                k in data for k in ("wartosc", "okres", "uczen_id", "przedmiot")
            ):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            ocena_okresowa = OcenaOkresowa.objects.create(
                wartosc=data["wartosc"],
                okres=data["okres"],
                uczen_id=data["uczen_id"],
                przedmiot=data["przedmiot"],
            )
            return JsonResponse(
                {
                    "id": ocena_okresowa.id,
                    "wartosc": ocena_okresowa.wartosc,
                    "okres": ocena_okresowa.okres,
                    "uczen_id": ocena_okresowa.uczen.id,
                    "przedmiot": ocena_okresowa.przedmiot,
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
            ocena_okresowa.uczen_id = data.get("uczen_id", ocena_okresowa.uczen.id)
            ocena_okresowa.przedmiot = data.get("przedmiot", ocena_okresowa.przedmiot)
            ocena_okresowa.save()

            return JsonResponse(
                {
                    "id": ocena_okresowa.id,
                    "wartosc": ocena_okresowa.wartosc,
                    "okres": ocena_okresowa.okres,
                    "uczen_id": ocena_okresowa.uczen.id,
                    "przedmiot": ocena_okresowa.przedmiot,
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
                    "wartosc": ocena_koncowa.wartosc,
                    "rok_szkolny": ocena_koncowa.rok_szkolny,
                    "uczen_id": ocena_koncowa.uczen.id,
                    "przedmiot": ocena_koncowa.przedmiot,
                }
                return JsonResponse(data)
            except OcenaKoncowa.DoesNotExist:
                return JsonResponse({"error": "OcenaKoncowa not found"}, status=404)
        else:
            oceny_koncowe = OcenaKoncowa.objects.all()

            # Filter by user_id if provided
            user_id = request.GET.get("user_id")
            if user_id:
                oceny_koncowe = oceny_koncowe.filter(uczen_id=user_id)

            data = []
            for ocena_koncowa in oceny_koncowe:
                data.append(
                    {
                        "id": ocena_koncowa.id,
                        "wartosc": ocena_koncowa.wartosc,
                        "rok_szkolny": ocena_koncowa.rok_szkolny,
                        "uczen_id": ocena_koncowa.uczen.id,
                        "przedmiot": ocena_koncowa.przedmiot,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(
                k in data for k in ("wartosc", "rok_szkolny", "uczen_id", "przedmiot")
            ):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            ocena_koncowa = OcenaKoncowa.objects.create(
                wartosc=data["wartosc"],
                rok_szkolny=data["rok_szkolny"],
                uczen_id=data["uczen_id"],
                przedmiot=data["przedmiot"],
            )
            return JsonResponse(
                {
                    "id": ocena_koncowa.id,
                    "wartosc": ocena_koncowa.wartosc,
                    "rok_szkolny": ocena_koncowa.rok_szkolny,
                    "uczen_id": ocena_koncowa.uczen.id,
                    "przedmiot": ocena_koncowa.przedmiot,
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
            ocena_koncowa.rok_szkolny = data.get(
                "rok_szkolny", ocena_koncowa.rok_szkolny
            )
            ocena_koncowa.uczen_id = data.get("uczen_id", ocena_koncowa.uczen.id)
            ocena_koncowa.przedmiot = data.get("przedmiot", ocena_koncowa.przedmiot)
            ocena_koncowa.save()

            return JsonResponse(
                {
                    "id": ocena_koncowa.id,
                    "wartosc": ocena_koncowa.wartosc,
                    "rok_szkolny": ocena_koncowa.rok_szkolny,
                    "uczen_id": ocena_koncowa.uczen.id,
                    "przedmiot": ocena_koncowa.przedmiot,
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
                    "uczen_id": zp.uczen.id,
                    "punkty": zp.punkty,
                    "opis": zp.opis,
                    "data_wpisu": zp.data_wpisu,
                    "nauczyciel_wpisujacy_id": zp.nauczyciel_wpisujacy.id if zp.nauczyciel_wpisujacy else None,
                }
                return JsonResponse(data)
            except ZachowaniePunkty.DoesNotExist:
                return JsonResponse({"error": "ZachowaniePunkty not found"}, status=404)
        else:
            user_id = request.GET.get("user_id")
            qs = ZachowaniePunkty.objects.all()
            if user_id:
                qs = qs.filter(uczen_id=user_id)
            data = []
            for zp in qs:
                data.append(
                    {
                        "id": zp.id,
                        "uczen_id": zp.uczen.id,
                        "punkty": zp.punkty,
                        "opis": zp.opis,
                        "data_wpisu": zp.data_wpisu,
                        "nauczyciel_wpisujacy_id": zp.nauczyciel_wpisujacy.id if zp.nauczyciel_wpisujacy else None,
                    }
                )
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
            return JsonResponse({"id": zp.id, "message": "ZachowaniePunkty created"}, status=201)
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
