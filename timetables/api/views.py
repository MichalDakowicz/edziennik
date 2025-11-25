import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from timetables.models import (
    PlanyZajec,
    GodzinyLekcyjne,
    DniTygodnia,
    Zajecia,
    PlanWpis,
    Wydarzenie,
)
from authentication.api.services import admin_key_required


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class GodzinyLekcyjneApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                gl = GodzinyLekcyjne.objects.get(pk=pk)
                data = {
                    "id": gl.id,
                    "Numer": gl.Numer,
                    "CzasOd": gl.CzasOd,
                    "CzasDo": gl.CzasDo,
                    "CzasTrwania": gl.CzasTrwania,
                }
                return JsonResponse(data)
            except GodzinyLekcyjne.DoesNotExist:
                return JsonResponse({"error": "GodzinyLekcyjne not found"}, status=404)
        else:
            qs = GodzinyLekcyjne.objects.all()
            data = []
            for gl in qs:
                data.append(
                    {
                        "id": gl.id,
                        "Numer": gl.Numer,
                        "CzasOd": gl.CzasOd,
                        "CzasDo": gl.CzasDo,
                        "CzasTrwania": gl.CzasTrwania,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("Numer", "CzasOd", "CzasDo", "CzasTrwania")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            gl = GodzinyLekcyjne.objects.create(
                Numer=data["Numer"],
                CzasOd=data["CzasOd"],
                CzasDo=data["CzasDo"],
                CzasTrwania=data["CzasTrwania"],
            )
            return JsonResponse(
                {
                    "id": gl.id,
                    "Numer": gl.Numer,
                    "CzasOd": gl.CzasOd,
                    "CzasDo": gl.CzasDo,
                    "CzasTrwania": gl.CzasTrwania,
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            gl = GodzinyLekcyjne.objects.get(pk=pk)
            data = json.loads(request.body)

            gl.Numer = data.get("Numer", gl.Numer)
            gl.CzasOd = data.get("CzasOd", gl.CzasOd)
            gl.CzasDo = data.get("CzasDo", gl.CzasDo)
            gl.CzasTrwania = data.get("CzasTrwania", gl.CzasTrwania)
            gl.save()

            return JsonResponse(
                {
                    "id": gl.id,
                    "Numer": gl.Numer,
                    "CzasOd": gl.CzasOd,
                    "CzasDo": gl.CzasDo,
                    "CzasTrwania": gl.CzasTrwania,
                }
            )
        except GodzinyLekcyjne.DoesNotExist:
            return JsonResponse({"error": "GodzinyLekcyjne not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            gl = GodzinyLekcyjne.objects.get(pk=pk)
            gl.delete()
            return JsonResponse({"message": "GodzinyLekcyjne deleted"})
        except GodzinyLekcyjne.DoesNotExist:
            return JsonResponse({"error": "GodzinyLekcyjne not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class DniTygodniaApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                d = DniTygodnia.objects.get(pk=pk)
                data = {"id": d.id, "Nazwa": d.Nazwa, "Numer": d.Numer}
                return JsonResponse(data)
            except DniTygodnia.DoesNotExist:
                return JsonResponse({"error": "DniTygodnia not found"}, status=404)
        else:
            qs = DniTygodnia.objects.all().order_by("Numer")
            data = [{"id": d.id, "Nazwa": d.Nazwa, "Numer": d.Numer} for d in qs]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("Nazwa", "Numer")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            d = DniTygodnia.objects.create(Nazwa=data["Nazwa"], Numer=data["Numer"])
            return JsonResponse({"id": d.id, "Nazwa": d.Nazwa, "Numer": d.Numer}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            d = DniTygodnia.objects.get(pk=pk)
            data = json.loads(request.body)

            d.Nazwa = data.get("Nazwa", d.Nazwa)
            d.Numer = data.get("Numer", d.Numer)
            d.save()

            return JsonResponse({"id": d.id, "Nazwa": d.Nazwa, "Numer": d.Numer})
        except DniTygodnia.DoesNotExist:
            return JsonResponse({"error": "DniTygodnia not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            d = DniTygodnia.objects.get(pk=pk)
            d.delete()
            return JsonResponse({"message": "DniTygodnia deleted"})
        except DniTygodnia.DoesNotExist:
            return JsonResponse({"error": "DniTygodnia not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class ZajeciaApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                z = Zajecia.objects.get(pk=pk)
                data = {"id": z.id, "nauczyciel_id": z.nauczyciel_id}
                return JsonResponse(data)
            except Zajecia.DoesNotExist:
                return JsonResponse({"error": "Zajecia not found"}, status=404)
        else:
            qs = Zajecia.objects.all()
            data = [{"id": z.id, "nauczyciel_id": z.nauczyciel_id} for z in qs]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            # Only nauczyciel_id is required in current model
            if "nauczyciel_id" not in data:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            z = Zajecia.objects.create(nauczyciel_id=data["nauczyciel_id"]) 
            return JsonResponse({"id": z.id, "nauczyciel_id": z.nauczyciel_id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            z = Zajecia.objects.get(pk=pk)
            data = json.loads(request.body)

            z.nauczyciel_id = data.get("nauczyciel_id", z.nauczyciel_id)
            z.save()

            return JsonResponse({"id": z.id, "nauczyciel_id": z.nauczyciel_id})
        except Zajecia.DoesNotExist:
            return JsonResponse({"error": "Zajecia not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            z = Zajecia.objects.get(pk=pk)
            z.delete()
            return JsonResponse({"message": "Zajecia deleted"})
        except Zajecia.DoesNotExist:
            return JsonResponse({"error": "Zajecia not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class PlanWpisApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                p = PlanWpis.objects.get(pk=pk)
                data = {
                    "id": p.id,
                    "godzina_lekcyjna_id": p.godzina_lekcyjna_id,
                    "dzien_tygodnia_id": p.dzien_tygodnia_id,
                    "zajecia_id": p.zajecia_id,
                }
                return JsonResponse(data)
            except PlanWpis.DoesNotExist:
                return JsonResponse({"error": "PlanWpis not found"}, status=404)
        else:
            qs = PlanWpis.objects.all()
            data = [
                {
                    "id": p.id,
                    "godzina_lekcyjna_id": p.godzina_lekcyjna_id,
                    "dzien_tygodnia_id": p.dzien_tygodnia_id,
                    "zajecia_id": p.zajecia_id,
                }
                for p in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("godzina_lekcyjna_id", "dzien_tygodnia_id", "zajecia_id")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            p = PlanWpis.objects.create(
                godzina_lekcyjna_id=data["godzina_lekcyjna_id"],
                dzien_tygodnia_id=data["dzien_tygodnia_id"],
                zajecia_id=data["zajecia_id"],
            )
            return JsonResponse(
                {
                    "id": p.id,
                    "godzina_lekcyjna_id": p.godzina_lekcyjna_id,
                    "dzien_tygodnia_id": p.dzien_tygodnia_id,
                    "zajecia_id": p.zajecia_id,
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            p = PlanWpis.objects.get(pk=pk)
            data = json.loads(request.body)

            p.godzina_lekcyjna_id = data.get("godzina_lekcyjna_id", p.godzina_lekcyjna_id)
            p.dzien_tygodnia_id = data.get("dzien_tygodnia_id", p.dzien_tygodnia_id)
            p.zajecia_id = data.get("zajecia_id", p.zajecia_id)
            p.save()

            return JsonResponse(
                {
                    "id": p.id,
                    "godzina_lekcyjna_id": p.godzina_lekcyjna_id,
                    "dzien_tygodnia_id": p.dzien_tygodnia_id,
                    "zajecia_id": p.zajecia_id,
                }
            )
        except PlanWpis.DoesNotExist:
            return JsonResponse({"error": "PlanWpis not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            p = PlanWpis.objects.get(pk=pk)
            p.delete()
            return JsonResponse({"message": "PlanWpis deleted"})
        except PlanWpis.DoesNotExist:
            return JsonResponse({"error": "PlanWpis not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class PlanyZajecApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                pl = PlanyZajec.objects.get(pk=pk)
                data = {
                    "id": pl.id,
                    "ObowiazujeOdDnia": pl.ObowiazujeOdDnia,
                    "wpisy": [w.id for w in pl.wpisy.all()],
                }
                return JsonResponse(data)
            except PlanyZajec.DoesNotExist:
                return JsonResponse({"error": "PlanyZajec not found"}, status=404)
        else:
            qs = PlanyZajec.objects.all()
            data = [
                {"id": pl.id, "ObowiazujeOdDnia": pl.ObowiazujeOdDnia, "wpisy": [w.id for w in pl.wpisy.all()]} 
                for pl in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if "ObowiazujeOdDnia" not in data:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            pl = PlanyZajec.objects.create(ObowiazujeOdDnia=data["ObowiazujeOdDnia"]) 
            # optionally add wpisy if provided
            wpisy = data.get("wpisy")
            if wpisy:
                pl.wpisy.set(wpisy)
            return JsonResponse({"id": pl.id, "ObowiazujeOdDnia": pl.ObowiazujeOdDnia, "wpisy": [w.id for w in pl.wpisy.all()]}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, pk):
        try:
            pl = PlanyZajec.objects.get(pk=pk)
            data = json.loads(request.body)

            pl.ObowiazujeOdDnia = data.get("ObowiazujeOdDnia", pl.ObowiazujeOdDnia)
            pl.save()
            if "wpisy" in data:
                pl.wpisy.set(data["wpisy"]) 

            return JsonResponse({"id": pl.id, "ObowiazujeOdDnia": pl.ObowiazujeOdDnia, "wpisy": [w.id for w in pl.wpisy.all()]})
        except PlanyZajec.DoesNotExist:
            return JsonResponse({"error": "PlanyZajec not found"}, status=404)



@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class WydarzenieApiView(View):


    def get(self, request, pk=None):
        if pk:
            try:
                w = Wydarzenie.objects.get(pk=pk)
                data = {
                    "id": w.id,
                    "tytul": w.tytul,
                    "opis": w.opis,
                    "data": w.data,
                    "klasa_id": getattr(w, "klasa_id", None),
                    "przedmiot_id": getattr(w, "przedmiot_id", None),
                    "nauczyciel_id": getattr(w, "nauczyciel_id", None),
                }
                return JsonResponse(data)
            except Wydarzenie.DoesNotExist:
                return JsonResponse({"error": "Wydarzenie not found"}, status=404)
        else:
            qs = Wydarzenie.objects.all()
            klasa_id = request.GET.get("klasa_id")
            nauczyciel_id = request.GET.get("nauczyciel_id")
            przedmiot_id = request.GET.get("przedmiot_id")
            if klasa_id:
                qs = qs.filter(klasa_id=klasa_id)
            if nauczyciel_id:
                qs = qs.filter(nauczyciel_id=nauczyciel_id)
            if przedmiot_id:
                qs = qs.filter(przedmiot_id=przedmiot_id)

            data = [
                {
                    "id": ev.id,
                    "tytul": ev.tytul,
                    "opis": ev.opis,
                    "data": ev.data,
                    "klasa_id": getattr(ev, "klasa_id", None),
                    "przedmiot_id": getattr(ev, "przedmiot_id", None),
                    "nauczyciel_id": getattr(ev, "nauczyciel_id", None),
                }
                for ev in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("tytul", "opis", "data")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            w = Wydarzenie.objects.create(
                tytul=data["tytul"],
                opis=data["opis"],
                data=data["data"],
                klasa_id=data.get("klasa_id"),
                przedmiot_id=data.get("przedmiot_id"),
                nauczyciel_id=data.get("nauczyciel_id"),
            )
            return JsonResponse({"id": w.id, "message": "Wydarzenie created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            w = Wydarzenie.objects.get(pk=pk)
            data = json.loads(request.body)

            if "tytul" in data:
                w.tytul = data["tytul"]
            if "opis" in data:
                w.opis = data["opis"]
            if "data" in data:
                w.data = data["data"]
            if "klasa_id" in data:
                w.klasa_id = data["klasa_id"]
            if "przedmiot_id" in data:
                w.przedmiot_id = data["przedmiot_id"]
            if "nauczyciel_id" in data:
                w.nauczyciel_id = data["nauczyciel_id"]

            w.save()
            return JsonResponse({"message": "Wydarzenie updated"})
        except Wydarzenie.DoesNotExist:
            return JsonResponse({"error": "Wydarzenie not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            w = Wydarzenie.objects.get(pk=pk)
            w.delete()
            return JsonResponse({"message": "Wydarzenie deleted"}, status=204)
        except Wydarzenie.DoesNotExist:
            return JsonResponse({"error": "Wydarzenie not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            pl = PlanyZajec.objects.get(pk=pk)
            pl.delete()
            return JsonResponse({"message": "PlanyZajec deleted"})
        except PlanyZajec.DoesNotExist:
            return JsonResponse({"error": "PlanyZajec not found"}, status=404)
