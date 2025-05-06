from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),
    path('login/', views.login_view, name='login'),
]