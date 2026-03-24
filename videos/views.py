"""
Views del proyecto Mis Videos - Pro-Gol Watch
Avance 4: Frontend HTML/CSS + Backend Django
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from videos.models import TBL_Usuario, TBL_Video, TBL_UsuarioVideo
import json


def index(request):
    """Vista principal: muestra el formulario de registro."""
    return render(request, 'index.html')


def guardar(request):
    """
    Vista que recibe los datos del formulario vía POST
    y los guarda en la base de datos Pro_Gol.
    """
    if request.method == 'POST':
        try:
            # Obtener datos del usuario desde el formulario
            id_nomina  = request.POST.get('id_nomina', '').strip()
            nombre     = request.POST.get('nombre', '').strip()
            cantidad   = int(request.POST.get('cantidad', 0))

            # Guardar o actualizar el usuario en TBL_Usuario
            usuario, creado = TBL_Usuario.objects.get_or_create(
                id_nomina=id_nomina,
                defaults={'nombre': nombre}
            )
            if not creado:
                usuario.nombre = nombre
                usuario.save()

            # Guardar cada video en TBL_Video y TBL_UsuarioVideo
            for i in range(1, cantidad + 1):
                titulo       = request.POST.get(f'titulo_{i}', '').strip()
                nombre_video = request.POST.get(f'nombre_video_{i}', '').strip()
                extension    = request.POST.get(f'extension_{i}', '').strip()
                tamano       = float(request.POST.get(f'tamano_{i}', 0))

                # Crear el video en TBL_Video
                video = TBL_Video.objects.create(
                    titulo=titulo,
                    nombre_video=nombre_video,
                    extension=extension,
                    tamano=tamano
                )

                # Crear la relación en TBL_UsuarioVideo
                TBL_UsuarioVideo.objects.create(
                    usuario=usuario,
                    video=video
                )

            # Redirigir a página de éxito
            return redirect('exito')

        except Exception as e:
            # Si hay error, regresar con mensaje
            return render(request, 'index.html', {'error': str(e)})

    return redirect('index')


def exito(request):
    """Vista de confirmación: muestra mensaje de éxito."""
    return render(request, 'exito.html')
