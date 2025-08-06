from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.shortcuts import redirect


schema_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version='v1',
        description="Регистрация, логин, подтверждение OTP",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', lambda request: redirect('schema-swagger-ui')),
    path('api/', include('accounts.urls')),  
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
