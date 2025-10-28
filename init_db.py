#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialización de la base de datos.
Ejecutar una vez antes de iniciar la aplicación por primera vez.
"""

from database import init_database

if __name__ == '__main__':
    print("🔧 Inicializando base de datos...")
    init_database()
    print("\n✅ Base de datos lista!")
    print("   Ahora puedes ejecutar: python3 web_app.py")
