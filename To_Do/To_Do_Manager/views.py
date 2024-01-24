from rest_framework import viewsets, generics
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegisterSerializer, ToDoSerializer
from .models import ToDo, MyUser


class LoginView(ObtainAuthToken):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = MyUser.objects.all()

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "created": created})
        else:
            return Response({"error": "Invalid credentials"}, status=401)


# delete token/logout
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:  # type: ignore
            return get_user_model().objects.all()
        elif user.is_staff:  # type: ignore
            return get_user_model().objects.filter(is_superuser=False)
        elif user.id == int(self.kwargs["pk"]):  # type: ignore
            return get_user_model().objects.filter(id=user.id)  # type: ignore
        else:
            raise PermissionDenied("Not authorized")


class UserAllViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:  # type: ignore
            return get_user_model().objects.all()
        else:
            raise PermissionDenied("Not authorized")


class ListToDoView(generics.ListAPIView):
    serializer_class = ToDoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)


class DetailToDoView(generics.RetrieveAPIView):
    serializer_class = ToDoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)


class UpdateTodoView(generics.UpdateAPIView):
    serializer_class = ToDoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)


class CreateTodoView(generics.CreateAPIView):
    serializer_class = ToDoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteTodoView(generics.DestroyAPIView):
    serializer_class = ToDoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)
