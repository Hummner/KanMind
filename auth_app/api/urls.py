from django.urls import path
from .views import RegistrationView, LoginView, UserEmailCheck

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-check/<str:email>', UserEmailCheck.as_view(), name='email_check')
]
