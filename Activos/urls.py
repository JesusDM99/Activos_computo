from django.urls import path
from . import views
from .views import exit

from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns=[

    path('',views.activos, name='activos'),
    path('logout/', exit ,name="exit"),
    

    path('activos', views.activos, name='activos'),
    path('activos/crear',views.crear_activos, name="crear_activos"),
    path('activos/editar.html/<int:id>',views.editar_activos,name="editar_activos"),

    path('licencias', views.licencias, name='licencias'),
    path('licencias/crear',views.crear_licencias, name="crear_licencias"),
    path('licencias/editar.html/<int:id>',views.editar_licencias,name="editar_licencias"),
    
    path('usuarios', views.usuarios, name='usuarios'),
    path('usuarios/crear',views.crear_usuarios, name="crear_usuarios"),
    path('usuarios/editar.html/<int:id>',views.editar_usuarios,name="editar_usuarios"),


    path('listas/crear_ciudades', views.crear_ciudades, name='crear_ciudades'),
    path('listas/crear_tipos', views.crear_tipos_activos, name='crear_tipos_activos'),
    path('listas/crear_ubicacion', views.crear_ubicacion, name='crear_ubicacion'),
    path('listas/crear_direccion', views.crear_direccion, name='crear_direccion'),
    path('listas/crear_area', views.crear_area, name='crear_area'),
    path('listas/crear_cargo', views.crear_cargo, name='crear_cargo'),
    path('listas/crear_proveedor', views.crear_proveedor, name='crear_proveedor'),
    
    path('actas', views.generar_actas, name='actas'),
     
] 

