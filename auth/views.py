from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['nim'] = user.nim
        return token


class JwtObtain(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
