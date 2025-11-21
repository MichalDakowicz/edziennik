import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from users.models import Uczen, Nauczyciel, Rodzic, UserProfile
from authentication.api.services import admin_key_required


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
                    "email": uczen.user.email,
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
                        "email": uczen.user.email,
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
                email=data.get("email", ""),
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
            if "email" in data:
                uczen.user.email = data["email"]
                user_changed = True
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


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class NauczycielApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                nauczyciel = Nauczyciel.objects.get(pk=pk)
                data = {
                    "id": nauczyciel.id,
                    "username": nauczyciel.user.username,
                    "email": nauczyciel.user.email,
                    "first_name": nauczyciel.user.first_name,
                    "last_name": nauczyciel.user.last_name,
                    "telefon": nauczyciel.telefon,
                }
                return JsonResponse(data)
            except Nauczyciel.DoesNotExist:
                return JsonResponse({"error": "Nauczyciel not found"}, status=404)
        else:
            nauczyciele = Nauczyciel.objects.all()
            data = []
            for nauczyciel in nauczyciele:
                data.append(
                    {
                        "id": nauczyciel.id,
                        "username": nauczyciel.user.username,
                        "email": nauczyciel.user.email,
                        "first_name": nauczyciel.user.first_name,
                        "last_name": nauczyciel.user.last_name,
                        "telefon": nauczyciel.telefon,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("username", "password", "telefon")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if User.objects.filter(username=data["username"]).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                email=data.get("email", ""),
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
            )
            nauczyciel = Nauczyciel.objects.create(
                user=user,
                telefon=data["telefon"],
            )
            return JsonResponse(
                {"id": nauczyciel.id, "message": "Nauczyciel created"}, status=201
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            nauczyciel = Nauczyciel.objects.get(pk=pk)
            data = json.loads(request.body)

            if "telefon" in data:
                nauczyciel.telefon = data["telefon"]

            user_changed = False
            if "email" in data:
                nauczyciel.user.email = data["email"]
                user_changed = True
            if "first_name" in data:
                nauczyciel.user.first_name = data["first_name"]
                user_changed = True
            if "last_name" in data:
                nauczyciel.user.last_name = data["last_name"]
                user_changed = True

            if user_changed:
                nauczyciel.user.save()
            nauczyciel.save()

            return JsonResponse({"message": "Nauczyciel updated"})
        except Nauczyciel.DoesNotExist:
            return JsonResponse({"error": "Nauczyciel not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            nauczyciel = Nauczyciel.objects.get(pk=pk)
            user = nauczyciel.user
            nauczyciel.delete()
            user.delete()
            return JsonResponse({"message": "Nauczyciel deleted"}, status=204)
        except Nauczyciel.DoesNotExist:
            return JsonResponse({"error": "Nauczyciel not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class RodzicApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                rodzic = Rodzic.objects.get(pk=pk)
                data = {
                    "id": rodzic.id,
                    "username": rodzic.user.username,
                    "email": rodzic.user.email,
                    "first_name": rodzic.user.first_name,
                    "last_name": rodzic.user.last_name,
                    "telefon": rodzic.telefon,
                }
                return JsonResponse(data)
            except Rodzic.DoesNotExist:
                return JsonResponse({"error": "Rodzic not found"}, status=404)
        else:
            rodzice = Rodzic.objects.all()
            data = []
            for rodzic in rodzice:
                data.append(
                    {
                        "id": rodzic.id,
                        "username": rodzic.user.username,
                        "email": rodzic.user.email,
                        "first_name": rodzic.user.first_name,
                        "last_name": rodzic.user.last_name,
                        "telefon": rodzic.telefon,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if not all(k in data for k in ("username", "password", "telefon")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if User.objects.filter(username=data["username"]).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                email=data.get("email", ""),
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
            )
            rodzic = Rodzic.objects.create(
                user=user,
                telefon=data["telefon"],
            )
            return JsonResponse(
                {"id": rodzic.id, "message": "Rodzic created"}, status=201
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            rodzic = Rodzic.objects.get(pk=pk)
            data = json.loads(request.body)

            if "telefon" in data:
                rodzic.telefon = data["telefon"]

            user_changed = False
            if "email" in data:
                rodzic.user.email = data["email"]
                user_changed = True
            if "first_name" in data:
                rodzic.user.first_name = data["first_name"]
                user_changed = True
            if "last_name" in data:
                rodzic.user.last_name = data["last_name"]
                user_changed = True

            if user_changed:
                rodzic.user.save()
            rodzic.save()

            return JsonResponse({"message": "Rodzic updated"})
        except Rodzic.DoesNotExist:
            return JsonResponse({"error": "Rodzic not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            rodzic = Rodzic.objects.get(pk=pk)
            user = rodzic.user
            rodzic.delete()
            user.delete()
            return JsonResponse({"message": "Rodzic deleted"}, status=204)
        except Rodzic.DoesNotExist:
            return JsonResponse({"error": "Rodzic not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class UserProfileApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                profile = UserProfile.objects.get(pk=pk)
                data = {
                    "id": profile.id,
                    "user_id": profile.user.id,
                    "username": profile.user.username,
                    "theme_preference": profile.theme_preference,
                }
                return JsonResponse(data)
            except UserProfile.DoesNotExist:
                return JsonResponse({"error": "UserProfile not found"}, status=404)
        else:
            profiles = UserProfile.objects.all()
            data = []
            for profile in profiles:
                data.append(
                    {
                        "id": profile.id,
                        "user_id": profile.user.id,
                        "username": profile.user.username,
                        "theme_preference": profile.theme_preference,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if "user_id" not in data:
                return JsonResponse(
                    {"error": "Missing required field: user_id"}, status=400
                )

            user = User.objects.get(pk=data["user_id"])
            profile = UserProfile.objects.create(
                user=user,
                theme_preference=data.get("theme_preference", "system"),
            )
            return JsonResponse(
                {"id": profile.id, "message": "UserProfile created"}, status=201
            )
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            profile = UserProfile.objects.get(pk=pk)
            data = json.loads(request.body)

            if "theme_preference" in data:
                profile.theme_preference = data["theme_preference"]

            profile.save()
            return JsonResponse({"message": "UserProfile updated"})
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "UserProfile not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            profile = UserProfile.objects.get(pk=pk)
            profile.delete()
            return JsonResponse({"message": "UserProfile deleted"}, status=204)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "UserProfile not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
