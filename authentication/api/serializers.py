from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import Uczen, Nauczyciel, Rodzic


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        # Determine user role and add role-specific ID
        try:
            uczen = Uczen.objects.get(user=user)
            token['role'] = 'uczen'
            token['uczen_id'] = uczen.id
            if uczen.klasa:
                token['klasa_id'] = uczen.klasa.id
        except Uczen.DoesNotExist:
            pass

        try:
            nauczyciel = Nauczyciel.objects.get(user=user)
            token['role'] = 'nauczyciel'
            token['nauczyciel_id'] = nauczyciel.id
        except Nauczyciel.DoesNotExist:
            pass

        try:
            rodzic = Rodzic.objects.get(user=user)
            token['role'] = 'rodzic'
            token['rodzic_id'] = rodzic.id
            # Include children IDs for parent
            dzieci_ids = list(rodzic.dzieci.values_list('id', flat=True))
            token['dzieci_ids'] = dzieci_ids
        except Rodzic.DoesNotExist:
            pass

        # Check if user is admin/staff
        if user.is_staff or user.is_superuser:
            token['role'] = 'admin'

        return token
