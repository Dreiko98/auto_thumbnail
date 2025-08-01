#!/usr/bin/env python3
"""
Iniciador rápido para Thumbnail Generator Web App
===============================================

Inicia la aplicación web con configuración optimizada.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Verifica e instala dependencias necesarias."""
    print("🔍 Verificando dependencias...")
    
    required_packages = ['flask', 'werkzeug', 'PIL', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Instalando dependencias faltantes...")
        try:
            # Instalar desde requirements.txt
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias")
            print("💡 Intenta ejecutar manualmente: pip install -r requirements.txt")
            return False
    
    return True

def start_web_app():
    """Inicia la aplicación web."""
    try:
        from web_app import run_app
        print("\n🚀 INICIANDO THUMBNAIL GENERATOR WEB APP")
        print("═" * 50)
        run_app(debug=False, port=5000)
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Asegúrate de que todos los archivos estén en el mismo directorio")
        return False
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal."""
    print("🎨 THUMBNAIL GENERATOR - INICIADOR WEB")
    print("═" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ No se puede iniciar sin las dependencias necesarias")
        input("Presiona Enter para salir...")
        return False
    
    # Iniciar aplicación web
    return start_web_app()

if __name__ == '__main__':
    success = main()
    if not success:
        input("\n📝 Presiona Enter para salir...")
        sys.exit(1)
