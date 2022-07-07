from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',include('index.urls')),
    path('calculadora/',include('basica.urls')),
    path('calculadora/avancada/',include('avancada.urls')),
    path('alurareceita/',include('alurareceita.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
