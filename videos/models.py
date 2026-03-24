"""
Modelos de la base de datos Pro_Gol
Tablas: TBL_Usuario, TBL_Video, TBL_UsuarioVideo
"""

from django.db import models


# ─────────────────────────────────────────────────────────────
# TABLA: TBL_Usuario
# Guarda los datos del usuario que sube videos
# ─────────────────────────────────────────────────────────────
class TBL_Usuario(models.Model):

    # Campo llave: nómina alfanumérica de 10 caracteres
    id_nomina = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="Número de nómina"
    )

    # Nombre completo del usuario, máximo 50 caracteres
    nombre = models.CharField(
        max_length=50,
        verbose_name="Nombre del usuario"
    )

    class Meta:
        db_table = 'TBL_Usuario'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} ({self.id_nomina})"


# ─────────────────────────────────────────────────────────────
# TABLA: TBL_Video
# Guarda la información de cada video
# ─────────────────────────────────────────────────────────────
class TBL_Video(models.Model):

    # ID autoincremental del video
    id_video = models.AutoField(
        primary_key=True,
        verbose_name="ID del video"
    )

    # Título descriptivo del video, máximo 50 caracteres
    titulo = models.CharField(
        max_length=50,
        verbose_name="Título del video"
    )

    # Nombre del archivo de video, máximo 50 caracteres
    nombre_video = models.CharField(
        max_length=50,
        verbose_name="Nombre del video"
    )

    # Extensión del archivo (.mpg, .mov, etc.), máximo 5 caracteres
    extension = models.CharField(
        max_length=5,
        verbose_name="Extensión del video"
    )

    # Tamaño del video en MB, máximo 3
    tamano = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Tamaño (MB)"
    )

    class Meta:
        db_table = 'TBL_Video'
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return f"{self.titulo} ({self.extension}) - {self.tamano} MB"


# ─────────────────────────────────────────────────────────────
# TABLA: TBL_UsuarioVideo
# Relaciona usuarios con sus videos
# ─────────────────────────────────────────────────────────────
class TBL_UsuarioVideo(models.Model):

    # Llave foránea al usuario
    usuario = models.ForeignKey(
        TBL_Usuario,
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )

    # Llave foránea al video
    video = models.ForeignKey(
        TBL_Video,
        on_delete=models.CASCADE,
        verbose_name="Video"
    )

    class Meta:
        db_table = 'TBL_UsuarioVideo'
        verbose_name = "Relación Usuario-Video"
        verbose_name_plural = "Relaciones Usuario-Video"

    def __str__(self):
        return f"{self.usuario} → {self.video}"
