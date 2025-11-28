import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from utils.models import Przedmiot, Temat, PracaDomowa, DataSource
from django.contrib.auth import get_user_model
from authentication.api.services import admin_key_required
from django.utils import timezone

User = get_user_model()



@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class PrzedmiotApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                p = Przedmiot.objects.get(pk=pk)
                data = {
                    "id": p.id,
                    "nazwa": p.nazwa,
                    "nazwa_skrocona": p.nazwa_skrocona,
                    "numer": p.numer,
                    "czy_dodatkowy": p.czy_dodatkowy,
                    "nauczyciele": [u.id for u in p.nauczyciele.all()],
                }
                return JsonResponse(data)
            except Przedmiot.DoesNotExist:
                return JsonResponse({"error": "Przedmiot not found"}, status=404)
        else:
            qs = Przedmiot.objects.all()
            data = [
                {
                    "id": p.id,
                    "nazwa": p.nazwa,
                    "nazwa_skrocona": p.nazwa_skrocona,
                    "numer": p.numer,
                    "czy_dodatkowy": p.czy_dodatkowy,
                    "nauczyciele": [u.id for u in p.nauczyciele.all()],
                }
                for p in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if "nazwa" not in data:
                return JsonResponse({"error": "Missing required field: nazwa"}, status=400)

            p = Przedmiot.objects.create(
                nazwa=data["nazwa"],
                nazwa_skrocona=data.get("nazwa_skrocona"),
                numer=data.get("numer"),
                czy_dodatkowy=data.get("czy_dodatkowy", False),
            )
            nauczyciele = data.get("nauczyciele")
            if nauczyciele:
                p.nauczyciele.set(nauczyciele)
            return JsonResponse({"id": p.id, "message": "Przedmiot created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            p = Przedmiot.objects.get(pk=pk)
            data = json.loads(request.body)

            p.nazwa = data.get("nazwa", p.nazwa)
            p.nazwa_skrocona = data.get("nazwa_skrocona", p.nazwa_skrocona)
            p.numer = data.get("numer", p.numer)
            if "czy_dodatkowy" in data:
                p.czy_dodatkowy = bool(data["czy_dodatkowy"])
            p.save()
            if "nauczyciele" in data:
                p.nauczyciele.set(data["nauczyciele"])

            return JsonResponse({"message": "Przedmiot updated"})
        except Przedmiot.DoesNotExist:
            return JsonResponse({"error": "Przedmiot not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            p = Przedmiot.objects.get(pk=pk)
            p.delete()
            return JsonResponse({"message": "Przedmiot deleted"}, status=204)
        except Przedmiot.DoesNotExist:
            return JsonResponse({"error": "Przedmiot not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class TematApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                t = Temat.objects.get(pk=pk)
                data = {
                    "id": t.id,
                    "tresc": t.tresc,
                    "data": t.data,
                    "numer_lekcji": t.numer_lekcji,
                    "czas_realizacji": t.czas_realizacji,
                    "czas_od": t.czas_od,
                    "czas_do": t.czas_do,
                    "przedmiot_id": getattr(t, "przedmiot_id", None),
                    "nauczyciel_id": getattr(t, "nauczyciel_id", None),
                }
                return JsonResponse(data)
            except Temat.DoesNotExist:
                return JsonResponse({"error": "Temat not found"}, status=404)
        else:
            qs = Temat.objects.all()
            data = [
                {
                    "id": t.id,
                    "tresc": t.tresc,
                    "data": t.data,
                    "numer_lekcji": t.numer_lekcji,
                    "czas_realizacji": t.czas_realizacji,
                    "czas_od": t.czas_od,
                    "czas_do": t.czas_do,
                    "przedmiot_id": getattr(t, "przedmiot_id", None),
                    "nauczyciel_id": getattr(t, "nauczyciel_id", None),
                }
                for t in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            # minimal required: can be just 'tresc' or more
            t = Temat.objects.create(
                tresc=data.get("tresc"),
                data=data.get("data"),
                numer_lekcji=data.get("numer_lekcji"),
                czas_realizacji=data.get("czas_realizacji"),
                czas_od=data.get("czas_od"),
                czas_do=data.get("czas_do"),
                przedmiot_id=data.get("przedmiot_id"),
                nauczyciel_id=data.get("nauczyciel_id"),
            )
            return JsonResponse({"id": t.id, "message": "Temat created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            t = Temat.objects.get(pk=pk)
            data = json.loads(request.body)

            for field in ("tresc", "data", "numer_lekcji", "czas_realizacji", "czas_od", "czas_do"):
                if field in data:
                    setattr(t, field, data[field])
            if "przedmiot_id" in data:
                t.przedmiot_id = data["przedmiot_id"]
            if "nauczyciel_id" in data:
                t.nauczyciel_id = data["nauczyciel_id"]
            t.save()
            return JsonResponse({"message": "Temat updated"})
        except Temat.DoesNotExist:
            return JsonResponse({"error": "Temat not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            t = Temat.objects.get(pk=pk)
            t.delete()
            return JsonResponse({"message": "Temat deleted"}, status=204)
        except Temat.DoesNotExist:
            return JsonResponse({"error": "Temat not found"}, status=404)



@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class PracaDomowaApiView(View):
    """CRUD API for PracaDomowa (homework)."""

    def get(self, request, pk=None):
        if pk:
            try:
                p = PracaDomowa.objects.get(pk=pk)
                data = {
                    "id": p.id,
                    "klasa_id": getattr(p, "klasa_id", None),
                    "przedmiot_id": getattr(p, "przedmiot_id", None),
                    "nauczyciel_id": getattr(p, "nauczyciel_id", None),
                    "opis": p.opis,
                    "data_wystawienia": p.data_wystawienia,
                    "termin": p.termin,
                }
                return JsonResponse(data)
            except PracaDomowa.DoesNotExist:
                return JsonResponse({"error": "PracaDomowa not found"}, status=404)
        else:
            qs = PracaDomowa.objects.all()
            klasa_id = request.GET.get("klasa_id")
            przedmiot_id = request.GET.get("przedmiot_id")
            nauczyciel_id = request.GET.get("nauczyciel_id")
            if klasa_id:
                qs = qs.filter(klasa_id=klasa_id)
            if przedmiot_id:
                qs = qs.filter(przedmiot_id=przedmiot_id)
            if nauczyciel_id:
                qs = qs.filter(nauczyciel_id=nauczyciel_id)

            data = [
                {
                    "id": pd.id,
                    "klasa_id": getattr(pd, "klasa_id", None),
                    "przedmiot_id": getattr(pd, "przedmiot_id", None),
                    "nauczyciel_id": getattr(pd, "nauczyciel_id", None),
                    "opis": pd.opis,
                    "data_wystawienia": pd.data_wystawienia,
                    "termin": pd.termin,
                }
                for pd in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("klasa_id", "przedmiot_id", "nauczyciel_id", "opis", "termin")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            pd = PracaDomowa.objects.create(
                klasa_id=data["klasa_id"],
                przedmiot_id=data["przedmiot_id"],
                nauczyciel_id=data["nauczyciel_id"],
                opis=data["opis"],
                termin=data["termin"],
            )
            return JsonResponse({"id": pd.id, "message": "PracaDomowa created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class DataSourceApiView(View):
    """API to view and update the singleton DataSource settings."""

    def get(self, request):
        try:
            ds = DataSource.objects.get_or_create(pk=1)[0]
            data = {
                "active_source": ds.active_source,
                "last_import_file": ds.last_import_file,
                "last_imported_at": ds.last_imported_at,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def post(self, request):
        # set active source and optional filename
        try:
            data = json.loads(request.body)
            if "active_source" not in data:
                return JsonResponse({"error": "Missing required field: active_source"}, status=400)
            ds = DataSource.objects.get_or_create(pk=1)[0]
            ds.active_source = data["active_source"]
            if "last_import_file" in data:
                ds.last_import_file = data["last_import_file"]
                ds.last_imported_at = timezone.now()
            ds.save()
            return JsonResponse({"message": "DataSource updated", "active_source": ds.active_source})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            pd = PracaDomowa.objects.get(pk=pk)
            data = json.loads(request.body)

            if "opis" in data:
                pd.opis = data["opis"]
            if "termin" in data:
                pd.termin = data["termin"]
            if "klasa_id" in data:
                pd.klasa_id = data["klasa_id"]
            if "przedmiot_id" in data:
                pd.przedmiot_id = data["przedmiot_id"]
            if "nauczyciel_id" in data:
                pd.nauczyciel_id = data["nauczyciel_id"]

            pd.save()
            return JsonResponse({"message": "PracaDomowa updated"})
        except PracaDomowa.DoesNotExist:
            return JsonResponse({"error": "PracaDomowa not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            pd = PracaDomowa.objects.get(pk=pk)
            pd.delete()
            return JsonResponse({"message": "PracaDomowa deleted"}, status=204)
        except PracaDomowa.DoesNotExist:
            return JsonResponse({"error": "PracaDomowa not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
