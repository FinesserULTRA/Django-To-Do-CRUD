from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    DetailToDoView,
    CreateTodoView,
    DeleteTodoView,
    ListToDoView,
    UpdateTodoView,
    UserRegistrationView,
    LoginView,
    LogoutView,
    UserAllViewSet,
    UserViewSet,
)

urlpatterns = [
    path("todo/<int:pk>/", DetailToDoView.as_view(), name="todo_detail"),
    path("todo/create/", CreateTodoView.as_view(), name="todo_create"),
    path("todo/delete/<int:pk>/", DeleteTodoView.as_view(), name="todo_delete"),
    path("todo/list/", ListToDoView.as_view(), name="todo_list"),
    path("todo/update/<int:pk>/", UpdateTodoView.as_view(), name="todo_update"),
    path(
        "register/", csrf_exempt(UserRegistrationView.as_view()), name="auth_register"
    ),
    path("login/", LoginView.as_view(), name="auth_login"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("users/", UserAllViewSet.as_view({"get": "list"}), name="user_list"),
    path(
        "users/<int:pk>/", UserViewSet.as_view({"get": "retrieve"}), name="user_detail"
    ),
]
