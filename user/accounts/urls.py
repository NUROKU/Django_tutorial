from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True, template_name="accounts/login.html"
        ),
        name="login",
    ),
    path("profile/", views.profile, name="profile"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]