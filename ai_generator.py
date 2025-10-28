"""
Módulo de generación de imágenes con IA usando OpenAI DALL-E.
Maneja la creación de prompts y la generación de imágenes para fondos e iconos.
"""

import os
import requests
from io import BytesIO
from PIL import Image
import time

def generate_image_with_dalle(prompt, api_key, size="1024x1024", quality="standard"):
    """
    Genera una imagen usando DALL-E 3 de OpenAI.
    
    Args:
        prompt (str): Descripción de la imagen a generar
        api_key (str): Token de API de OpenAI
        size (str): Tamaño de la imagen ("1024x1024", "1792x1024", "1024x1792")
        quality (str): Calidad de la imagen ("standard", "hd")
        
    Returns:
        PIL.Image or None: Imagen generada o None si hubo error
    """
    try:
        print(f"\n🎨 Generando imagen con IA...")
        print(f"   📝 Prompt: {prompt}")
        print(f"   📏 Tamaño: {size}")
        
        # Endpoint de DALL-E 3
        url = "https://api.openai.com/v1/images/generations"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": quality,
            "response_format": "url"
        }
        
        # Hacer la petición
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            print(f"   ✅ Imagen generada exitosamente")
            print(f"   🔗 URL: {image_url}")
            
            # Descargar la imagen
            img_response = requests.get(image_url, timeout=30)
            img = Image.open(BytesIO(img_response.content))
            
            print(f"   📦 Imagen descargada: {img.size}")
            
            return img
        else:
            error_data = response.json()
            error_message = error_data.get('error', {}).get('message', 'Error desconocido')
            print(f"   ❌ Error de OpenAI: {error_message}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout: La generación tomó demasiado tiempo")
        return None
    except Exception as e:
        print(f"   ❌ Error al generar imagen: {str(e)}")
        return None


def generate_background_image(user_post_description, api_key):
    """
    Genera una imagen de fondo (1920x1080) para un thumbnail basándose en la descripción del post.
    
    Args:
        user_post_description (str): Descripción del post del usuario
        api_key (str): Token de API de OpenAI
        
    Returns:
        PIL.Image or None: Imagen generada o None si hubo error
    """
    # Prompt template optimizado para imágenes de fondo de thumbnails
    prompt_template = f"""Create a professional stock photo style background image in landscape orientation (16:9 ratio). 
The image should be suitable as a YouTube thumbnail or blog post background.
Style: Modern, clean, professional, with good contrast and visual appeal.
Subject: {user_post_description}
Important: Leave enough negative space in the center for text overlay. 
The image should be visually interesting but not too busy or cluttered.
Colors: Vibrant but professional, suitable for tech/professional content.
Avoid: Text, logos, watermarks, faces unless specifically mentioned in the subject."""

    print("\n🖼️  GENERANDO IMAGEN DE FONDO")
    print("═" * 60)
    
    # DALL-E 3 soporta 1792x1024 que es más cercano a 16:9
    img = generate_image_with_dalle(
        prompt=prompt_template,
        api_key=api_key,
        size="1792x1024",  # Landscape format
        quality="standard"
    )
    
    if img:
        # Redimensionar a 1920x1080 exactamente
        img_resized = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        print(f"   📐 Redimensionado a 1920x1080")
        return img_resized
    
    return None


def generate_icon_image(user_post_description, api_key, icon_number=1):
    """
    Genera un icono representativo basándose en la descripción del post.
    
    Args:
        user_post_description (str): Descripción del post del usuario
        api_key (str): Token de API de OpenAI
        icon_number (int): Número del icono (1 o 2) para variación
        
    Returns:
        PIL.Image or None: Imagen generada o None si hubo error
    """
    # Prompt template optimizado para iconos
    prompt_template = f"""Create a simple, clean icon or logo that represents the following concept:
{user_post_description}

Style requirements:
- Minimalist and modern design
- Clear and recognizable symbol
- Professional and suitable for a thumbnail
- Transparent or clean background preferred
- Bold and clear shapes
- Works well at small sizes
- No text or letters
- Icon variation {icon_number} (make it slightly different if generating multiple)

The icon should be symbolic and instantly recognizable, similar to app icons or logo designs."""

    print(f"\n🎯 GENERANDO ICONO #{icon_number}")
    print("═" * 60)
    
    # Tamaño cuadrado para iconos
    img = generate_image_with_dalle(
        prompt=prompt_template,
        api_key=api_key,
        size="1024x1024",
        quality="standard"
    )
    
    if img:
        print(f"   ✅ Icono #{icon_number} generado exitosamente")
        return img
    
    return None


def save_generated_image(image, output_path):
    """
    Guarda una imagen generada en el sistema de archivos.
    
    Args:
        image (PIL.Image): Imagen a guardar
        output_path (str): Ruta donde guardar la imagen
        
    Returns:
        bool: True si se guardó correctamente
    """
    try:
        # Asegurarse de que el directorio existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Guardar como PNG con buena calidad
        image.save(output_path, "PNG", optimize=False, compress_level=1)
        
        print(f"   💾 Imagen guardada: {output_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error al guardar imagen: {str(e)}")
        return False


def test_openai_token(api_key):
    """
    Verifica si un token de OpenAI es válido haciendo una petición de prueba.
    
    Args:
        api_key (str): Token de API a verificar
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    try:
        url = "https://api.openai.com/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return True, "Token válido"
        elif response.status_code == 401:
            return False, "Token inválido o expirado"
        else:
            return False, f"Error al verificar token (código {response.status_code})"
            
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"


if __name__ == '__main__':
    print("🧪 Módulo de generación con IA")
    print("Este módulo se importa desde web_app.py")
    print("\nFunciones disponibles:")
    print("  - generate_background_image()")
    print("  - generate_icon_image()")
    print("  - test_openai_token()")
