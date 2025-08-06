from django.urls import path
from .views import RegisterView, VerifyOTPView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    path('verify/', VerifyOTPView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path('', TemplateView.as_view(template_name='accounts/home.html'), name='home'),
    path('register-form/', TemplateView.as_view(template_name='accounts/register.html'), name='register_form'),
    path('login-form/', TemplateView.as_view(template_name='accounts/login.html'), name='login_form'),
    path('verify-form/', TemplateView.as_view(template_name='accounts/verify.html'), name='verify_form'),
]
