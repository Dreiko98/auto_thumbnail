#!/usr/bin/env python3
"""
Netlify Function para generar thumbnails
=======================================

Función serverless que usa el motor Python original
con toda la potencia de Pillow y efectos profesionales.
"""

import json
import base64
import io
import os
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from urllib.parse import unquote

def handler(event, context):
    """Handler principal para Netlify Functions."""
    
    # Configurar CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Manejar preflight OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parsear el body
        body = json.loads(event['body'])
        
        # Extraer parámetros
        background_data = body.get('background')
        title = body.get('title', '')
        icons_data = body.get('icons', [])
        
        if not background_data or not title:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Missing background or title'})
            }
        
        # Generar thumbnail
        thumbnail_base64 = generate_thumbnail_serverless(
            background_data, title, icons_data
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'thumbnail': thumbnail_base64
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': f'Internal error: {str(e)}'})
        }


def generate_thumbnail_serverless(background_data, title, icons_data):
    """
    Genera thumbnail usando el motor Python original.
    Adaptado para funcionar en entorno serverless.
    """
    
    # Configuración (misma que config.json)
    CONFIG = {
        'width': 1920,
        'height': 1080,
        'background_blur': 20,
        'font': {
            'size_initial': 158.52,
            'size_minimum': 60.0,
            'size_step': 6.0,
            'max_lines': 2
        },
        'effects': {
            'text': {
                'drop_shadow': {'opacity': 0.85, 'distance': 9, 'spread': 0.24, 'size': 40},
                'inner_shadow': {'opacity': 0.45, 'angle': 30, 'size': 0.08, 'distance': 0}
            },
            'icons': {
                'drop_shadow': {'opacity': 0.85, 'distance': 9, 'spread': 0.24, 'size': 40}
            }
        }
    }
    
    # Crear canvas principal
    canvas = Image.new('RGBA', (CONFIG['width'], CONFIG['height']), (0, 0, 0, 0))
    
    # 1. Procesar imagen de fondo
    background_img = decode_base64_image(background_data)
    background_processed = process_background(background_img, CONFIG)
    canvas.paste(background_processed, (0, 0))
    
    # 2. Añadir texto con efectos
    canvas = add_text_with_effects(canvas, title, CONFIG)
    
    # 3. Añadir iconos si existen
    if icons_data:
        canvas = add_icons_with_effects(canvas, icons_data, CONFIG)
    
    # 4. Convertir a base64 para respuesta
    return encode_image_to_base64(canvas)


def decode_base64_image(base64_data):
    """Decodifica imagen desde base64."""
    # Remover header si existe (data:image/jpeg;base64,)
    if ',' in base64_data:
        base64_data = base64_data.split(',')[1]
    
    image_data = base64.b64decode(base64_data)
    return Image.open(io.BytesIO(image_data)).convert('RGBA')


def process_background(img, config):
    """Procesa la imagen de fondo: redimensiona y desenfoca."""
    # Redimensionar manteniendo proporción
    img_resized = img.resize((config['width'], config['height']), Image.Resampling.LANCZOS)
    
    # Aplicar desenfoque gaussiano
    img_blurred = img_resized.filter(ImageFilter.GaussianBlur(config['background_blur']))
    
    return img_blurred


def add_text_with_effects(canvas, title, config):
    """Añade texto con sombras paralela e interior."""
    draw = ImageDraw.Draw(canvas)
    
    # Configuración de fuente
    font_size = config['font']['size_initial']
    font_min = config['font']['size_minimum']
    font_step = config['font']['size_step']
    max_lines = config['font']['max_lines']
    
    # Buscar tamaño de fuente óptimo
    font = get_font(font_size)
    text_width = canvas.width - 200  # Margen de 100px cada lado
    
    while font_size >= font_min:
        font = get_font(font_size)
        lines = wrap_text(title, font, text_width, draw)
        
        if len(lines) <= max_lines:
            break
        font_size -= font_step
    
    # Calcular posición centrada
    total_height = len(lines) * font_size * 1.2
    start_y = (canvas.height - total_height) / 2
    
    # Dibujar cada línea con efectos
    for i, line in enumerate(lines):
        line_y = start_y + (i * font_size * 1.2)
        
        # Obtener dimensiones del texto
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width_actual = bbox[2] - bbox[0]
        text_x = (canvas.width - text_width_actual) / 2
        
        # 1. Sombra paralela (drop shadow)
        shadow_config = config['effects']['text']['drop_shadow']
        shadow_offset = shadow_config['distance']
        shadow_color = (0, 0, 0, int(255 * shadow_config['opacity']))
        
        draw.text(
            (text_x + shadow_offset, line_y + shadow_offset),
            line, font=font, fill=shadow_color
        )
        
        # 2. Texto principal en blanco
        draw.text((text_x, line_y), line, font=font, fill='white')
        
        # 3. Sombra interior (simulada con overlay)
        inner_shadow_config = config['effects']['text']['inner_shadow']
        inner_color = (0, 0, 0, int(255 * inner_shadow_config['opacity']))
        
        # Dibujar texto ligeramente desplazado para simular sombra interior
        inner_offset = 2
        draw.text(
            (text_x + inner_offset, line_y + inner_offset),
            line, font=font, fill=inner_color
        )
    
    return canvas


def add_icons_with_effects(canvas, icons_data, config):
    """Añade iconos con sombras."""
    if not icons_data:
        return canvas
    
    # Configuración de iconos
    icon_size = 120  # Tamaño base para iconos
    spacing = 40     # Espaciado entre iconos
    
    # Procesar iconos
    processed_icons = []
    for icon_data in icons_data[:4]:  # Máximo 4 iconos
        icon_img = decode_base64_image(icon_data)
        icon_resized = icon_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        processed_icons.append(icon_resized)
    
    if not processed_icons:
        return canvas
    
    # Calcular posición centrada horizontal
    total_width = len(processed_icons) * icon_size + (len(processed_icons) - 1) * spacing
    start_x = (canvas.width - total_width) / 2
    icon_y = canvas.height - 200  # 200px desde abajo
    
    # Dibujar cada icono con sombra
    for i, icon in enumerate(processed_icons):
        icon_x = start_x + i * (icon_size + spacing)
        
        # 1. Sombra paralela
        shadow_config = config['effects']['icons']['drop_shadow']
        shadow_offset = shadow_config['distance']
        
        # Crear sombra
        shadow = Image.new('RGBA', icon.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Dibujar sombra como rectángulo semi-transparente
        shadow_color = (0, 0, 0, int(255 * shadow_config['opacity']))
        shadow_draw.rectangle([0, 0, icon_size, icon_size], fill=shadow_color)
        
        # Aplicar desenfoque a la sombra
        shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(shadow_config['size'] / 10))
        
        # Pegar sombra
        canvas.paste(
            shadow_blurred,
            (int(icon_x + shadow_offset), int(icon_y + shadow_offset)),
            shadow_blurred
        )
        
        # 2. Icono principal
        canvas.paste(icon, (int(icon_x), int(icon_y)), icon)
    
    return canvas


def get_font(size):
    """Obtiene fuente con fallbacks."""
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVu-Sans-Bold-Oblique.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf',
        '/usr/share/fonts/truetype/ubuntu/Ubuntu-BI.ttf',
        '/System/Library/Fonts/Arial Bold Italic.ttf',  # macOS
        '/Windows/Fonts/arialbi.ttf',  # Windows
    ]
    
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, int(size))
        except:
            continue
    
    # Fallback a fuente por defecto
    try:
        return ImageFont.load_default()
    except:
        return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    """Divide texto en múltiples líneas si es necesario."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        
        if line_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def encode_image_to_base64(image):
    """Convierte imagen PIL a base64."""
    # Convertir a RGB para PNG
    if image.mode == 'RGBA':
        # Crear fondo blanco
        background = Image.new('RGB', image.size, 'white')
        background.paste(image, mask=image.split()[-1])  # Usar canal alpha como máscara
        image = background
    
    buffer = io.BytesIO()
    image.save(buffer, format='PNG', quality=95, optimize=True)
    
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


# Handler para Netlify
def handler(event, context):
    return handler(event, context)
