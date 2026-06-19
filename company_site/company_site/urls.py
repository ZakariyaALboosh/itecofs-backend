from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView,SpectacularRedocView
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # UI for Swagger (Interactive documentation)
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), 
name='swagger-ui'),
    # UI for ReDoc (Clean, structured documentation)
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), 
name='redoc')
]




