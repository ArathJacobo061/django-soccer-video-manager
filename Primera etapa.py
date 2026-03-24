"""
=============================================================
  Pro-Gol Watch — Sistema de Gestión de Videos
  Avance 1: Python básico
  Archivo: Primera etapa.py

  Descripción:
    Sistema de consola que permite a un usuario registrar
    videos para subir a la plataforma Pro-Gol Watch.
    Valida entradas, usa ciclos y guarda los datos en salida.txt

  Autor: Luis Santoy — Pro-Gol Watch
=============================================================
"""

import re  # Librería para validar con expresiones regulares


# =============================================================
# FUNCIÓN: mostrar_mensaje_validacion
# Muestra el mensaje de error según el tipo de campo inválido.
# Es una sola función que centraliza todos los mensajes.
# =============================================================
def mostrar_mensaje_validacion(tipo_error):
    """Despliega el letrero de error correspondiente al campo."""

    # Diccionario con todos los mensajes de validación
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

    # Imprimir el mensaje del tipo de error recibido
    print(f"\n⚠  {mensajes.get(tipo_error, 'Error de validación desconocido.')}")


# =============================================================
# FUNCIÓN: validar_captura
# Valida el valor ingresado según el tipo de campo.
# Retorna True si es válido, False si no lo es.
# =============================================================
def validar_captura(valor, tipo):
    """
    Valida 'valor' según las reglas del campo 'tipo'.
    Llama a mostrar_mensaje_validacion si hay error.
    """

    if tipo == "nomina":
        # La nómina solo acepta letras y números (alfanumérico)
        if not re.fullmatch(r'[A-Za-z0-9]+', valor):
            mostrar_mensaje_validacion("nomina")
            return False

    elif tipo == "nombre":
        # El nombre solo acepta letras y espacios
        if not re.fullmatch(r'[A-Za-záéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("nombre")
            return False

    elif tipo == "cantidad":
        # La cantidad solo acepta dígitos
        if not re.fullmatch(r'[0-9]+', valor):
            mostrar_mensaje_validacion("cantidad")
            return False
        # Además debe ser mayor a 0
        if int(valor) <= 0:
            print("\n⚠  La cantidad de videos debe ser al menos 1.")
            return False

    elif tipo == "titulo":
        # El título acepta letras, números y espacios
        if not re.fullmatch(r'[A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("titulo")
            return False

    elif tipo == "nombre_vid":
        # El nombre del video acepta letras, números y espacios
        if not re.fullmatch(r'[A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', valor):
            mostrar_mensaje_validacion("nombre_vid")
            return False

    elif tipo == "extension":
        # La extensión acepta letras y números (quitando el punto inicial si lo hay)
        limpio = valor.lstrip('.')
        if not re.fullmatch(r'[A-Za-z0-9]+', limpio):
            mostrar_mensaje_validacion("extension")
            return False

    elif tipo == "tamano":
        # Primero verificar que sea un número válido
        try:
            valor_num = float(valor)
        except ValueError:
            # Si no es número, mostrar error de formato
            mostrar_mensaje_validacion("tamano_fmt")
            return False
        # Verificar que esté dentro del rango permitido (0 a 3 MB)
        if valor_num < 0 or valor_num > 3:
            mostrar_mensaje_validacion("tamano_rng")
            return False

    # Si pasó todas las validaciones, retornar True
    return True


# =============================================================
# FUNCIÓN: manejar_excepcion
# Maneja errores inesperados de forma centralizada.
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
# FUNCIÓN: pedir_datos_usuario
# Solicita y valida: id (nómina), nombre y cantidad de videos.
# Retorna una tupla con los tres valores ya validados.
# =============================================================
def pedir_datos_usuario():
    """
    Pide al usuario su nómina, nombre y cantidad de videos.
    Repite la solicitud de cada campo hasta que sea válido.
    """

    print("\n" + "═" * 52)
    print("      PRO-GOL WATCH — Ingreso al sistema")
    print("═" * 52)

    # ── Capturar número de nómina ──────────────────────────
    # Variable tipo str: almacena el número de nómina alfanumérico
    id_nomina: str = ""
    while True:
        id_nomina = input("\nIngresa tu número de nómina: ").strip()
        if validar_captura(id_nomina, "nomina"):
            break  # Nómina válida, salir del ciclo

    # ── Capturar nombre del usuario ────────────────────────
    # Variable tipo str: almacena el nombre completo del usuario
    nombre: str = ""
    while True:
        nombre = input("Ingresa tu nombre completo: ").strip()
        if validar_captura(nombre, "nombre"):
            break  # Nombre válido, salir del ciclo

    # ── Capturar cantidad de videos ────────────────────────
    # Variable tipo int: almacena cuántos videos subirá
    cantidad: int = 0
    while True:
        cantidad_str = input("¿Cuántos videos deseas subir? ").strip()
        if validar_captura(cantidad_str, "cantidad"):
            cantidad = int(cantidad_str)  # Convertir a entero
            break  # Cantidad válida, salir del ciclo

    return id_nomina, nombre, cantidad


# =============================================================
# FUNCIÓN: capturar_info_video
# Solicita y valida los datos de un video individual.
# Retorna un diccionario con la info del video.
# =============================================================
def capturar_info_video(numero):
    """
    Pide título, nombre, extensión y tamaño de un video.
    Valida cada campo antes de aceptarlo.
    Retorna un dict con la información del video.
    """

    print(f"\n  ── Video #{numero} {'─' * 35}")

    # ── Título del video ───────────────────────────────────
    # Variable tipo str: título descriptivo del video
    titulo: str = ""
    while True:
        titulo = input("  Título del video: ").strip()
        if validar_captura(titulo, "titulo"):
            break

    # ── Nombre del archivo de video ────────────────────────
    # Variable tipo str: nombre del archivo de video
    nombre_video: str = ""
    while True:
        nombre_video = input("  Nombre del video: ").strip()
        if validar_captura(nombre_video, "nombre_vid"):
            break

    # ── Extensión del video ────────────────────────────────
    # Variable tipo str: extensión del archivo (.mpg, .mov, etc.)
    extension: str = ""
    while True:
        extension = input("  Extensión del video (.mpg, .mov, etc.): ").strip()
        if validar_captura(extension, "extension"):
            break

    # ── Tamaño del video ───────────────────────────────────
    # Variable tipo float: tamaño en MB, máximo 3
    tamano: float = 0.0
    while True:
        tamano_str = input("  Tamaño en MB (máx. 3): ").strip()
        if validar_captura(tamano_str, "tamano"):
            tamano = float(tamano_str)  # Convertir a número decimal
            break

    # Retornar los datos del video como diccionario
    return {
        "titulo":       titulo,
        "nombre_video": nombre_video,
        "extension":    extension,
        "tamano":       tamano
    }


# =============================================================
# FUNCIÓN: guardar_en_archivo
# Guarda toda la información validada en salida.txt
# con el formato requerido separado por pipes ( | )
# =============================================================
def guardar_en_archivo(id_nomina, nombre, cantidad, lista_videos):
    """
    Escribe una línea en salida.txt con el formato:
    Nómina | Nombre | Cantidad | Título1 | Nombre1 | Ext1 | Tam1 | ...
    Maneja al menos 2 excepciones (IOError y PermissionError).
    """

    try:
        # Construir la línea de datos comenzando con info del usuario
        linea = f"{id_nomina} | {nombre} | {cantidad}"

        # Agregar la información de cada video a la línea
        for video in lista_videos:
            linea += (
                f" | {video['titulo']}"
                f" | {video['nombre_video']}"
                f" | {video['extension']}"
                f" | {video['tamano']}"
            )

        # Abrir (o crear) el archivo salida.txt en modo append
        # 'a' → agrega al final sin borrar contenido previo
        # encoding='utf-8' → soporta caracteres especiales en español
        with open("salida.txt", "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")  # Escribir la línea con salto de línea

        print(f"\n✅ Información guardada correctamente en 'salida.txt'.")

    except PermissionError:
        # Excepción 1: No hay permisos para escribir en el archivo
        print("\n❌ Error: No tienes permisos para escribir en 'salida.txt'.")
        print("   Intenta ejecutar el programa con permisos de administrador.")

    except IOError as e:
        # Excepción 2: Error de entrada/salida (disco lleno, archivo bloqueado, etc.)
        manejar_excepcion(e, "escritura del archivo salida.txt")


# =============================================================
# FUNCIÓN PRINCIPAL: main
# Controla el flujo completo del programa.
# =============================================================
def main():
    """
    Función principal que orquesta todo el sistema.
    Maneja el ciclo de vida: captura → confirmación → guardado.
    """

    try:
        # Variable de control del ciclo principal
        continuar = True

        while continuar:

            # ── Paso 1: Pedir datos del usuario ───────────────
            id_nomina, nombre, cantidad = pedir_datos_usuario()

            # ── Paso 2: Mostrar resumen y pedir confirmación ──
            print(f"""
╔══════════════════════════════════════════════════════╗
  Bienvenido {nombre},
  tu número de nómina es {id_nomina}
  y estás intentando subir {cantidad} video(s).
  ¿Es correcta la información? (Sí/No)
╚══════════════════════════════════════════════════════╝""")

            respuesta = input("Tu respuesta: ").strip().lower()

            # ── Caso A: El usuario confirmó con "Sí" ──────────
            if respuesta in ("sí", "si", "s"):

                # Paso 3: Capturar info de cada video con ciclo FOR
                lista_videos = []

                for i in range(1, cantidad + 1):
                    # Llamar a la función para capturar datos del video #i
                    video = capturar_info_video(i)
                    lista_videos.append(video)  # Agregar a la lista

                # Paso 4: Guardar toda la información en salida.txt
                guardar_en_archivo(id_nomina, nombre, cantidad, lista_videos)

                # Mostrar resumen final de lo registrado
                print("\n📋 Resumen de videos registrados:")
                for i, v in enumerate(lista_videos, start=1):
                    print(f"   #{i}: {v['titulo']} | {v['nombre_video']} | "
                          f"{v['extension']} | {v['tamano']} MB")

                continuar = False  # Finalizar el ciclo principal

            # ── Caso B: El usuario contestó "No" ──────────────
            else:
                print("\n¿Deseas salir del sistema? (Sí/No)")
                salir = input("Tu respuesta: ").strip().lower()

                if salir in ("sí", "si", "s"):
                    # Mostrar mensaje de despedida y terminar
                    print("\nMuchas gracias por haber usado nuestro sistema, hasta pronto.")
                    continuar = False
                else:
                    # Volver al inicio y pedir datos nuevamente
                    print("\nVolviendo al inicio del sistema...\n")
                    continuar = True  # El ciclo while continúa

    except KeyboardInterrupt:
        # Excepción por si el usuario presiona Ctrl+C
        print("\n\n⚠  Proceso interrumpido. Hasta pronto.")


# =============================================================
# Punto de entrada del script
# =============================================================
if __name__ == "__main__":
    main()
