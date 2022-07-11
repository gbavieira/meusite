from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    path('',include('index.urls')),
    path('calculadora/',include('basica.urls')),
    path('calculadora/avancada/',include('avancada.urls')),
    path('alurareceita/',include('alurareceita.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', favicon_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
