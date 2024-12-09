from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ENT API Documentations",
        default_version='v1',
        description="My API descriptions of ENT",
        terms_of_service="https://www.mcq.gastii.com",
        contact=openapi.Contact(email="mcq@gmail.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('api/', include('api.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('',include('dashboard.urls')),
    # path('ckeditor/' ,include('ckeditor_uploader.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('khalti/', include('khalti.urls')),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

