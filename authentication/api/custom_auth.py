from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = super().get_header(request)

        # If standard Authorization header is missing, check X-Authorization
        if header is None:
            # Note: headers in request.META are usually uppercase with HTTP_ prefix
            auth_str = request.META.get("HTTP_X_AUTHORIZATION")
            if auth_str:
                if isinstance(auth_str, str):
                    # Work around django-rest-framework-simplejwt expectation of bytes
                    return auth_str.encode("utf-8")
                return auth_str

        return header
