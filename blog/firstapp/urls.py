
from django.urls import path
from .views import Signup,login

urlpatterns = [
    path('register/', Signup.as_view(), name='register_user'),
    path('login/', login.as_view(), name='login_user'),
]
