#!/usr/bin/env python3
"""
EJEMPLO DE USO - Generador de Thumbnails
========================================

Este archivo muestra diferentes formas de usar el generador de thumbnails.
"""

from generate_thumbnail import generar_thumbnail

# Ejemplo 1: Thumbnail con imagen local y iconos locales
def ejemplo_local():
    """Ejemplo usando archivos locales"""
    imagen_base = "fondo_ejemplo.jpg"  # Pon aquí tu imagen
    titulo = "Tutorial de Python para Principiantes"
    iconos = [
        "icono_python.png",
        "icono_tutorial.png"
    ]
    
    generar_thumbnail(imagen_base, titulo, iconos, "ejemplo_local")


# Ejemplo 2: Thumbnail con recursos en línea
def ejemplo_online():
    """Ejemplo usando recursos de internet"""
    imagen_base = "https://picsum.photos/1920/1080"
    titulo = "Desarrollo Web con Python"
    iconos = [
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"
    ]
    
    generar_thumbnail(imagen_base, titulo, iconos, "ejemplo_web")


# Ejemplo 3: Solo texto (sin iconos)
def ejemplo_solo_texto():
    """Ejemplo con solo texto, sin iconos"""
    imagen_base = "https://source.unsplash.com/1920x1080/technology"
    titulo = "Mi Blog de Tecnología"
    iconos = []  # Sin iconos
    
    generar_thumbnail(imagen_base, titulo, iconos, "ejemplo_blog")


if __name__ == "__main__":
    print("🚀 Ejecutando ejemplos de thumbnails...")
    print()
    
    # Descomenta el ejemplo que quieras probar:
    
    # ejemplo_local()
    ejemplo_online()
    # ejemplo_solo_texto()
    
    print("✅ Ejemplos completados!")
