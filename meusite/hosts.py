from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    '',
    host(r'', 'meusite.urls', name='meusite'),
    host(r'calculadorahidreo.localhost:8000', 'basica.urls', name='calculadorahidreo'),
    host(r'alurareceita.localhost:8000', 'alurareceita.urls', name='alurareceita'),
)