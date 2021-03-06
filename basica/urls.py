from django.urls import path
from .views import *

urlpatterns = [
    path('', calculadora, name='calculadora'),
    path('basica', basica, name='basica'),
    path('basica/resultado', basica_resultado, name='basica_resultado'),
    path('avancada', avancada, name='avancada'),
    path('avancada/resultado', avancada_resultado, name='avancada_resultado'),
]