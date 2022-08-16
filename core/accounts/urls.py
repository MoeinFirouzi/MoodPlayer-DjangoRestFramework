from django.urls import path, include
from .api.views import EmailLogin, UsernameLogin, SignUp

urlpatterns = [
    path('login/email/', EmailLogin.as_view(), name="email-login"),
    path('login/username/', UsernameLogin.as_view(), name="email-login"),
    path('signup/', SignUp.as_view(), name="signup"),
]
