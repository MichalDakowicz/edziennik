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
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, pk):
        try:
            pl = PlanyZajec.objects.get(pk=pk)
            pl.delete()
            return JsonResponse({"message": "PlanyZajec deleted"})
        except PlanyZajec.DoesNotExist:
            return JsonResponse({"error": "PlanyZajec not found"}, status=404)
