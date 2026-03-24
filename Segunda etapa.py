"""
=============================================================
  Pro-Gol Watch — Sistema de Gestión de Videos
  Avance 2: Programación Orientada a Objetos
  Archivo: Segunda etapa.py

  Descripción:
    Versión mejorada del Avance 1 usando clases y objetos.
    Clases: Persona y Videos.
    Toda la funcionalidad del Avance 1 se mantiene igual.

  Autor: Luis Santoy — Pro-Gol Watch
=============================================================
"""

import re  # Librería para validaciones con expresiones regulares


# =============================================================
# FUNCIÓN: mostrar_mensaje_validacion
# Función única que centraliza todos los mensajes de error.
# =============================================================
def mostrar_mensaje_validacion(tipo_error):
    """Despliega el letrero de error según el campo inválido."""

    # Diccionario con todos los mensajes de validación del sistema
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

    # Mostrar el mensaje correspondiente al tipo de error
    print(f"\n⚠  {mensajes.get(tipo_error, 'Error de validación desconocido.')}")


# =============================================================
# FUNCIÓN: validar_captura
# Valida el valor según el tipo de campo.
# Retorna True si es válido, False si hay error.
# =============================================================
def validar_captura(valor, tipo):
    """Valida 'valor' según las reglas del campo 'tipo'."""

    if tipo == "nomina":
        # Nómina: solo letras y números
        if not re.fullmatch(r'[A-Za-z0-9]+', valor):
            mostrar_mensaje_validacion("nomina")
            return False

    elif tipo == "nombre":
        # Nombre: solo letras y espacios
        if not re.fullmatch(r'[A-Za-záéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("nombre")
            return False

    elif tipo == "cantidad":
        # Cantidad: solo dígitos y mayor a 0
        if not re.fullmatch(r'[0-9]+', valor):
            mostrar_mensaje_validacion("cantidad")
            return False
        if int(valor) <= 0:
            print("\n⚠  La cantidad de videos debe ser al menos 1.")
            return False

    elif tipo == "titulo":
        # Título: letras, números y espacios
        if not re.fullmatch(r'[A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("titulo")
            return False

    elif tipo == "nombre_vid":
        # Nombre del video: letras, números y espacios
        if not re.fullmatch(r'[A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("nombre_vid")
            return False

    elif tipo == "extension":
        # Extensión: letras y números (sin el punto)
        limpio = valor.lstrip('.')
        if not re.fullmatch(r'[A-Za-z0-9]+', limpio):
            mostrar_mensaje_validacion("extension")
            return False

    elif tipo == "tamano":
        # Tamaño: número entre 0 y 3
        try:
            valor_num = float(valor)
        except ValueError:
            mostrar_mensaje_validacion("tamano_fmt")
            return False
        if valor_num < 0 or valor_num > 3:
            mostrar_mensaje_validacion("tamano_rng")
            return False

    return True  # Valor válido


# =============================================================
# FUNCIÓN: manejar_excepcion
# Maneja y reporta errores de forma centralizada.
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
# Representa al usuario que sube videos al sistema.
# Atributos: nombre, id_nomina
# Métodos: capturar, imprimir y guardar en archivo
# =============================================================
class Persona:

    def __init__(self):
        # Atributo: número de nómina del usuario (alfanumérico)
        self.id_nomina: str = ""
        # Atributo: nombre completo del usuario (solo letras)
        self.nombre: str = ""

    # ── Métodos de captura ─────────────────────────────────

    def capturar_id(self):
        """Solicita y valida el número de nómina al usuario."""
        while True:
            self.id_nomina = input("\nIngresa tu número de nómina: ").strip()
            if validar_captura(self.id_nomina, "nomina"):
                break  # Nómina válida, salir del ciclo

    def capturar_nombre(self):
        """Solicita y valida el nombre completo al usuario."""
        while True:
            self.nombre = input("Ingresa tu nombre completo: ").strip()
            if validar_captura(self.nombre, "nombre"):
                break  # Nombre válido, salir del ciclo

    # ── Métodos de impresión ───────────────────────────────

    def imprimir_id(self):
        """Muestra en pantalla el número de nómina."""
        print(f"  Nómina : {self.id_nomina}")

    def imprimir_nombre(self):
        """Muestra en pantalla el nombre del usuario."""
        print(f"  Nombre : {self.nombre}")

    # ── Método para construir la parte del usuario en salida.txt ──

    def obtener_linea(self, cantidad_videos: int) -> str:
        """
        Retorna la parte del usuario formateada para salida.txt:
        Nómina | Nombre | Cantidad de videos
        """
        return f"{self.id_nomina} | {self.nombre} | {cantidad_videos}"


# =============================================================
# CLASE: Videos
# Representa un video individual que sube el usuario.
# Atributos: nombre_video, extension, tamano, titulo
# Métodos: capturar, imprimir y obtener línea para archivo
# =============================================================
class Videos:

    def __init__(self):
        # Atributo: título descriptivo del video
        self.titulo: str = ""
        # Atributo: nombre del archivo del video
        self.nombre_video: str = ""
        # Atributo: extensión del archivo (.mpg, .mov, etc.)
        self.extension: str = ""
        # Atributo: tamaño del video en MB (máximo 3)
        self.tamano: float = 0.0

    # ── Métodos de captura ─────────────────────────────────

    def capturar_titulo(self):
        """Solicita y valida el título del video."""
        while True:
            self.titulo = input("  Título del video: ").strip()
            if validar_captura(self.titulo, "titulo"):
                break

    def capturar_nombre_video(self):
        """Solicita y valida el nombre del archivo de video."""
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
                self.tamano = float(tamano_str)  # Convertir a número decimal
                break

    # ── Métodos de impresión ───────────────────────────────

    def imprimir_nombre_video(self):
        """Muestra en pantalla el nombre del video."""
        print(f"  Nombre    : {self.nombre_video}")

    def imprimir_extension(self):
        """Muestra en pantalla la extensión del video."""
        print(f"  Extensión : {self.extension}")

    def imprimir_tamano(self):
        """Muestra en pantalla el tamaño del video."""
        print(f"  Tamaño    : {self.tamano} MB")

    def imprimir_titulo(self):
        """Muestra en pantalla el título del video."""
        print(f"  Título    : {self.titulo}")

    # ── Método para construir la parte del video en salida.txt ──

    def obtener_linea(self) -> str:
        """
        Retorna los datos del video formateados para salida.txt:
        Título | Nombre | Extensión | Tamaño
        """
        return f"{self.titulo} | {self.nombre_video} | {self.extension} | {self.tamano}"


# =============================================================
# FUNCIÓN: pedir_datos_usuario
# Usa el objeto Persona para capturar id, nombre y cantidad.
# Retorna la persona y la cantidad de videos.
# =============================================================
def pedir_datos_usuario():
    """
    Crea un objeto Persona, captura sus datos y la cantidad
    de videos que desea subir. Retorna (persona, cantidad).
    """

    print("\n" + "═" * 52)
    print("      PRO-GOL WATCH — Ingreso al sistema")
    print("═" * 52)

    # Crear objeto de tipo Persona
    persona = Persona()

    # Usar los métodos del objeto para capturar datos
    persona.capturar_id()
    persona.capturar_nombre()

    # Capturar cantidad de videos (no es atributo de Persona)
    cantidad: int = 0
    while True:
        cantidad_str = input("¿Cuántos videos deseas subir? ").strip()
        if validar_captura(cantidad_str, "cantidad"):
            cantidad = int(cantidad_str)
            break

    return persona, cantidad


# =============================================================
# FUNCIÓN: capturar_info_video
# Usa el objeto Videos para capturar los datos de un video.
# Retorna el objeto Videos con la información completa.
# =============================================================
def capturar_info_video(numero):
    """
    Crea un objeto Videos, captura todos sus datos
    y lo retorna listo para guardar.
    """

    print(f"\n  ── Video #{numero} {'─' * 35}")

    # Crear objeto de tipo Videos
    video = Videos()

    # Usar los métodos del objeto para capturar cada campo
    video.capturar_titulo()
    video.capturar_nombre_video()
    video.capturar_extension()
    video.capturar_tamano()

    return video


# =============================================================
# FUNCIÓN: guardar_en_archivo
# Usa los métodos de Persona y Videos para construir y
# guardar la línea en salida.txt con el formato requerido.
# =============================================================
def guardar_en_archivo(persona, cantidad, lista_videos):
    """
    Construye la línea usando los métodos de los objetos
    y la escribe en salida.txt. Maneja 2 excepciones.
    """

    try:
        # Obtener la parte del usuario desde el objeto Persona
        linea = persona.obtener_linea(cantidad)

        # Agregar la parte de cada video usando el objeto Videos
        for video in lista_videos:
            linea += f" | {video.obtener_linea()}"

        # Escribir la línea en salida.txt (modo append)
        with open("salida.txt", "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")

        print(f"\n✅ Información guardada correctamente en 'salida.txt'.")

    except PermissionError:
        # Excepción 1: Sin permisos de escritura
        print("\n❌ Error: No tienes permisos para escribir en 'salida.txt'.")

    except IOError as e:
        # Excepción 2: Error de entrada/salida
        manejar_excepcion(e, "escritura del archivo salida.txt")


# =============================================================
# FUNCIÓN PRINCIPAL: main
# Controla el flujo completo usando objetos Persona y Videos.
# =============================================================
def main():
    """
    Función principal del sistema Pro-Gol Watch.
    Usa objetos para capturar, imprimir y guardar información.
    """

    try:
        continuar = True

        while continuar:

            # ── Paso 1: Crear objeto Persona y capturar datos ─
            persona, cantidad = pedir_datos_usuario()

            # ── Paso 2: Confirmar información ─────────────────
            print(f"""
╔══════════════════════════════════════════════════════╗
  Bienvenido {persona.nombre},
  tu número de nómina es {persona.id_nomina}
  y estás intentando subir {cantidad} video(s).
  ¿Es correcta la información? (Sí/No)
╚══════════════════════════════════════════════════════╝""")

            respuesta = input("Tu respuesta: ").strip().lower()

            # ── Caso A: Confirmó con "Sí" ──────────────────────
            if respuesta in ("sí", "si", "s"):

                # ── Paso 3: Crear objetos Videos con ciclo FOR ─
                lista_videos = []

                for i in range(1, cantidad + 1):
                    video = capturar_info_video(i)
                    lista_videos.append(video)

                # ── Paso 4: Imprimir resumen usando los objetos ─
                print("\n📋 Resumen de lo registrado:")
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

                # ── Paso 5: Guardar en salida.txt ──────────────
                guardar_en_archivo(persona, cantidad, lista_videos)

                continuar = False  # Terminar el ciclo principal

            # ── Caso B: Contestó "No" ──────────────────────────
            else:
                print("\n¿Deseas salir del sistema? (Sí/No)")
                salir = input("Tu respuesta: ").strip().lower()

                if salir in ("sí", "si", "s"):
                    print("\nMuchas gracias por haber usado nuestro sistema, hasta pronto.")
                    continuar = False
                else:
                    print("\nVolviendo al inicio del sistema...\n")
                    continuar = True

    except KeyboardInterrupt:
        # Excepción por Ctrl+C
        print("\n\n⚠  Proceso interrumpido. Hasta pronto.")


# =============================================================
# Punto de entrada del script
# =============================================================
if __name__ == "__main__":
    main()
