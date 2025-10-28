#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interfaz Web para Generador de Thumbnails
==========================================

Aplicación Flask que proporciona una interfaz web moderna para generar thumbnails.
Compatible con empaquetado como aplicación de escritorio.

Autor: Desarrollador Senior Python
Fecha: Agosto 2025
"""

import os
import base64
import tempfile
import uuid
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
from generate_thumbnail import generar_thumbnail
from database import init_database, create_user, authenticate_user, get_user_by_id, update_openai_token, get_openai_token
from ai_generator import generate_background_image, generate_icon_image, test_openai_token, save_generated_image
import webbrowser
import threading
import time
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thumbnail_generator_2025_secure_key_change_in_production'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB máximo

# Directorio temporal para archivos subidos - usar carpetas del proyecto, no /tmp
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(SCRIPT_DIR, '.uploads')
RESULTS_FOLDER = os.path.join(SCRIPT_DIR, '.results')

# Crear carpetas si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

print(f"📁 Carpeta de uploads: {UPLOAD_FOLDER}")
print(f"📁 Carpeta de resultados: {RESULTS_FOLDER}")

# Inicializar base de datos
init_database()

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}

def login_required(f):
    """Decorador para rutas que requieren autenticación."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Debes iniciar sesión', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    """Limpia archivos temporales antiguos."""
    try:
        current_time = time.time()
        for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        # Eliminar archivos más antiguos de 1 hora
                        file_age = current_time - os.path.getctime(file_path)
                        if file_age > 3600:  # 1 hora
                            try:
                                os.remove(file_path)
                                print(f"🗑️  Archivo antiguo eliminado: {filename}")
                            except OSError as e:
                                print(f"⚠️  No se pudo eliminar {filename}: {e}")
    except Exception as e:
        print(f"⚠️  Error limpiando archivos temporales: {e}")


def cleanup_all_temp_files():
    """Limpia TODOS los archivos temporales al iniciar el servidor."""
    try:
        for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        try:
                            os.remove(file_path)
                            print(f"🗑️  Archivo temporal eliminado: {filename}")
                        except OSError as e:
                            print(f"⚠️  No se pudo eliminar {filename}: {e}")
        print("✅ Limpieza completa de archivos temporales al iniciar")
    except Exception as e:
        print(f"⚠️  Error en limpieza inicial: {e}")

@app.route('/')
def index():
    """Página principal de la aplicación."""
    # No limpiar archivos en cada carga - hacerlo solo en shutdown
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Maneja la subida de archivos (imagen de fondo, iconos y foto de persona)."""
    try:
        response = {'success': False, 'message': '', 'files': {'icons': []}}
        
        # Procesar imagen de fondo
        if 'background_image' in request.files:
            file = request.files['background_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                response['files']['background'] = unique_filename
                print(f"✅ Imagen de fondo guardada: {unique_filename}")
        
        # Procesar iconos
        icons = []
        for key in request.files:
            if key.startswith('icon_'):
                file = request.files[key]
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(file_path)
                    icons.append(unique_filename)
                    print(f"✅ Icono guardado: {unique_filename}")
        
        # Siempre incluir icons en la respuesta (vacío si no hay)
        response['files']['icons'] = icons
        
        # Procesar foto de persona (para plantilla 2)
        if 'person_photo' in request.files:
            file = request.files['person_photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                response['files']['person_photo'] = unique_filename
                print(f"✅ Foto de persona guardada: {unique_filename}")
        
        # Procesar icono 1 de plantilla 3
        if 'icon1_template3' in request.files:
            file = request.files['icon1_template3']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                response['files']['icon1_template3'] = unique_filename
                print(f"✅ Icono 1 (plantilla 3) guardado: {unique_filename}")
        
        # Procesar icono 2 de plantilla 3
        if 'icon2_template3' in request.files:
            file = request.files['icon2_template3']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                response['files']['icon2_template3'] = unique_filename
                print(f"✅ Icono 2 (plantilla 3) guardado: {unique_filename}")
        
        response['success'] = True
        response['message'] = f"Archivos subidos correctamente. Fondo: {'✅' if 'background' in response['files'] else '❌'}, Iconos: {len(icons)}"
        
        print(f"📤 Respuesta /upload: success={response['success']}, background={'✅' if 'background' in response['files'] else '❌'}, icons={len(icons)}, person_photo={'✅' if 'person_photo' in response['files'] else '❌'}, icon1_t3={'✅' if 'icon1_template3' in response['files'] else '❌'}, icon2_t3={'✅' if 'icon2_template3' in response['files'] else '❌'}")
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/generate', methods=['POST'])
def generate_thumbnail():
    """Genera el thumbnail con los parámetros especificados."""
    try:
        data = request.get_json()
        
        # Obtener tipo de plantilla (por defecto: plantilla 1)
        template_type = data.get('template_type', 1)
        print(f"🎨 Tipo de plantilla seleccionada: {template_type}")
        
        # Validar imagen de fondo (común para todas las plantillas)
        if not data.get('background_file'):
            return jsonify({'success': False, 'message': 'La imagen de fondo es obligatoria'})
        
        # Preparar ruta de imagen de fondo
        background_file = data.get('background_file')
        print(f"📥 background_file recibido: {background_file}")
        background_path = os.path.join(app.config['UPLOAD_FOLDER'], background_file)
        print(f"   📂 Ruta construida: {background_path}")
        print(f"   ✓ Existe: {os.path.exists(background_path)}")
        
        if not os.path.exists(background_path):
            print(f"   ❌ ARCHIVO NO ENCONTRADO!")
            return jsonify({'success': False, 'message': 'Imagen de fondo no encontrada'})
        
        # Generar nombre único para el resultado
        result_id = uuid.uuid4().hex
        result_name = f"thumbnail_{result_id}"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_name)
        
        # Procesar según el tipo de plantilla
        if template_type == 1:
            # Plantilla 1: Título + Iconos
            if not data.get('title'):
                return jsonify({'success': False, 'message': 'El título es obligatorio'})
            
            # Preparar iconos
            icon_paths = []
            icon_files = data.get('icon_files', [])
            print(f"📥 icon_files recibido: {icon_files}")
            
            if icon_files and isinstance(icon_files, list) and len(icon_files) > 0:
                for icon_file in icon_files:
                    icon_path = os.path.join(app.config['UPLOAD_FOLDER'], icon_file)
                    if os.path.exists(icon_path):
                        icon_paths.append(icon_path)
                        print(f"   ✅ Icono encontrado: {icon_file}")
            
            print(f"🎨 Generando thumbnail plantilla 1:")
            print(f"   📸 Fondo: {background_path}")
            print(f"   📝 Título: {data['title']}")
            print(f"   🎯 Iconos: {len(icon_paths)}")
            
            generar_thumbnail(
                imagen_base=background_path,
                titulo=data['title'],
                iconos=icon_paths,
                ruta_salida=result_path,
                tipo_plantilla=template_type
            )
            
        elif template_type == 2:
            # Plantilla 2: Texto1 + Texto2 + Foto de persona
            if not data.get('text1') or not data.get('text2'):
                return jsonify({'success': False, 'message': 'Los textos 1 y 2 son obligatorios'})
            
            if not data.get('person_photo_file'):
                return jsonify({'success': False, 'message': 'La foto de persona es obligatoria'})
            
            # Preparar ruta de foto de persona
            person_photo_file = data.get('person_photo_file')
            person_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], person_photo_file)
            
            if not os.path.exists(person_photo_path):
                return jsonify({'success': False, 'message': 'Foto de persona no encontrada'})
            
            print(f"🎨 Generando thumbnail plantilla 2:")
            print(f"   📸 Fondo: {background_path}")
            print(f"   📝 Texto 1: {data['text1']}")
            print(f"   📝 Texto 2: {data['text2']}")
            print(f"   � Foto: {person_photo_path}")
            
            generar_thumbnail(
                imagen_base=background_path,
                titulo="",  # No se usa en plantilla 2
                iconos=[],  # No se usa en plantilla 2
                ruta_salida=result_path,
                tipo_plantilla=template_type,
                texto1=data['text1'],
                texto2=data['text2'],
                foto_persona=person_photo_path
            )
            
        elif template_type == 3:
            # Plantilla 3: Texto + 2 iconos en esquinas
            if not data.get('text'):
                return jsonify({'success': False, 'message': 'El texto es obligatorio'})
            
            if not data.get('icon1_file') or not data.get('icon2_file'):
                return jsonify({'success': False, 'message': 'Los 2 iconos son obligatorios'})
            
            # Preparar rutas de iconos
            icon1_file = data.get('icon1_file')
            icon1_path = os.path.join(app.config['UPLOAD_FOLDER'], icon1_file)
            
            icon2_file = data.get('icon2_file')
            icon2_path = os.path.join(app.config['UPLOAD_FOLDER'], icon2_file)
            
            if not os.path.exists(icon1_path):
                return jsonify({'success': False, 'message': 'Icono 1 no encontrado'})
            
            if not os.path.exists(icon2_path):
                return jsonify({'success': False, 'message': 'Icono 2 no encontrado'})
            
            # Obtener formato (Instagram o normal)
            is_instagram = data.get('is_instagram', False)
            
            print(f"🎨 Generando thumbnail plantilla 3:")
            print(f"   📸 Fondo: {background_path}")
            print(f"   📝 Texto: {data['text']}")
            print(f"   🎯 Icono 1: {icon1_path}")
            print(f"   🎯 Icono 2: {icon2_path}")
            if is_instagram:
                print(f"   📱 Formato: Instagram Post (1080x1080)")
            
            generar_thumbnail(
                imagen_base=background_path,
                titulo="",  # No se usa en plantilla 3
                iconos=[],  # No se usa en plantilla 3
                ruta_salida=result_path,
                tipo_plantilla=template_type,
                texto_plantilla3=data['text'],
                icono1_plantilla3=icon1_path,
                icono2_plantilla3=icon2_path,
                is_instagram_plantilla3=is_instagram
            )
            
        else:
            return jsonify({'success': False, 'message': f'Tipo de plantilla no soportado: {template_type}'})
        
        # Verificar que se generó correctamente
        png_path = f"{result_path}.png"
        if os.path.exists(png_path):
            # Convertir imagen a base64 para preview
            with open(png_path, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Limpiar archivos temporales inmediatamente
            try:
                # Eliminar imagen de fondo subida
                if os.path.exists(background_path):
                    os.remove(background_path)
                    print(f"🗑️  Eliminado: {background_path}")
                
                # Eliminar iconos subidos
                for icon_path in icon_paths:
                    if os.path.exists(icon_path):
                        os.remove(icon_path)
                        print(f"🗑️  Eliminado: {icon_path}")
                
                # Eliminar foto de persona (plantilla 2)
                if template_type == 2 and person_photo_path and os.path.exists(person_photo_path):
                    os.remove(person_photo_path)
                    print(f"🗑️  Eliminado: {person_photo_path}")
                
                # Eliminar iconos plantilla 3
                if template_type == 3:
                    if icon1_path and os.path.exists(icon1_path):
                        os.remove(icon1_path)
                        print(f"🗑️  Eliminado: {icon1_path}")
                    if icon2_path and os.path.exists(icon2_path):
                        os.remove(icon2_path)
                        print(f"🗑️  Eliminado: {icon2_path}")
                
                # Eliminar thumbnail generado
                if os.path.exists(png_path):
                    os.remove(png_path)
                    print(f"🗑️  Eliminado: {png_path}")
                
                print("✅ Limpieza automática de archivos temporales completada")
            except Exception as cleanup_error:
                print(f"⚠️  Error en limpieza automática: {cleanup_error}")
            
            return jsonify({
                'success': True,
                'message': '🎉 Thumbnail generado exitosamente',
                'result_id': result_id,
                'preview': f"data:image/png;base64,{img_base64}"
            })
        else:
            return jsonify({'success': False, 'message': 'Error al generar el thumbnail'})
            
    except Exception as e:
        print(f"❌ Error generando thumbnail: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'})

@app.route('/download/<result_id>')
def download_thumbnail(result_id):
    """Descarga el thumbnail generado."""
    try:
        png_path = os.path.join(app.config['RESULTS_FOLDER'], f"thumbnail_{result_id}.png")
        if os.path.exists(png_path):
            return send_file(
                png_path,
                as_attachment=True,
                download_name=f"thumbnail_{result_id}.png",
                mimetype='image/png'
            )
        else:
            return "Archivo no encontrado", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/health')
def health_check():
    """Endpoint para verificar el estado de la aplicación."""
    return jsonify({'status': 'ok', 'message': 'Thumbnail Generator Web App funcionando correctamente'})


# ==========================================
# RUTAS DE AUTENTICACIÓN
# ==========================================

@app.route('/register', methods=['POST'])
def register():
    """Registro de nuevos usuarios."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Validaciones
        if not username or not password:
            return jsonify({'success': False, 'message': 'Usuario y contraseña son obligatorios'})
        
        if len(username) < 3:
            return jsonify({'success': False, 'message': 'El usuario debe tener al menos 3 caracteres'})
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 6 caracteres'})
        
        # Crear usuario
        user = create_user(username, password)
        
        if user:
            # Iniciar sesión automáticamente
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            return jsonify({
                'success': True,
                'message': f'¡Bienvenido {username}! Tu cuenta ha sido creada exitosamente',
                'user': {
                    'id': user['id'],
                    'username': user['username']
                }
            })
        else:
            return jsonify({'success': False, 'message': 'El nombre de usuario ya está en uso'})
            
    except Exception as e:
        print(f"❌ Error en registro: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al crear usuario'})


@app.route('/login', methods=['POST'])
def login():
    """Inicio de sesión de usuarios."""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Usuario y contraseña son obligatorios'})
        
        # Autenticar usuario
        user = authenticate_user(username, password)
        
        if user:
            # Crear sesión
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['has_openai_token'] = user['has_openai_token']
            
            return jsonify({
                'success': True,
                'message': f'¡Bienvenido de nuevo, {username}!',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'has_openai_token': user['has_openai_token']
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'})
            
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al iniciar sesión'})


@app.route('/logout', methods=['POST'])
def logout():
    """Cierre de sesión."""
    session.clear()
    return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'})


@app.route('/session', methods=['GET'])
def get_session():
    """Obtiene información de la sesión actual."""
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        if user:
            return jsonify({
                'logged_in': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'has_openai_token': user['has_openai_token']
                }
            })
    
    return jsonify({'logged_in': False})


@app.route('/update_token', methods=['POST'])
@login_required
def update_token():
    """Actualiza el token de OpenAI del usuario."""
    try:
        data = request.get_json()
        openai_token = data.get('openai_token', '').strip()
        
        if not openai_token:
            # Eliminar token si está vacío
            openai_token = None
        
        user_id = session['user_id']
        
        if update_openai_token(user_id, openai_token):
            session['has_openai_token'] = openai_token is not None
            
            message = 'Token de OpenAI actualizado' if openai_token else 'Token de OpenAI eliminado'
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': 'Error al actualizar token'})
            
    except Exception as e:
        print(f"❌ Error al actualizar token: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al actualizar token'})


@app.route('/change_password', methods=['POST'])
@login_required
def change_password_route():
    """Cambia la contraseña del usuario."""
    try:
        from database import change_password
        
        data = request.get_json()
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()
        
        # Validaciones
        if not current_password or not new_password or not confirm_password:
            return jsonify({'success': False, 'message': 'Todos los campos son requeridos'})
        
        if new_password != confirm_password:
            return jsonify({'success': False, 'message': 'Las contraseñas nuevas no coinciden'})
        
        if len(new_password) < 6:
            return jsonify({'success': False, 'message': 'La nueva contraseña debe tener al menos 6 caracteres'})
        
        if new_password == current_password:
            return jsonify({'success': False, 'message': 'La nueva contraseña debe ser diferente a la actual'})
        
        user_id = session['user_id']
        
        if change_password(user_id, current_password, new_password):
            return jsonify({'success': True, 'message': 'Contraseña actualizada correctamente'})
        else:
            return jsonify({'success': False, 'message': 'Contraseña actual incorrecta'})
            
    except Exception as e:
        print(f"❌ Error al cambiar contraseña: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al cambiar contraseña'})


# ==========================================
# RUTAS DE GENERACIÓN CON IA
# ==========================================

@app.route('/generate_ai_background', methods=['POST'])
@login_required
def generate_ai_background():
    """Genera una imagen de fondo usando IA."""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        
        if not description:
            return jsonify({'success': False, 'message': 'La descripción es obligatoria'})
        
        # Obtener token de OpenAI del usuario
        user_id = session['user_id']
        api_key = get_openai_token(user_id)
        
        if not api_key:
            return jsonify({
                'success': False, 
                'message': 'Necesitas configurar tu token de OpenAI primero',
                'require_token': True
            })
        
        print(f"\n🎨 Generando fondo con IA para usuario {session['username']}")
        print(f"   📝 Descripción: {description}")
        
        # Generar imagen
        image = generate_background_image(description, api_key)
        
        if image:
            # Guardar imagen en uploads
            filename = f"{uuid.uuid4().hex}_ai_background.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            if save_generated_image(image, filepath):
                # Convertir a base64 para preview
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                return jsonify({
                    'success': True,
                    'message': '¡Imagen de fondo generada con éxito!',
                    'filename': filename,
                    'preview': f'data:image/png;base64,{img_base64}'
                })
            else:
                return jsonify({'success': False, 'message': 'Error al guardar la imagen generada'})
        else:
            return jsonify({'success': False, 'message': 'No se pudo generar la imagen. Verifica tu token de OpenAI.'})
            
    except Exception as e:
        print(f"❌ Error al generar fondo con IA: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/generate_ai_icon', methods=['POST'])
@login_required
def generate_ai_icon():
    """Genera un icono usando IA."""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        icon_number = data.get('icon_number', 1)
        
        if not description:
            return jsonify({'success': False, 'message': 'La descripción es obligatoria'})
        
        # Obtener token de OpenAI del usuario
        user_id = session['user_id']
        api_key = get_openai_token(user_id)
        
        if not api_key:
            return jsonify({
                'success': False, 
                'message': 'Necesitas configurar tu token de OpenAI primero',
                'require_token': True
            })
        
        print(f"\n🎯 Generando icono #{icon_number} con IA para usuario {session['username']}")
        print(f"   📝 Descripción: {description}")
        
        # Generar icono
        image = generate_icon_image(description, api_key, icon_number)
        
        if image:
            # Guardar imagen en uploads
            filename = f"{uuid.uuid4().hex}_ai_icon{icon_number}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            if save_generated_image(image, filepath):
                # Convertir a base64 para preview
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                return jsonify({
                    'success': True,
                    'message': f'¡Icono #{icon_number} generado con éxito!',
                    'filename': filename,
                    'preview': f'data:image/png;base64,{img_base64}',
                    'icon_number': icon_number
                })
            else:
                return jsonify({'success': False, 'message': 'Error al guardar la imagen generada'})
        else:
            return jsonify({'success': False, 'message': 'No se pudo generar el icono. Verifica tu token de OpenAI.'})
            
    except Exception as e:
        print(f"❌ Error al generar icono con IA: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


def open_browser():
    """Abre el navegador automáticamente tras iniciar el servidor."""
    time.sleep(1.5)  # Esperar a que el servidor esté listo
    webbrowser.open('http://localhost:5000')

def run_app(debug=False, port=5000):
    """Ejecuta la aplicación Flask."""
    print("\n🚀 INICIANDO THUMBNAIL GENERATOR WEB APP")
    print("═" * 60)
    print(f"📱 Interfaz web disponible en: http://localhost:{port}")
    print("🔧 Presiona Ctrl+C para detener el servidor")
    print("═" * 60)
    
    # Limpiar archivos temporales al iniciar
    print("\n🧹 Limpiando archivos temporales...")
    cleanup_all_temp_files()
    
    # Abrir navegador automáticamente en modo producción
    if not debug:
        threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=False  # Evitar doble inicio en modo debug
        )
    except KeyboardInterrupt:
        print("\n👋 Cerrando aplicación...")
    finally:
        print("\n🧹 Limpieza final de archivos temporales...")
        cleanup_all_temp_files()

if __name__ == '__main__':
    import sys
    
    # Argumentos de línea de comandos
    debug_mode = '--debug' in sys.argv
    port = 5000
    
    if '--port' in sys.argv:
        try:
            port_index = sys.argv.index('--port') + 1
            port = int(sys.argv[port_index])
        except (IndexError, ValueError):
            print("⚠️  Puerto inválido, usando 5000 por defecto")
    
    run_app(debug=debug_mode, port=port)
