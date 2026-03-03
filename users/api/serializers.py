from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Uczen, Nauczyciel, Rodzic, UserProfile, Klasa, Adres, Wiadomosc

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserDisplaySerializer(serializers.ModelSerializer):
    """Read-only serializer for looking up user display info by id (e.g. message senders)."""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]
        read_only_fields = fields


class AdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adres
        fields = "__all__"


class KlasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klasa
        fields = "__all__"


class UczenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Uczen
        fields = ["id", "user", "klasa", "telefon", "data_urodzenia", "adres"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        uczen = Uczen.objects.create(user=user, **validated_data)
        return uczen

    def update(self, instance, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user = instance.user
            for attr, value in user_data.items():
                if attr == "password":
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)


class NauczycielSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Nauczyciel
        fields = ["id", "user", "telefon"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        nauczyciel = Nauczyciel.objects.create(user=user, **validated_data)
        return nauczyciel

    def update(self, instance, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user = instance.user
            for attr, value in user_data.items():
                if attr == "password":
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)


class RodzicSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rodzic
        fields = ["id", "user", "telefon", "dzieci"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        dzieci = validated_data.pop("dzieci", [])
        user = User.objects.create_user(**user_data)
        rodzic = Rodzic.objects.create(user=user, **validated_data)
        rodzic.dzieci.set(dzieci)
        return rodzic

    def update(self, instance, validated_data):
        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user = instance.user
            for attr, value in user_data.items():
                if attr == "password":
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    # Usually UserProfile is created automatically or linked.
    # Exposing User field for read
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"


class WiadomoscSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiadomosc
        fields = "__all__"
