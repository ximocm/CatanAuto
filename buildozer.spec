[app]

# Nombre principal del archivo (sin .py)
source.main = main
source.dir = .
version = 0.1


# Título de la app
title = CatanAutoRoller

# Nombre interno del paquete (sin espacios ni mayúsculas)
package.name = cautor

# Dominio inverso (puede ser ficticio)
package.domain = org.cautor

# Requisitos de Python para compilar
requirements = python3, pygame

# Archivos que se incluirán en el APK
source.include_exts = py,png,wav,ico
include_patterns = dice.png,icon.ico,info.png,moon.png,pause.png,ping.wav,sun.png

# Icono opcional
icon.filename = icon.ico

# Orientación de la pantalla: portrait | landscape | all
orientation = portrait

# Versión del archivo de Python (usa 3 para python3.x)
android.python = 3

# SDK mínimo requerido (generalmente 21 es suficiente)
android.minapi = 21

# Modo de empaquetado: 'dir' para desarrollo, 'monolithic' para producción
android.packaging = monolithic

# Archivos que se excluirán del APK
exclude_patterns = *.md, *.pyc

# No usar la consola de Android (evita pantalla negra al iniciar)
android.disable_android_log = 1

# Si quieres firmar el APK con una key personalizada, configura esto:
# android.release_key.alias = mykey
# android.release_key.storepassword = your_password
# android.release_key.aliaspassword = your_password

[buildozer]

# Directorio donde se colocará el APK generado
build_dir = .buildozer

# Directorio de salida
bin_dir = bin

# Log level (1: silencioso, 2: normal, 3: verbose)
log_level = 2
