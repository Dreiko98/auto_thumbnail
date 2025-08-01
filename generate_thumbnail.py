#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Automático de Thumbnails para Blog
============================================

Script que genera thumbnails de 1920x1080px con:
- Imagen de fondo desenfocada
- Título centrado con sombras
- Iconos en fila horizontal centrada
- Exportación a PNG y PSD con capas separadas

Autor: Desarrollador Senior Python
Fecha: Julio 2025
"""

import os
import sys
import requests
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import tempfile


def descargar_imagen(url_o_ruta):
    """
    Descarga una imagen desde URL o carga desde ruta local.
    
    Args:
        url_o_ruta (str): URL o ruta local de la imagen
        
    Returns:
        PIL.Image: Imagen cargada
    """
    if url_o_ruta.startswith(('http://', 'https://')):
        try:
            response = requests.get(url_o_ruta, timeout=30, stream=True)
            response.raise_for_status()
            
            # Obtener tamaño si está disponible
            tamaño = response.headers.get('content-length')
            if tamaño:
                tamaño_mb = int(tamaño) / (1024 * 1024)
                if tamaño_mb > 10:  # Advertir si es muy grande
                    print(f"⚠️  Imagen grande detectada: {tamaño_mb:.1f} MB")
            
            return Image.open(BytesIO(response.content))
        except requests.exceptions.Timeout:
            print(f"❌ Timeout al descargar: {url_o_ruta}")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error procesando imagen remota: {e}")
            sys.exit(1)
    else:
        try:
            if not os.path.exists(url_o_ruta):
                print(f"❌ Archivo no encontrado: {url_o_ruta}")
                sys.exit(1)
            
            # Verificar tamaño del archivo local
            tamaño_mb = os.path.getsize(url_o_ruta) / (1024 * 1024)
            if tamaño_mb > 20:
                print(f"⚠️  Archivo grande: {tamaño_mb:.1f} MB")
            
            return Image.open(url_o_ruta)
        except Exception as e:
            print(f"❌ Error cargando imagen local: {e}")
            sys.exit(1)


def procesar_imagen_base(imagen_base, ancho=1920, alto=1080):
    """
    Redimensiona la imagen base y aplica desenfoque gaussiano.
    
    Args:
        imagen_base (PIL.Image): Imagen base original
        ancho (int): Ancho objetivo en píxeles
        alto (int): Alto objetivo en píxeles
        
    Returns:
        PIL.Image: Imagen procesada
    """
    # Convertir a RGB si es necesario
    if imagen_base.mode != 'RGB':
        imagen_base = imagen_base.convert('RGB')
    
    # Calcular dimensiones manteniendo aspecto
    ratio_original = imagen_base.width / imagen_base.height
    ratio_objetivo = ancho / alto
    
    if ratio_original > ratio_objetivo:
        # La imagen es más ancha, ajustar por altura
        nuevo_alto = alto
        nuevo_ancho = int(alto * ratio_original)
    else:
        # La imagen es más alta, ajustar por ancho
        nuevo_ancho = ancho
        nuevo_alto = int(ancho / ratio_original)
    
    # Redimensionar
    imagen_redimensionada = imagen_base.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    
    # Crear canvas final y centrar imagen
    canvas = Image.new('RGB', (ancho, alto), (0, 0, 0))
    x_offset = (ancho - nuevo_ancho) // 2
    y_offset = (alto - nuevo_alto) // 2
    canvas.paste(imagen_redimensionada, (x_offset, y_offset))
    
    # Aplicar desenfoque gaussiano
    imagen_desenfocada = canvas.filter(ImageFilter.GaussianBlur(radius=20))
    
    return imagen_desenfocada


def obtener_fuente(tamano):
    """
    Obtiene la fuente Arial o una alternativa del sistema.
    
    Args:
        tamano (int): Tamaño de la fuente
        
    Returns:
        PIL.ImageFont: Objeto de fuente
    """
    # Intentar cargar Arial o fuentes alternativas comunes
    fuentes_posibles = [
        "arial.ttf",
        "Arial.ttf", 
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/arial.ttf",
        "/System/Library/Fonts/Arial.ttf",  # macOS
        "C:/Windows/Fonts/arial.ttf"  # Windows
    ]
    
    for fuente in fuentes_posibles:
        try:
            return ImageFont.truetype(fuente, tamano)
        except:
            continue
    
    # Si no encuentra ninguna, usar fuente por defecto
    print("Advertencia: No se pudo cargar Arial, usando fuente por defecto")
    return ImageFont.load_default()


def crear_sombra_texto(draw, texto, posicion, fuente, color_sombra, blur, offset):
    """
    Crea efecto de sombra para texto.
    
    Args:
        draw (PIL.ImageDraw): Objeto de dibujo
        texto (str): Texto a dibujar
        posicion (tuple): Posición (x, y)
        fuente (PIL.ImageFont): Fuente a usar
        color_sombra (tuple): Color de la sombra RGBA
        blur (int): Intensidad del blur
        offset (tuple): Desplazamiento (x, y) de la sombra
    """
    x, y = posicion
    offset_x, offset_y = offset
    
    # Dibujar sombra con offset
    draw.text((x + offset_x, y + offset_y), texto, font=fuente, fill=color_sombra)


def dividir_texto_en_lineas(texto, fuente, ancho_max):
    """
    Divide el texto en múltiples líneas si es necesario para que quepa en el ancho máximo.
    
    Args:
        texto (str): Texto a dividir
        fuente (PIL.ImageFont): Fuente a usar
        ancho_max (int): Ancho máximo disponible
        
    Returns:
        list: Lista de líneas de texto
    """
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        linea_prueba = f"{linea_actual} {palabra}".strip()
        bbox = fuente.getbbox(linea_prueba)
        ancho_linea = bbox[2] - bbox[0]
        
        if ancho_linea <= ancho_max:
            linea_actual = linea_prueba
        else:
            if linea_actual:
                lineas.append(linea_actual)
                linea_actual = palabra
            else:
                # Si una sola palabra es muy larga, la forzamos
                lineas.append(palabra)
                linea_actual = ""
    
    if linea_actual:
        lineas.append(linea_actual)
    
    return lineas


def añadir_titulo(imagen, titulo, ancho=1920, alto=1080):
    """
    Añade el título centrado con efectos de sombra suave, sin contornos.
    
    Args:
        imagen (PIL.Image): Imagen base
        titulo (str): Texto del título
        ancho (int): Ancho de la imagen
        alto (int): Alto de la imagen
        
    Returns:
        PIL.Image: Imagen con título añadido
    """
    # Crear copia para no modificar original
    img_con_titulo = imagen.copy().convert('RGBA')
    
    # Calcular tamaño de fuente inicial (12% de la altura para permitir múltiples líneas)
    tamano_fuente = int(alto * 0.12)
    fuente = obtener_fuente(tamano_fuente)
    
    # Ancho máximo para el texto (85% del ancho total)
    ancho_max_texto = int(ancho * 0.85)
    
    # Dividir texto en líneas
    lineas = dividir_texto_en_lineas(titulo, fuente, ancho_max_texto)
    
    # Ajustar tamaño de fuente si hay muchas líneas
    if len(lineas) > 2:
        tamano_fuente = int(alto * 0.09)
        fuente = obtener_fuente(tamano_fuente)
        lineas = dividir_texto_en_lineas(titulo, fuente, ancho_max_texto)
    
    # Calcular altura total del bloque de texto
    bbox_linea = fuente.getbbox("Ay")
    alto_linea = bbox_linea[3] - bbox_linea[1]
    espaciado_lineas = int(alto_linea * 0.3)  # Más espacio entre líneas
    alto_total_texto = len(lineas) * alto_linea + (len(lineas) - 1) * espaciado_lineas
    
    # Posición Y centrada (o ligeramente arriba si hay iconos)
    y_inicial = int((alto - alto_total_texto) * 0.4)  # Más arriba para dar espacio a iconos
    
    # Crear múltiples capas de sombras para efecto suave
    img_sombras = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    
    # Dibujar cada línea con sombras mejoradas
    y_actual = y_inicial
    for linea in lineas:
        bbox_actual = fuente.getbbox(linea)
        ancho_linea = bbox_actual[2] - bbox_actual[0]
        x = (ancho - ancho_linea) // 2
        
        # Crear imagen temporal para esta línea con múltiples sombras
        temp_sombra = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
        draw_temp = ImageDraw.Draw(temp_sombra)
        
        # Sombra exterior difusa (múltiples capas)
        for offset in range(1, 8):
            opacity = max(10, 60 - offset * 8)  # Sombra que se desvanece
            for dx in [-offset, 0, offset]:
                for dy in [-offset, 0, offset]:
                    if dx != 0 or dy != 0:
                        draw_temp.text((x + dx, y_actual + dy), linea, 
                                     font=fuente, fill=(0, 0, 0, opacity))
        
        # Aplicar blur progresivo
        temp_sombra = temp_sombra.filter(ImageFilter.GaussianBlur(radius=6))
        img_sombras = Image.alpha_composite(img_sombras, temp_sombra)
        
        y_actual += alto_linea + espaciado_lineas
    
    # Combinar sombras con imagen
    img_con_titulo = Image.alpha_composite(img_con_titulo, img_sombras)
    
    # Dibujar texto principal sin contornos duros
    draw_final = ImageDraw.Draw(img_con_titulo)
    y_actual = y_inicial
    
    for linea in lineas:
        bbox_actual = fuente.getbbox(linea)
        ancho_linea = bbox_actual[2] - bbox_actual[0]
        x = (ancho - ancho_linea) // 2
        
        # Solo sombra muy sutil para definición
        draw_final.text((x + 1, y_actual + 1), linea, font=fuente, fill=(0, 0, 0, 100))
        
        # Texto principal blanco brillante
        draw_final.text((x, y_actual), linea, font=fuente, fill=(255, 255, 255, 255))
        
        y_actual += alto_linea + espaciado_lineas
    
    return img_con_titulo.convert('RGB')


def procesar_iconos(lista_iconos, ancho_max_por_icono):
    """
    Descarga y procesa los iconos redimensionándolos.
    
    Args:
        lista_iconos (list): Lista de URLs/rutas de iconos
        ancho_max_por_icono (int): Ancho máximo por icono
        
    Returns:
        list: Lista de imágenes PIL procesadas
    """
    iconos_procesados = []
    
    for i, icono_path in enumerate(lista_iconos, 1):
        try:
            # Descargar/cargar icono
            icono = descargar_imagen(icono_path)
            
            # Convertir a RGBA para preservar transparencia
            if icono.mode not in ['RGBA', 'LA']:
                if icono.mode == 'P' and 'transparency' in icono.info:
                    icono = icono.convert('RGBA')
                else:
                    icono = icono.convert('RGBA')
            
            # Redimensionar manteniendo aspecto
            ratio = icono.width / icono.height
            if icono.width > icono.height:
                nuevo_ancho = min(ancho_max_por_icono, icono.width)
                nuevo_alto = int(nuevo_ancho / ratio)
            else:
                nuevo_alto = min(ancho_max_por_icono, icono.height)
                nuevo_ancho = int(nuevo_alto * ratio)
            
            icono_redimensionado = icono.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
            iconos_procesados.append(icono_redimensionado)
            
        except Exception as e:
            print(f"\n⚠️  Error procesando icono {i}: {icono_path}")
            print(f"   Error: {e}")
            print("   Continuando sin este icono...")
            continue
    
    return iconos_procesados


def añadir_iconos(imagen, iconos, ancho=1920, alto=1080):
    """
    Añade los iconos en fila horizontal centrada, asegurándose de que quepan completamente.
    
    Args:
        imagen (PIL.Image): Imagen con título
        iconos (list): Lista de imágenes PIL de iconos
        ancho (int): Ancho de la imagen
        alto (int): Alto de la imagen
        
    Returns:
        PIL.Image: Imagen final con iconos
    """
    if not iconos:
        return imagen
    
    img_final = imagen.copy().convert('RGBA')
    
    # Calcular tamaño óptimo para iconos basado en la cantidad
    if len(iconos) == 1:
        tamano_max_icono = int(ancho * 0.12)  # Un solo icono puede ser más grande
    elif len(iconos) <= 3:
        tamano_max_icono = int(ancho * 0.08)  # 2-3 iconos
    else:
        tamano_max_icono = int(ancho * 0.06)  # 4+ iconos más pequeños
    
    # Asegurar tamaño mínimo y máximo
    tamano_max_icono = max(60, min(tamano_max_icono, 150))
    
    # Redimensionar iconos a tamaño consistente
    iconos_redimensionados = []
    for icono in iconos:
        # Calcular nuevo tamaño manteniendo aspecto
        ratio = min(tamano_max_icono / icono.width, tamano_max_icono / icono.height)
        nuevo_ancho = int(icono.width * ratio)
        nuevo_alto = int(icono.height * ratio)
        
        icono_redim = icono.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        iconos_redimensionados.append(icono_redim)
    
    # Calcular espaciado dinámico
    espaciado_base = max(15, int(ancho * 0.015))
    ancho_total_iconos = sum(icono.width for icono in iconos_redimensionados)
    ancho_total_con_espacios = ancho_total_iconos + (espaciado_base * (len(iconos_redimensionados) - 1))
    
    # Si no caben todos, reducir espaciado
    if ancho_total_con_espacios > ancho * 0.9:
        espaciado = max(10, int((ancho * 0.9 - ancho_total_iconos) / (len(iconos_redimensionados) - 1)))
        ancho_total_con_espacios = ancho_total_iconos + (espaciado * (len(iconos_redimensionados) - 1))
    else:
        espaciado = espaciado_base
    
    # Posición inicial X para centrar la fila de iconos
    x_inicial = max(0, (ancho - ancho_total_con_espacios) // 2)
    
    # Posición Y: 72% de la altura (más arriba para no cortarse)
    # Asegurar que los iconos quepan dentro del canvas
    alto_max_icono = max(icono.height for icono in iconos_redimensionados)
    y_iconos = min(int(alto * 0.72), alto - alto_max_icono - 20)  # 20px de margen inferior
    
    x_actual = x_inicial
    
    for icono in iconos_redimensionados:
        # Centrar verticalmente cada icono en la línea base
        y_centrado = y_iconos + (alto_max_icono - icono.height) // 2
        
        # Verificar que el icono esté completamente dentro del canvas
        if x_actual + icono.width <= ancho and y_centrado + icono.height <= alto:
            # Crear sombra más elegante
            sombra = Image.new('RGBA', img_final.size, (0, 0, 0, 0))
            draw_sombra = ImageDraw.Draw(sombra)
            
            # Sombra suave y profesional
            for offset in range(1, 6):
                opacity = max(15, 40 - offset * 5)
                # Crear máscara de sombra usando el alpha del icono original
                temp_sombra = Image.new('RGBA', icono.size, (0, 0, 0, 0))
                for y in range(icono.height):
                    for x in range(icono.width):
                        r, g, b, a = icono.getpixel((x, y))
                        if a > 0:  # Solo donde hay contenido del icono
                            temp_sombra.putpixel((x, y), (0, 0, 0, min(opacity, a)))
                
                # Pegar sombra con offset
                sombra.paste(temp_sombra, (x_actual + offset, y_centrado + offset), temp_sombra)
            
            # Aplicar blur a la sombra
            sombra = sombra.filter(ImageFilter.GaussianBlur(radius=4))
            
            # Aplicar sombra
            img_final = Image.alpha_composite(img_final, sombra)
            
            # Pegar icono principal
            img_final.paste(icono, (x_actual, y_centrado), icono)
        
        # Avanzar posición X
        x_actual += icono.width + espaciado
    
    return img_final.convert('RGB')


def guardar_como_psd_simulado(imagen_fondo, imagen_con_titulo, iconos, titulo, ruta_salida):
    """
    Simula guardado PSD creando capas separadas como PNG individuales.
    Nota: psd-tools es principalmente para lectura. Para escritura real de PSD
    se necesitarían librerías comerciales como Photoshop scripting.
    
    Args:
        imagen_fondo (PIL.Image): Capa de fondo
        imagen_con_titulo (PIL.Image): Imagen con título
        iconos (list): Lista de iconos
        titulo (str): Texto del título
        ruta_salida (str): Ruta base para guardar archivos
    """
    # Crear directorio para capas
    directorio_capas = ruta_salida.replace('.psd', '_capas')
    os.makedirs(directorio_capas, exist_ok=True)
    
    print(f"Guardando capas simuladas en: {directorio_capas}")
    
    # Guardar capa de fondo
    imagen_fondo.save(os.path.join(directorio_capas, "01_fondo_desenfocado.png"))
    
    # Crear capa solo con texto (transparente)
    capa_texto = Image.new('RGBA', imagen_fondo.size, (0, 0, 0, 0))
    # Aquí se podría recrear solo el texto, por simplicidad guardamos referencia
    with open(os.path.join(directorio_capas, "02_texto_info.txt"), 'w', encoding='utf-8') as f:
        f.write(f"Título: {titulo}\n")
        f.write("Posición: Centrado\n")
        f.write("Color: #FFFFFF\n")
        f.write("Sombras: Interior (negro 35%) y Exterior (negro 50%)\n")
    
    # Guardar iconos individuales
    for i, icono in enumerate(iconos, 1):
        icono.save(os.path.join(directorio_capas, f"03_icono_{i:02d}.png"))
    
    print(f"Capas PSD simuladas guardadas en: {directorio_capas}")


def generar_thumbnail(imagen_base, titulo, iconos, ruta_salida="thumbnail"):
    """
    Función principal que genera el thumbnail completo.
    
    Args:
        imagen_base (str): Ruta o URL de la imagen base
        titulo (str): Título a mostrar
        iconos (list): Lista de rutas/URLs de iconos
        ruta_salida (str): Nombre base para archivos de salida
    """
    print("\n🚀 INICIANDO GENERACIÓN DE THUMBNAIL")
    print("═" * 60)
    
    pasos_totales = 5
    
    try:
        # 1. Cargar y procesar imagen base
        mostrar_progreso(1, pasos_totales, "Descargando y procesando imagen base...")
        img_original = descargar_imagen(imagen_base)
        img_fondo = procesar_imagen_base(img_original)
        
        # 2. Añadir título con sombras
        mostrar_progreso(2, pasos_totales, "Añadiendo título con efectos...")
        img_con_titulo = añadir_titulo(img_fondo, titulo)
        
        # 3. Procesar iconos
        mostrar_progreso(3, pasos_totales, "Procesando iconos...")
        ancho_max_icono = int(1920 * 0.15)  # 15% del ancho
        iconos_procesados = procesar_iconos(iconos, ancho_max_icono)
        
        # 4. Añadir iconos
        mostrar_progreso(4, pasos_totales, "Integrando iconos...")
        img_final = añadir_iconos(img_con_titulo, iconos_procesados)
        
        # 5. Guardar resultados
        mostrar_progreso(5, pasos_totales, "Guardando archivos...")
        
        # Guardar PNG final
        ruta_png = f"{ruta_salida}.png"
        img_final.save(ruta_png, "PNG", optimize=False, compress_level=1)
        
        # Guardar PSD simulado
        ruta_psd = f"{ruta_salida}.psd"
        guardar_como_psd_simulado(img_fondo, img_con_titulo, iconos_procesados, titulo, ruta_psd)
        
        print()
        print("✅ GENERACIÓN COMPLETADA CON ÉXITO")
        print("╔" + "═" * 58 + "╗")
        print("║" + "📁 ARCHIVOS GENERADOS:".ljust(58) + "║")
        print("║" + f"   🖼️  {ruta_png}".ljust(58) + "║")
        print("║" + f"   📂 {ruta_salida}_capas/ (capas separadas)".ljust(58) + "║")
        print("║" + " " * 58 + "║")
        print("║" + f"📊 ESTADÍSTICAS:".ljust(58) + "║")
        print("║" + f"   • Resolución: 1920x1080 píxeles".ljust(58) + "║")
        print("║" + f"   • Líneas de texto: {len(dividir_texto_en_lineas(titulo, obtener_fuente(130), 1536))}".ljust(58) + "║")
        print("║" + f"   • Iconos: {len(iconos)}".ljust(58) + "║")
        print("║" + f"   • Tamaño archivo: ~{os.path.getsize(ruta_png) // 1024} KB".ljust(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print()
        print("🎉 ¡Tu thumbnail está listo para usar!")
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA GENERACIÓN:")
        print(f"   {str(e)}")
        print("\n💡 CONSEJOS:")
        print("   • Verifica que la imagen base sea válida")
        print("   • Comprueba tu conexión a internet para URLs")
        print("   • Asegúrate de tener permisos de escritura")
        raise


def mostrar_banner():
    """Muestra un banner de bienvenida atractivo."""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "🎨 GENERADOR AUTOMÁTICO DE THUMBNAILS PARA BLOG".center(58) + "║")
    print("║" + "✨ Crea miniaturas profesionales en segundos ✨".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def mostrar_progreso(paso, total, descripcion):
    """Muestra una barra de progreso visual."""
    porcentaje = (paso / total) * 100
    barra_llena = int(porcentaje // 5)
    barra_vacia = 20 - barra_llena
    
    barra = "█" * barra_llena + "░" * barra_vacia
    print(f"\r🔄 [{barra}] {porcentaje:6.1f}% - {descripcion}", end="", flush=True)
    
    if paso == total:
        print("  ✅")


def solicitar_datos_usuario():
    """
    Solicita al usuario los datos necesarios para generar el thumbnail.
    
    Returns:
        tuple: (imagen_base, titulo, iconos, ruta_salida)
    """
    mostrar_banner()
    
    print("📋 Vamos a configurar tu thumbnail paso a paso:")
    print("─" * 60)
    print()
    
    # Solicitar imagen base
    print("📸 PASO 1: IMAGEN DE FONDO")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ Puedes usar:                                            │")
    print("│ • Ruta local: /home/usuario/imagenes/fondo.jpg          │")
    print("│ • URL remota: https://ejemplo.com/imagen.jpg            │")
    print("│ • Imagen de prueba: demo                                │")
    print("└─────────────────────────────────────────────────────────┘")
    
    while True:
        imagen_base = input("👉 Imagen de fondo: ").strip()
        
        if imagen_base.lower() == "demo":
            imagen_base = "https://picsum.photos/1920/1080"
            print(f"✅ Usando imagen de demostración: {imagen_base}")
            break
        elif imagen_base:
            print(f"✅ Imagen seleccionada: {imagen_base}")
            break
        else:
            print("❌ Por favor, ingresa una ruta de imagen válida")
    
    print()
    
    # Solicitar título
    print("📝 PASO 2: TÍTULO DEL THUMBNAIL")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ • El texto se centrará automáticamente                 │")
    print("│ • Se dividirá en líneas si es muy largo                │")
    print("│ • Máximo recomendado: 50 caracteres                    │")
    print("└─────────────────────────────────────────────────────────┘")
    
    while True:
        titulo = input("👉 Título: ").strip()
        if titulo:
            if len(titulo) > 80:
                confirmar = input("⚠️  El título es muy largo. ¿Continuar? (s/N): ").strip().lower()
                if confirmar in ['s', 'si', 'sí']:
                    break
            else:
                print(f"✅ Título: '{titulo}' ({len(titulo)} caracteres)")
                break
        else:
            print("❌ El título no puede estar vacío")
    
    print()
    
    # Solicitar iconos
    print("🎯 PASO 3: ICONOS (OPCIONAL)")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ • Separa múltiples iconos con comas                    │")
    print("│ • Acepta rutas locales y URLs                          │")
    print("│ • Presiona Enter para omitir                           │")
    print("│ • Iconos demo: demo                                     │")
    print("└─────────────────────────────────────────────────────────┘")
    
    iconos_input = input("👉 Iconos: ").strip()
    
    iconos = []
    if iconos_input.lower() == "demo":
        iconos = [
            "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
            "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
            "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"
        ]
        print(f"✅ Usando {len(iconos)} iconos de demostración")
    elif iconos_input:
        iconos = [icono.strip() for icono in iconos_input.split(',') if icono.strip()]
        print(f"✅ {len(iconos)} icono(s) configurado(s)")
    else:
        print("✅ Sin iconos (solo texto)")
    
    print()
    
    # Solicitar nombre de salida
    print("💾 PASO 4: ARCHIVO DE SALIDA")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ • Nombre sin extensión (se agrega .png automáticamente)│")
    print("│ • Deja vacío para usar 'thumbnail'                     │")
    print("└─────────────────────────────────────────────────────────┘")
    
    ruta_salida = input("👉 Nombre del archivo: ").strip()
    if not ruta_salida:
        ruta_salida = "thumbnail"
    
    print(f"✅ Archivo de salida: {ruta_salida}.png")
    print()
    
    # Mostrar resumen
    print("📋 RESUMEN DE CONFIGURACIÓN")
    print("╔" + "═" * 58 + "╗")
    print(f"║ {'PARÁMETRO':<20} │ {'VALOR':<35} ║")
    print("╠" + "═" * 20 + "┼" + "═" * 37 + "╣")
    print(f"║ {'Imagen':<20} │ {imagen_base[:35]:<35} ║")
    print(f"║ {'Título':<20} │ {titulo[:35]:<35} ║")
    print(f"║ {'Iconos':<20} │ {str(len(iconos)) + ' archivo(s)':<35} ║")
    
    for i, icono in enumerate(iconos[:3], 1):  # Mostrar máximo 3
        icono_mostrar = icono[:35] + "..." if len(icono) > 35 else icono
        print(f"║ {f'  {i}.':<20} │ {icono_mostrar:<35} ║")
    
    if len(iconos) > 3:
        print(f"║ {'  ...':<20} │ {f'y {len(iconos) - 3} más':<35} ║")
    
    print(f"║ {'Salida':<20} │ {ruta_salida + '.png':<35} ║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # Confirmación final
    confirmar = input("🚀 ¿Generar thumbnail? [S/n]: ").strip().lower()
    if confirmar in ['n', 'no']:
        print("❌ Operación cancelada")
        sys.exit(0)
    
    return imagen_base, titulo, iconos, ruta_salida


if __name__ == "__main__":
    # Si se proporcionan argumentos por línea de comandos, usarlos
    if len(sys.argv) >= 3:
        print("📌 Usando argumentos de línea de comandos...")
        imagen_base = sys.argv[1]
        titulo = sys.argv[2]
        iconos = sys.argv[3:] if len(sys.argv) > 3 else []
        ruta_salida = "thumbnail"
        
        print(f"   • Imagen: {imagen_base}")
        print(f"   • Título: {titulo}")
        print(f"   • Iconos: {len(iconos)} archivo(s)")
        print()
    else:
        # Modo interactivo: solicitar datos al usuario
        imagen_base, titulo, iconos, ruta_salida = solicitar_datos_usuario()
    
    # Generar thumbnail
    try:
        generar_thumbnail(imagen_base, titulo, iconos, ruta_salida)
    except KeyboardInterrupt:
        print("\n❌ Generación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        sys.exit(1)
