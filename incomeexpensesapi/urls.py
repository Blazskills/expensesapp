
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="INCOME EXPENSES API",
        default_version='v1',
        description="Income Expenses Api description",
        terms_of_service="https://www.afexnigeria.com",
        contact=openapi.Contact(email="tilesanmi@afexnigeria.com"),
        license=openapi.License(name="Afex License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    # Addon for swagger docs
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('expenses/', include('expenses.urls')),
    path('income/', include('income.urls')),
    path('userstats/', include('userstats.urls')),




]
