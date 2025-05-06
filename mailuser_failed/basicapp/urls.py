from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import include
from .views import activate_user

router = DefaultRouter()

app_name = 'basicapi'
urlpatterns = [
    path('', include(router.urls)),
    path('users/<uuid:activate_token>/activation/', activate_user, name='users-activation'),

]
