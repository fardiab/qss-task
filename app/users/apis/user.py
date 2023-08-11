from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response


class UserApiView(APIView):
    serualizer_class = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)