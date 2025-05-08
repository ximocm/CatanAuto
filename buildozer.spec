[app]

# Nombre visible de la app
title = CatanAutoRoller

# Identificador de paquete (único)
package.name = CatanAutoRoller
package.domain = org.ximocm

# Carpeta raíz del código fuente
source.dir = .

# Archivos a incluir
source.include_exts = py,png,jpg,kv,atlas,wav,txt

# Versión de la app (visible)
version = 1.3

# Requisitos de Python y librerías
requirements = python3==3.10.12,kivy==2.3.0,pyjnius==1.5.0,hostpython3==3.10.12,pygame

# Splash screen personalizada
presplash.filename = %(source.dir)s/assets/splash.png

# Icono personalizado
icon.filename = %(source.dir)s/assets/icon.png

# Orientación y pantalla
orientation = portrait
fullscreen = 1

# Arquitecturas soportadas
android.archs = arm64-v8a, armeabi-v7a

# Backup permitido
android.allow_backup = True
