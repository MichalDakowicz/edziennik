import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from . import __name__ as _mod
from attendance.models import StatusyObecnosci, Frekwencja
from authentication.api.services.auth import admin_key_required


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class StatusApiView(View):
	def get(self, request, pk=None):
		if pk:
			try:
				status = StatusyObecnosci.objects.get(pk=pk)
				data = {"id": status.id, "wartosc": status.Wartosc}
				return JsonResponse(data)
			except StatusyObecnosci.DoesNotExist:
				return JsonResponse({"error": "Status not found"}, status=404)
		else:
			statuses = StatusyObecnosci.objects.all()
			data = [{"id": s.id, "wartosc": s.Wartosc} for s in statuses]
			return JsonResponse(data, safe=False)

	def post(self, request):
		try:
			data = json.loads(request.body)
			if "wartosc" not in data:
				return JsonResponse({"error": "Missing required field 'wartosc'"}, status=400)

			status = StatusyObecnosci.objects.create(Wartosc=data["wartosc"])
			return JsonResponse({"id": status.id, "wartosc": status.Wartosc}, status=201)
		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

	def put(self, request, pk):
		try:
			status = StatusyObecnosci.objects.get(pk=pk)
			data = json.loads(request.body)
			status.Wartosc = data.get("wartosc", status.Wartosc)
			status.save()
			return JsonResponse({"id": status.id, "wartosc": status.Wartosc})
		except StatusyObecnosci.DoesNotExist:
			return JsonResponse({"error": "Status not found"}, status=404)
		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

	def delete(self, request, pk):
		try:
			status = StatusyObecnosci.objects.get(pk=pk)
			status.delete()
			return JsonResponse({"message": "Status deleted"})
		except StatusyObecnosci.DoesNotExist:
			return JsonResponse({"error": "Status not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class FrekwencjaApiView(View):
	def get(self, request, pk=None):
		if pk:
			try:
				f = Frekwencja.objects.get(pk=pk)
				data = {
					"id": f.id,
					"data": f.Data,
					"uczen_id": f.uczen.id,
					"godzina_lekcyjna_id": f.godzina_lekcyjna.id if f.godzina_lekcyjna else None,
					"status_id": f.status.id if f.status else None,
				}
				return JsonResponse(data)
			except Frekwencja.DoesNotExist:
				return JsonResponse({"error": "Frekwencja not found"}, status=404)
		else:
			qs = Frekwencja.objects.all()
			# optional filters
			uczen_id = request.GET.get("uczen_id")
			date = request.GET.get("date")
			if uczen_id:
				qs = qs.filter(uczen_id=uczen_id)
			if date:
				qs = qs.filter(Data=date)

			data = []
			for f in qs:
				data.append(
					{
						"id": f.id,
						"data": f.Data,
						"uczen_id": f.uczen.id,
						"godzina_lekcyjna_id": f.godzina_lekcyjna.id if f.godzina_lekcyjna else None,
						"status_id": f.status.id if f.status else None,
					}
				)
			return JsonResponse(data, safe=False)

	def post(self, request):
		try:
			data = json.loads(request.body)
			if not all(k in data for k in ("data", "uczen_id")):
				return JsonResponse({"error": "Missing required fields 'data' and/or 'uczen_id'"}, status=400)

			frek = Frekwencja.objects.create(
				Data=data["data"],
				uczen_id=data["uczen_id"],
				godzina_lekcyjna_id=data.get("godzina_lekcyjna_id"),
				status_id=data.get("status_id"),
			)
			return JsonResponse(
				{
					"id": frek.id,
					"data": frek.Data,
					"uczen_id": frek.uczen.id,
					"godzina_lekcyjna_id": frek.godzina_lekcyjna.id if frek.godzina_lekcyjna else None,
					"status_id": frek.status.id if frek.status else None,
				},
				status=201,
			)
		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

	def put(self, request, pk):
		try:
			frek = Frekwencja.objects.get(pk=pk)
			data = json.loads(request.body)
			frek.Data = data.get("data", frek.Data)
			frek.uczen_id = data.get("uczen_id", frek.uczen.id)
			frek.godzina_lekcyjna_id = data.get("godzina_lekcyjna_id", frek.godzina_lekcyjna.id if frek.godzina_lekcyjna else None)
			frek.status_id = data.get("status_id", frek.status.id if frek.status else None)
			frek.save()
			return JsonResponse({
				"id": frek.id,
				"data": frek.Data,
				"uczen_id": frek.uczen.id,
				"godzina_lekcyjna_id": frek.godzina_lekcyjna.id if frek.godzina_lekcyjna else None,
				"status_id": frek.status.id if frek.status else None,
			})
		except Frekwencja.DoesNotExist:
			return JsonResponse({"error": "Frekwencja not found"}, status=404)
		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON"}, status=400)

	def delete(self, request, pk):
		try:
			frek = Frekwencja.objects.get(pk=pk)
			frek.delete()
			return JsonResponse({"message": "Frekwencja deleted"})
		except Frekwencja.DoesNotExist:
			return JsonResponse({"error": "Frekwencja not found"}, status=404)

