from typing import Tuple
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

class CookiesJWTAuthencation(JWTAuthentication):
    def authenticate(self, request):
        Acces_token = request.COOKIES.get('access_token')

        if not Acces_token:
            return None
        
        Validate_token = self.get_validated_token(Acces_token)
        try:
            user = self.get_user(Validate_token)
        except:
            return None
        return (user, Validate_token)
    