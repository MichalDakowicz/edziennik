import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from users.models import Uczen, Nauczyciel, Rodzic, UserProfile, Klasa, Adres
from users.models import Wiadomosc
from authentication.api.services import admin_key_required
from django.db.models import Q


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



@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class WiadomoscApiView(View):

    def get(self, request, pk=None):
        if pk:
            try:
                w = Wiadomosc.objects.get(pk=pk)
                data = {
                    "id": w.id,
                    "nadawca_id": w.nadawca.id,
                    "nadawca_username": w.nadawca.username,
                    "odbiorca_id": w.odbiorca.id,
                    "odbiorca_username": w.odbiorca.username,
                    "przeczytana": w.przeczytana,
                    "temat": w.temat,
                    "tresc": w.tresc,
                    "data_wyslania": w.data_wyslania,
                }
                return JsonResponse(data)
            except Wiadomosc.DoesNotExist:
                return JsonResponse({"error": "Wiadomosc not found"}, status=404)
        else:
            user_id = request.GET.get("user_id")
            qs = Wiadomosc.objects.all()
            if user_id:
                qs = qs.filter(Q(nadawca__id=user_id) | Q(odbiorca__id=user_id))
            data = []
            for w in qs:
                data.append(
                    {
                        "id": w.id,
                        "nadawca_id": w.nadawca.id,
                        "nadawca_username": w.nadawca.username,
                        "odbiorca_id": w.odbiorca.id,
                        "odbiorca_username": w.odbiorca.username,
                        "przeczytana": w.przeczytana,
                        "temat": w.temat,
                        "tresc": w.tresc,
                        "data_wyslania": w.data_wyslania,
                    }
                )
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            # required fields
            if not all(k in data for k in ("nadawca_id", "odbiorca_id", "temat", "tresc")):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            nadawca = User.objects.get(pk=data["nadawca_id"])
            odbiorca = User.objects.get(pk=data["odbiorca_id"])

            w = Wiadomosc.objects.create(
                nadawca=nadawca,
                odbiorca=odbiorca,
                temat=data["temat"],
                tresc=data["tresc"],
            )
            return JsonResponse({"id": w.id, "message": "Wiadomosc created"}, status=201)
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
            w = Wiadomosc.objects.get(pk=pk)
            data = json.loads(request.body)

            if "temat" in data:
                w.temat = data["temat"]
            if "tresc" in data:
                w.tresc = data["tresc"]
            if "przeczytana" in data:
                w.przeczytana = bool(data["przeczytana"])

            w.save()
            return JsonResponse({"message": "Wiadomosc updated"})
        except Wiadomosc.DoesNotExist:
            return JsonResponse({"error": "Wiadomosc not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            w = Wiadomosc.objects.get(pk=pk)
            w.delete()
            return JsonResponse({"message": "Wiadomosc deleted"}, status=204)
        except Wiadomosc.DoesNotExist:
            return JsonResponse({"error": "Wiadomosc not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class KlasaApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                k = Klasa.objects.get(pk=pk)
                data = {
                    "id": k.id,
                    "nazwa": k.nazwa,
                    "numer": k.numer,
                    "wychowawca_id": getattr(k, "wychowawca_id", None),
                }
                return JsonResponse(data)
            except Klasa.DoesNotExist:
                return JsonResponse({"error": "Klasa not found"}, status=404)
        else:
            qs = Klasa.objects.all()
            data = [
                {"id": k.id, "nazwa": k.nazwa, "numer": k.numer, "wychowawca_id": getattr(k, "wychowawca_id", None)}
                for k in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            if "nazwa" not in data and "numer" not in data:
                return JsonResponse({"error": "Missing required field: nazwa or numer"}, status=400)
            k = Klasa.objects.create(
                nazwa=data.get("nazwa"),
                numer=data.get("numer"),
                wychowawca_id=data.get("wychowawca_id"),
            )
            return JsonResponse({"id": k.id, "message": "Klasa created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            k = Klasa.objects.get(pk=pk)
            data = json.loads(request.body)
            if "nazwa" in data:
                k.nazwa = data["nazwa"]
            if "numer" in data:
                k.numer = data["numer"]
            if "wychowawca_id" in data:
                k.wychowawca_id = data["wychowawca_id"]
            k.save()
            return JsonResponse({"message": "Klasa updated"})
        except Klasa.DoesNotExist:
            return JsonResponse({"error": "Klasa not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            k = Klasa.objects.get(pk=pk)
            k.delete()
            return JsonResponse({"message": "Klasa deleted"}, status=204)
        except Klasa.DoesNotExist:
            return JsonResponse({"error": "Klasa not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(admin_key_required, name="dispatch")
class AdresApiView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                a = Adres.objects.get(pk=pk)
                data = {
                    "id": a.id,
                    "ulica": a.ulica,
                    "numer_domu": a.numer_domu,
                    "numer_mieszkania": a.numer_mieszkania,
                    "miasto": a.miasto,
                    "kod_pocztowy": a.kod_pocztowy,
                    "kraj": a.kraj,
                }
                return JsonResponse(data)
            except Adres.DoesNotExist:
                return JsonResponse({"error": "Adres not found"}, status=404)
        else:
            qs = Adres.objects.all()
            data = [
                {
                    "id": a.id,
                    "ulica": a.ulica,
                    "numer_domu": a.numer_domu,
                    "numer_mieszkania": a.numer_mieszkania,
                    "miasto": a.miasto,
                    "kod_pocztowy": a.kod_pocztowy,
                    "kraj": a.kraj,
                }
                for a in qs
            ]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            a = Adres.objects.create(
                ulica=data.get("ulica"),
                numer_domu=data.get("numer_domu"),
                numer_mieszkania=data.get("numer_mieszkania"),
                miasto=data.get("miasto"),
                kod_pocztowy=data.get("kod_pocztowy"),
                kraj=data.get("kraj"),
            )
            return JsonResponse({"id": a.id, "message": "Adres created"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method PUT requires a pk"}, status=400)
        try:
            a = Adres.objects.get(pk=pk)
            data = json.loads(request.body)
            for field in ("ulica", "numer_domu", "numer_mieszkania", "miasto", "kod_pocztowy", "kraj"):
                if field in data:
                    setattr(a, field, data[field])
            a.save()
            return JsonResponse({"message": "Adres updated"})
        except Adres.DoesNotExist:
            return JsonResponse({"error": "Adres not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk=None):
        if not pk:
            return JsonResponse({"error": "Method DELETE requires a pk"}, status=400)
        try:
            a = Adres.objects.get(pk=pk)
            a.delete()
            return JsonResponse({"message": "Adres deleted"}, status=204)
        except Adres.DoesNotExist:
            return JsonResponse({"error": "Adres not found"}, status=404)
