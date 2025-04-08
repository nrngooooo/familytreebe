from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class UUIDTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        if not auth_header.startswith("Token "):
            raise AuthenticationFailed('Invalid token header')

        token = auth_header.split(" ")[1]
        print(token)
        try:
            user = User.nodes.get(token=token)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
