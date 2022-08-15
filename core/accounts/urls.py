from django.urls import path, include
from .api.views import EmailLogin

urlpatterns = [
    path('login/', EmailLogin.as_view(), name="email-login"),
]
