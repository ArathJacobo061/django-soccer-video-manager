"""
URLs de la aplicación videos - Pro-Gol Watch
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',        views.index,   name='index'),   # Página principal
    path('guardar/', views.guardar, name='guardar'), # Guardar en BD
    path('exito/',   views.exito,   name='exito'),   # Página de éxito
]
