from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class ObtainTokenAndIsAdmin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={ 'request': request }
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'is_admin': user.is_superuser,
        })

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class HelloAdminView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        content = {'message': 'Hello, Admin!'}
        return Response(content)


