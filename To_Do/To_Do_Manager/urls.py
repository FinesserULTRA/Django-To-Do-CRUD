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
    # New template views
    IndexView,
    DashboardView,
    LoginPageView,
    RegisterPageView,
    LogoutPageView,
    TodoDetailPageView,
    TodoCreatePageView,
    TodoUpdatePageView,
    TodoDeletePageView,
)

urlpatterns = [
    # API endpoints
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
    
    # Template views
    path("", IndexView.as_view(), name="index"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("accounts/login/", LoginPageView.as_view(), name="login_page"),
    path("accounts/register/", RegisterPageView.as_view(), name="register_page"),
    path("accounts/logout/", LogoutPageView.as_view(), name="logout_page"),
    path("todo/view/<int:pk>/", TodoDetailPageView.as_view(), name="todo_detail_page"),
    path("todo/new/", TodoCreatePageView.as_view(), name="todo_create_page"),
    path("todo/edit/<int:pk>/", TodoUpdatePageView.as_view(), name="todo_update_page"),
    path("todo/remove/<int:pk>/", TodoDeletePageView.as_view(), name="todo_delete_page"),
]
