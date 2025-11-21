import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from clients.models import Uczen
from auth.api.services import admin_key_required


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class UczenApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                uczen = Uczen.objects.get(pk=pk)
                data = {
                    "id": uczen.id,
                    "username": uczen.user.username,
                    "first_name": uczen.user.first_name,
                    "last_name": uczen.user.last_name,
                    "telefon": uczen.telefon,
                    "data_urodzenia": uczen.data_urodzenia,
                }
                return JsonResponse(data)
            except Uczen.DoesNotExist:
                return JsonResponse({"error": "Uczen not found"}, status=404)
        else:
            uczniowie = Uczen.objects.all()
            data = []
            for uczen in uczniowie:
                data.append(
                    {
                        "id": uczen.id,
                        "username": uczen.user.username,
                        "first_name": uczen.user.first_name,
                        "last_name": uczen.user.last_name,
                        "telefon": uczen.telefon,
                        "data_urodzenia": uczen.data_urodzenia,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("username", "password", "data_urodzenia")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if User.objects.filter(username=data["username"]).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
            )
            uczen = Uczen.objects.create(
                user=user,
                telefon=data.get("telefon"),
                data_urodzenia=data["data_urodzenia"],
            )
            return JsonResponse(
                {"id": uczen.id, "message": "Uczen created"}, status=201
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            uczen = Uczen.objects.get(pk=pk)
            data = json.loads(request.body)

            if "telefon" in data:
                uczen.telefon = data["telefon"]
            if "data_urodzenia" in data:
                uczen.data_urodzenia = data["data_urodzenia"]

            user_changed = False
            if "first_name" in data:
                uczen.user.first_name = data["first_name"]
                user_changed = True
            if "last_name" in data:
                uczen.user.last_name = data["last_name"]
                user_changed = True

            if user_changed:
                uczen.user.save()
            uczen.save()

            return JsonResponse({"message": "Uczen updated"})
        except Uczen.DoesNotExist:
            return JsonResponse({"error": "Uczen not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            uczen = Uczen.objects.get(pk=pk)
            user = uczen.user
            uczen.delete()
            user.delete()
            return JsonResponse({"message": "Uczen deleted"}, status=204)
        except Uczen.DoesNotExist:
            return JsonResponse({"error": "Uczen not found"}, status=404)
