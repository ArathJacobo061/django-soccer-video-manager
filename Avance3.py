"""
=============================================================
  Pro-Gol Watch — Sistema de Gestión de Videos
  Avance 3: Django + PostgreSQL
  Archivo: Avance3.py

  Descripción:
    Versión del Avance 2 adaptada para guardar toda la
    información en la base de datos Pro_Gol usando Django ORM.

  Autor: Luis Santoy — Pro-Gol Watch
=============================================================
"""

import os
import sys
import re
import django

# Configurar Django para usar nuestro proyecto mis_videos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mis_videos.settings')
django.setup()

# Importar los modelos después de inicializar Django
from videos.models import TBL_Usuario, TBL_Video, TBL_UsuarioVideo


# =============================================================
# FUNCIÓN: mostrar_mensaje_validacion
# Función única que centraliza todos los mensajes de error.
# =============================================================
def mostrar_mensaje_validacion(tipo_error):
    """Despliega el letrero de error según el campo inválido."""

    mensajes = {
        "nomina":     "Nómina en formato incorrecto. Debe capturar solo números y letras.",
        "nombre":     "Nombre de usuario en formato incorrecto. Debe capturar solo letras.",
        "cantidad":   "Cantidad de videos en formato incorrecto. Debe capturar solo números.",
        "titulo":     "Título del video en formato incorrecto. Debe capturar solo números y letras.",
        "nombre_vid": "Nombre del video en formato incorrecto. Debe capturar solo números y letras.",
        "extension":  "Extensión del video en formato incorrecto. Debe capturar solo números y letras.",
        "tamano_fmt": "Tamaño del video en formato incorrecto. Debe capturar solo números.",
        "tamano_rng": "El archivo no debe pesar más de 3 MB.",
    }

    print(f"\n⚠  {mensajes.get(tipo_error, 'Error de validación desconocido.')}")


# =============================================================
# FUNCIÓN: validar_captura
# Valida el valor según el tipo de campo.
# Retorna True si es válido, False si hay error.
# =============================================================
def validar_captura(valor, tipo):
    """Valida 'valor' según las reglas del campo 'tipo'."""

    if tipo == "nomina":
        if not re.fullmatch(r'[A-Za-z0-9]+', valor):
            mostrar_mensaje_validacion("nomina")
            return False

    elif tipo == "nombre":
        if not re.fullmatch(r'[A-Za-záéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("nombre")
            return False

    elif tipo == "cantidad":
        if not re.fullmatch(r'[0-9]+', valor):
            mostrar_mensaje_validacion("cantidad")
            return False
        if int(valor) <= 0:
            print("\n⚠  La cantidad de videos debe ser al menos 1.")
            return False

    elif tipo == "titulo":
        if not re.fullmatch(r'[A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("titulo")
            return False

    elif tipo == "nombre_vid":
        if not re.fullmatch(r'[A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("nombre_vid")
            return False

    elif tipo == "extension":
        limpio = valor.lstrip('.')
        if not re.fullmatch(r'[A-Za-z0-9]+', limpio):
            mostrar_mensaje_validacion("extension")
            return False

    elif tipo == "tamano":
        try:
            valor_num = float(valor)
        except ValueError:
            mostrar_mensaje_validacion("tamano_fmt")
            return False
        if valor_num < 0 or valor_num > 3:
            mostrar_mensaje_validacion("tamano_rng")
            return False

    return True


# =============================================================
# FUNCIÓN: manejar_excepcion
# Maneja errores de forma centralizada.
# =============================================================
def manejar_excepcion(excepcion, contexto=""):
    """Muestra un mensaje claro cuando ocurre una excepción."""
    tipo = type(excepcion).__name__
    mensaje = f"\n❌ Error ({tipo})"
    if contexto:
        mensaje += f" en {contexto}"
    mensaje += f": {excepcion}"
    print(mensaje)


# =============================================================
# CLASE: Persona
# Representa al usuario. Ahora guarda en TBL_Usuario.
# =============================================================
class Persona:

    def __init__(self):
        # Atributo: número de nómina del usuario
        self.id_nomina: str = ""
        # Atributo: nombre completo del usuario
        self.nombre: str = ""

    def capturar_id(self):
        """Solicita y valida el número de nómina."""
        while True:
            self.id_nomina = input("\nIngresa tu número de nómina: ").strip()
            if validar_captura(self.id_nomina, "nomina"):
                break

    def capturar_nombre(self):
        """Solicita y valida el nombre completo."""
        while True:
            self.nombre = input("Ingresa tu nombre completo: ").strip()
            if validar_captura(self.nombre, "nombre"):
                break

    def imprimir_id(self):
        """Muestra el número de nómina en pantalla."""
        print(f"  Nómina : {self.id_nomina}")

    def imprimir_nombre(self):
        """Muestra el nombre del usuario en pantalla."""
        print(f"  Nombre : {self.nombre}")

    def guardar_en_bd(self):
        """
        Guarda o actualiza el usuario en TBL_Usuario.
        Retorna el objeto usuario guardado.
        """
        # get_or_create: busca el usuario o lo crea si no existe
        usuario_obj, creado = TBL_Usuario.objects.get_or_create(
            id_nomina=self.id_nomina,
            defaults={'nombre': self.nombre}
        )
        # Si ya existía, actualizar el nombre
        if not creado:
            usuario_obj.nombre = self.nombre
            usuario_obj.save()

        accion = "registrado" if creado else "actualizado"
        print(f"\n✔ Usuario {accion} en la base de datos.")
        return usuario_obj


# =============================================================
# CLASE: Videos
# Representa un video. Ahora guarda en TBL_Video y TBL_UsuarioVideo.
# =============================================================
class Videos:

    def __init__(self):
        # Atributo: título descriptivo del video
        self.titulo: str = ""
        # Atributo: nombre del archivo de video
        self.nombre_video: str = ""
        # Atributo: extensión del archivo
        self.extension: str = ""
        # Atributo: tamaño en MB (máximo 3)
        self.tamano: float = 0.0

    def capturar_titulo(self):
        """Solicita y valida el título del video."""
        while True:
            self.titulo = input("  Título del video: ").strip()
            if validar_captura(self.titulo, "titulo"):
                break

    def capturar_nombre_video(self):
        """Solicita y valida el nombre del video."""
        while True:
            self.nombre_video = input("  Nombre del video: ").strip()
            if validar_captura(self.nombre_video, "nombre_vid"):
                break

    def capturar_extension(self):
        """Solicita y valida la extensión del video."""
        while True:
            self.extension = input("  Extensión del video (.mpg, .mov, etc.): ").strip()
            if validar_captura(self.extension, "extension"):
                break

    def capturar_tamano(self):
        """Solicita y valida el tamaño del video en MB."""
        while True:
            tamano_str = input("  Tamaño en MB (máx. 3): ").strip()
            if validar_captura(tamano_str, "tamano"):
                self.tamano = float(tamano_str)
                break

    def imprimir_titulo(self):
        """Muestra el título del video en pantalla."""
        print(f"  Título    : {self.titulo}")

    def imprimir_nombre_video(self):
        """Muestra el nombre del video en pantalla."""
        print(f"  Nombre    : {self.nombre_video}")

    def imprimir_extension(self):
        """Muestra la extensión del video en pantalla."""
        print(f"  Extensión : {self.extension}")

    def imprimir_tamano(self):
        """Muestra el tamaño del video en pantalla."""
        print(f"  Tamaño    : {self.tamano} MB")

    def guardar_en_bd(self, usuario_obj):
        """
        Guarda el video en TBL_Video y crea la relación
        en TBL_UsuarioVideo vinculando al usuario dado.
        """
        # Crear el registro del video en TBL_Video
        video_obj = TBL_Video.objects.create(
            titulo=self.titulo,
            nombre_video=self.nombre_video,
            extension=self.extension,
            tamano=self.tamano
        )
        # Crear la relación usuario ↔ video en TBL_UsuarioVideo
        TBL_UsuarioVideo.objects.create(
            usuario=usuario_obj,
            video=video_obj
        )
        return video_obj


# =============================================================
# FUNCIÓN: pedir_datos_usuario
# Crea un objeto Persona y captura sus datos.
# =============================================================
def pedir_datos_usuario():
    """Captura nómina, nombre y cantidad de videos del usuario."""

    print("\n" + "═" * 52)
    print("      PRO-GOL WATCH — Ingreso al sistema")
    print("═" * 52)

    # Crear objeto Persona y capturar datos con sus métodos
    persona = Persona()
    persona.capturar_id()
    persona.capturar_nombre()

    # Capturar cantidad de videos
    cantidad: int = 0
    while True:
        cantidad_str = input("¿Cuántos videos deseas subir? ").strip()
        if validar_captura(cantidad_str, "cantidad"):
            cantidad = int(cantidad_str)
            break

    return persona, cantidad


# =============================================================
# FUNCIÓN: capturar_info_video
# Crea un objeto Videos y captura sus datos.
# =============================================================
def capturar_info_video(numero):
    """Captura título, nombre, extensión y tamaño de un video."""

    print(f"\n  ── Video #{numero} {'─' * 35}")

    # Crear objeto Videos y capturar datos con sus métodos
    video = Videos()
    video.capturar_titulo()
    video.capturar_nombre_video()
    video.capturar_extension()
    video.capturar_tamano()

    return video


# =============================================================
# FUNCIÓN: guardar_en_base_de_datos
# Guarda usuario y videos en PostgreSQL usando Django ORM.
# =============================================================
def guardar_en_base_de_datos(persona, lista_videos):
    """
    Guarda al usuario y todos sus videos en Pro_Gol.
    Maneja 2 excepciones.
    """
    try:
        print("\n💾 Guardando en la base de datos Pro_Gol...")

        # Guardar el usuario en TBL_Usuario
        usuario_obj = persona.guardar_en_bd()

        # Guardar cada video en TBL_Video y TBL_UsuarioVideo
        for i, video in enumerate(lista_videos, start=1):
            video_obj = video.guardar_en_bd(usuario_obj)
            print(f"  ✔ Video #{i} '{video.titulo}' guardado (ID: {video_obj.id_video})")

        print(f"\n✅ {len(lista_videos)} video(s) guardados correctamente en Pro_Gol.")
        return True

    except Exception as e:
        # Excepción 1: Error de conexión o del ORM de Django
        manejar_excepcion(e, "guardado en base de datos")
        return False


# =============================================================
# FUNCIÓN PRINCIPAL: main
# =============================================================
def main():
    """Función principal del sistema Pro-Gol Watch."""

    try:
        continuar = True

        while continuar:

            # Paso 1: Capturar datos del usuario
            persona, cantidad = pedir_datos_usuario()

            # Paso 2: Confirmar información
            print(f"""
╔══════════════════════════════════════════════════════╗
  Bienvenido {persona.nombre},
  tu número de nómina es {persona.id_nomina}
  y estás intentando subir {cantidad} video(s).
  ¿Es correcta la información? (Sí/No)
╚══════════════════════════════════════════════════════╝""")

            respuesta = input("Tu respuesta: ").strip().lower()

            if respuesta in ("sí", "si", "s"):

                # Paso 3: Capturar datos de cada video con ciclo FOR
                lista_videos = []
                for i in range(1, cantidad + 1):
                    video = capturar_info_video(i)
                    lista_videos.append(video)

                # Paso 4: Imprimir resumen usando los métodos de los objetos
                print("\n📋 Resumen:")
                print("  Usuario:")
                persona.imprimir_id()
                persona.imprimir_nombre()
                print("\n  Videos:")
                for i, v in enumerate(lista_videos, start=1):
                    print(f"\n  #{i}:")
                    v.imprimir_titulo()
                    v.imprimir_nombre_video()
                    v.imprimir_extension()
                    v.imprimir_tamano()

                # Paso 5: Guardar en base de datos Pro_Gol
                guardar_en_base_de_datos(persona, lista_videos)

                continuar = False

            else:
                print("\n¿Deseas salir del sistema? (Sí/No)")
                salir = input("Tu respuesta: ").strip().lower()

                if salir in ("sí", "si", "s"):
                    print("\nMuchas gracias por haber usado nuestro sistema, hasta pronto.")
                    continuar = False
                else:
                    print("\nVolviendo al inicio del sistema...\n")

    except KeyboardInterrupt:
        # Excepción 2: El usuario presionó Ctrl+C
        print("\n\n⚠  Proceso interrumpido. Hasta pronto.")


# Punto de entrada del script
if __name__ == "__main__":
    main()
