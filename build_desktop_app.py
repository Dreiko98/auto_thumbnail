#!/usr/bin/env python3
"""
Script para empaquetar la aplicación web como aplicación de escritorio
====================================================================

Este script usa PyInstaller para crear un ejecutable independiente
que incluya el servidor Flask y abra automáticamente en el navegador.
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def check_dependencies():
    """Verifica que PyInstaller esté instalado."""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no encontrado")
        print("💡 Instalando PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=5.10.0"], check=True)
            print("✅ PyInstaller instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando PyInstaller")
            return False

def create_desktop_launcher():
    """Crea un script launcher que configura el entorno de escritorio."""
    launcher_content = '''#!/usr/bin/env python3
"""
Launcher para Thumbnail Generator - App de Escritorio
====================================================

Este script inicia la aplicación web y la abre en el navegador
como si fuera una aplicación de escritorio nativa.
"""

import sys
import os
import webbrowser
import threading
import time
import tkinter as tk
from tkinter import messagebox

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def show_startup_message():
    """Muestra una ventana de inicio mientras se carga la app."""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Ventana de splash
    splash = tk.Toplevel()
    splash.title("🎨 Thumbnail Generator")
    splash.geometry("400x200")
    splash.resizable(False, False)
    
    # Centrar ventana
    splash.transient(root)
    splash.grab_set()
    
    # Contenido
    frame = tk.Frame(splash, bg='white', padx=30, pady=30)
    frame.pack(fill='both', expand=True)
    
    title_label = tk.Label(frame, text="🎨 Thumbnail Generator", 
                          font=('Arial', 16, 'bold'), bg='white', fg='#2563eb')
    title_label.pack(pady=(0, 10))
    
    status_label = tk.Label(frame, text="🚀 Iniciando aplicación...", 
                           font=('Arial', 11), bg='white', fg='#64748b')
    status_label.pack(pady=(0, 10))
    
    progress_label = tk.Label(frame, text="⏳ Esto tomará unos segundos", 
                             font=('Arial', 9), bg='white', fg='#64748b')
    progress_label.pack()
    
    def update_status():
        for i, message in enumerate([
            "🔧 Preparando servidor...",
            "🌐 Iniciando interfaz web...",
            "🖥️ Abriendo navegador...",
            "✅ ¡Listo! La aplicación se abrirá en breve"
        ]):
            status_label.config(text=message)
            splash.update()
            time.sleep(1)
        
        time.sleep(1)
        splash.destroy()
        root.quit()
    
    # Ejecutar actualización en hilo separado
    threading.Thread(target=update_status, daemon=True).start()
    
    root.mainloop()

def open_browser_when_ready(port=5000):
    """Abre el navegador cuando el servidor esté listo."""
    time.sleep(3)  # Dar tiempo al servidor
    webbrowser.open(f'http://localhost:{port}')

def main():
    """Función principal del launcher."""
    try:
        # Mostrar mensaje de inicio
        threading.Thread(target=show_startup_message, daemon=True).start()
        time.sleep(0.5)  # Dar tiempo a que aparezca la ventana
        
        # Importar y ejecutar la app web
        from web_app import run_app
        
        # Abrir navegador después de un delay
        threading.Thread(target=open_browser_when_ready, daemon=True).start()
        
        # Iniciar aplicación web
        print("🚀 Iniciando Thumbnail Generator como aplicación de escritorio...")
        run_app(debug=False, port=5000)
        
    except KeyboardInterrupt:
        print("\\n👋 Cerrando aplicación...")
    except Exception as e:
        # Mostrar error en ventana gráfica
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Error en Thumbnail Generator",
                f"Error al iniciar la aplicación:\\n\\n{str(e)}\\n\\nPor favor contacta al desarrollador."
            )
            root.destroy()
        except:
            print(f"❌ Error crítico: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
    
    with open('desktop_launcher.py', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Launcher de escritorio creado: desktop_launcher.py")

def create_spec_file():
    """Crea el archivo .spec para PyInstaller con configuración optimizada."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Configuración de paths
current_dir = Path.cwd()
templates_dir = current_dir / 'templates'

a = Analysis(
    ['desktop_launcher.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
        (str(templates_dir), 'templates'),
        ('*.py', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'flask',
        'werkzeug',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw', 
        'PIL.ImageFont',
        'PIL.ImageFilter',
        'requests',
        'tkinter',
        'tkinter.messagebox',
        'webbrowser',
        'threading',
        'tempfile',
        'uuid',
        'base64',
        'io',
        'os',
        'sys',
        'time'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'test',
        'tests',
        'testing',
        'pytest',
        'unittest',
        'doctest'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ThumbnailGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Aquí puedes agregar un icono si tienes uno
)
'''
    
    with open('thumbnail_generator.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado: thumbnail_generator.spec")

def build_executable():
    """Construye el ejecutable usando PyInstaller."""
    print("🔨 Construyendo ejecutable...")
    print("⏳ Esto puede tomar varios minutos...")
    
    try:
        # Usar el archivo .spec para mayor control
        cmd = [
            'pyinstaller',
            '--clean',
            '--noconfirm',
            'thumbnail_generator.spec'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable creado exitosamente!")
            
            # Mostrar ubicación del ejecutable
            system = platform.system().lower()
            if system == 'windows':
                exe_path = 'dist/ThumbnailGenerator.exe'
            else:
                exe_path = 'dist/ThumbnailGenerator'
            
            if os.path.exists(exe_path):
                abs_path = os.path.abspath(exe_path)
                print(f"📍 Ubicación: {abs_path}")
                print(f"💡 Tamaño: {get_file_size(abs_path)}")
                
                # Crear acceso directo en el escritorio (opcional)
                create_desktop_shortcut(abs_path)
                
            return True
        else:
            print("❌ Error construyendo ejecutable:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ PyInstaller no encontrado en PATH")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def get_file_size(file_path):
    """Obtiene el tamaño del archivo en formato legible."""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def create_desktop_shortcut(exe_path):
    """Crea un acceso directo en el escritorio (Linux/Windows)."""
    try:
        system = platform.system().lower()
        
        if system == 'linux':
            # Crear .desktop file
            desktop_path = os.path.expanduser('~/Desktop/ThumbnailGenerator.desktop')
            desktop_content = f'''[Desktop Entry]
Name=Thumbnail Generator
Comment=Generador de thumbnails profesionales
Exec={exe_path}
Icon=applications-graphics
Terminal=false
Type=Application
Categories=Graphics;Photography;
'''
            with open(desktop_path, 'w') as f:
                f.write(desktop_content)
            
            # Hacer ejecutable
            os.chmod(desktop_path, 0o755)
            print(f"🖥️ Acceso directo creado: {desktop_path}")
            
        elif system == 'windows':
            # En Windows usaríamos win32com, pero por simplicidad solo mostramos la ruta
            print(f"💡 Para crear acceso directo en Windows:")
            print(f"   Clic derecho en el escritorio > Nuevo > Acceso directo")
            print(f"   Ruta: {exe_path}")
            
    except Exception as e:
        print(f"⚠️ No se pudo crear acceso directo: {e}")

def cleanup_build_files():
    """Limpia archivos temporales de construcción."""
    print("🧹 Limpiando archivos temporales...")
    
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['desktop_launcher.py', 'thumbnail_generator.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   🗑️ Eliminado: {dir_name}/")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"   🗑️ Eliminado: {file_name}")

def main():
    """Función principal del script de empaquetado."""
    print("📦 EMPAQUETADOR DE THUMBNAIL GENERATOR")
    print("═" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ No se puede continuar sin PyInstaller")
        return False
    
    print()
    
    # Crear archivos necesarios
    print("📝 Creando archivos de configuración...")
    create_desktop_launcher()
    create_spec_file()
    print()
    
    # Construir ejecutable
    success = build_executable()
    print()
    
    # Limpiar archivos temporales
    if success:
        cleanup_build_files()
        print()
        print("🎉 ¡EMPAQUETADO COMPLETADO EXITOSAMENTE!")
        print("═" * 50)
        print("💡 Tu aplicación está lista para distribución")
        print("📁 Busca el ejecutable en la carpeta 'dist/'")
        print("🚀 Puedes ejecutarlo directamente sin instalar Python")
        
        # Instrucciones finales
        system = platform.system().lower()
        if system == 'windows':
            print("\\n🪟 Windows:")
            print("   • Ejecuta: dist/ThumbnailGenerator.exe")
            print("   • Puedes copiar toda la carpeta 'dist/' a otro PC")
        else:
            print("\\n🐧 Linux/macOS:")
            print("   • Ejecuta: ./dist/ThumbnailGenerator")
            print("   • Haz ejecutable si es necesario: chmod +x dist/ThumbnailGenerator")
        
        return True
    else:
        print("❌ EMPAQUETADO FALLIDO")
        print("💡 Revisa los errores anteriores e intenta nuevamente")
        return False

if __name__ == '__main__':
    success = main()
    
    # Pausa para ver resultados
    input("\\n📝 Presiona Enter para continuar...")
    sys.exit(0 if success else 1)
