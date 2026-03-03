import datetime
import hashlib

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Klasa


class LuckyNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        klasa_id = request.query_params.get("klasa")
        student_count = 30

        if klasa_id:
            try:
                klasa = Klasa.objects.prefetch_related("uczniowie").get(pk=klasa_id)
                count = klasa.uczniowie.count()
                if count > 0:
                    student_count = count
            except Klasa.DoesNotExist:
                pass

        today = datetime.date.today().isoformat()
        seed = int(hashlib.md5(f"{today}-{klasa_id}".encode()).hexdigest(), 16)
        number = (seed % student_count) + 1

        return Response(
            {"date": today, "lucky_number": number, "klasa_id": klasa_id}
        )
