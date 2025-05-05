from rest_framework import viewsets, generics
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect

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


# Template Views
class IndexView(TemplateView):
    template_name = 'index.html'


class DashboardView(LoginRequiredMixin, ListView):
    model = ToDo
    template_name = 'dashboard.html'
    context_object_name = 'todos'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user).order_by('-date')


class LoginPageView(DjangoLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        token, created = Token.objects.get_or_create(user=user)
        messages.success(self.request, f"Welcome back, {user.username}!")
        return HttpResponseRedirect(self.get_success_url())


class RegisterPageView(FormView):
    template_name = 'register.html'
    success_url = reverse_lazy('login_page')

    def post(self, request, *args, **kwargs):
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'password': request.POST.get('password'),
            'password2': request.POST.get('password2')
        }
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login_page')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return self.render_to_response({'errors': serializer.errors})


class LogoutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('index')


class TodoDetailPageView(LoginRequiredMixin, DetailView):
    model = ToDo
    template_name = 'todo_detail.html'
    context_object_name = 'todo'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)


class TodoCreatePageView(LoginRequiredMixin, CreateView):
    model = ToDo
    template_name = 'todo_form.html'
    fields = ['title', 'description', 'date']
    success_url = reverse_lazy('dashboard')
    login_url = '/accounts/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Todo created successfully!")
        return super().form_valid(form)


class TodoUpdatePageView(LoginRequiredMixin, UpdateView):
    model = ToDo
    template_name = 'todo_form.html'
    fields = ['title', 'description', 'date', 'is_completed']
    success_url = reverse_lazy('dashboard')
    login_url = '/accounts/login/'

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Todo updated successfully!")
        return super().form_valid(form)


class TodoDeletePageView(LoginRequiredMixin, DeleteView):
    model = ToDo
    success_url = reverse_lazy('dashboard')
    login_url = '/accounts/login/'

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.delete()
        messages.success(request, "Todo deleted successfully!")
        return redirect(self.success_url)
