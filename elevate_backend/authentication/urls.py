from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.UserDetailView.as_view(), name="user_detail"),
    path("2fa/enable/", views.Enable2FAView.as_view(), name="enable_2fa"),
    path("2fa/verify/", views.Verify2FAView.as_view(), name="verify_2fa"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
]
