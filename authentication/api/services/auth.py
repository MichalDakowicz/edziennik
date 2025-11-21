from functools import wraps
from django.http import JsonResponse
from decouple import config


def admin_key_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        expected_key = config("ADMIN-KEY", default=None)
        if not expected_key:
            return JsonResponse(
                {"error": "Server configuration error: ADMIN-KEY not set"}, status=500
            )

        # Check header 'ADMIN-KEY'
        received_key = request.headers.get("ADMIN-KEY")

        if not received_key or received_key != expected_key:
            return JsonResponse(
                {"error": "Unauthorized: Invalid or missing ADMIN-KEY"}, status=401
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view
