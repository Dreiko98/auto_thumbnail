# Generador Automático de Thumbnails

Script en Python 3.11 que genera automáticamente thumbnails para blog con imagen de fondo, título centrado e iconos.

## Características

- ✅ Redimensiona imagen base a 1920×1080px con desenfoque gaussiano
- ✅ Título centrado con sombras interior y exterior
- ✅ Iconos escalados y centrados en fila horizontal
- ✅ Descarga automática de imágenes desde URLs
- ✅ Exportación a PNG optimizado
- ✅ Capas separadas simulando archivo PSD

## Instalación

```bash
# Ejecutar script de instalación
./install_dependencies.sh

# O instalar manualmente
pip install -r requirements.txt
```

## Uso

### Modo Interactivo (Recomendado):
```bash
python3 generate_thumbnail.py
```
El script te guiará paso a paso solicitando:
- **Imagen de fondo**: Ruta local o URL
- **Título**: Texto que aparecerá centrado  
- **Iconos**: Rutas/URLs separadas por comas (opcional)
- **Nombre de salida**: Nombre base para los archivos

### Modo por argumentos:
```bash
python3 generate_thumbnail.py "imagen_fondo.jpg" "Mi Título Genial" "icono1.png" "icono2.png"
```

### Ejemplos de uso interactivo:

**Ejemplo 1 - Con imagen local:**
```
📸 Imagen de fondo: /home/usuario/imagenes/fondo.jpg
📝 Título: Tutorial de Python Avanzado
🎯 Iconos: python.png, vscode.png, git.png
💾 Nombre de salida: tutorial_python
```

**Ejemplo 2 - Con URLs:**
```
📸 Imagen de fondo: https://picsum.photos/1920/1080
📝 Título: Desarrollo Web Moderno
🎯 Iconos: https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg, https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg
💾 Nombre de salida: web_moderno
```

**Ejemplo 3 - Solo texto (sin iconos):**
```
📸 Imagen de fondo: paisaje.jpg
📝 Título: Mi Blog Personal
🎯 Iconos: [dejar vacío]
💾 Nombre de salida: blog_header
```

## Salidas

- `thumbnail.png` - Imagen final optimizada
- `thumbnail_capas/` - Directorio con capas separadas:
  - `01_fondo_desenfocado.png` - Imagen base procesada
  - `02_texto_info.txt` - Información del texto
  - `03_icono_01.png`, `03_icono_02.png`, etc. - Iconos individuales

## Especificaciones Técnicas

- **Resolución**: 1920 × 1080 píxeles
- **Desenfoque**: Gaussiano 20px en imagen base
- **Fuente**: Arial (15% altura imagen) con fallback automático
- **Sombras texto**: Interior (negro 35%) + Exterior (negro 50%)
- **Iconos**: Máximo 20% ancho imagen, centrados con sombras
- **Formatos**: PNG sin compresión, capas PSD simuladas

## Dependencias

- Python 3.11+
- Pillow (manipulación imágenes)
- requests (descarga URLs)

## Estructura del Código

```python
- descargar_imagen()          # Descarga/carga imágenes
- procesar_imagen_base()      # Redimensiona y desenfoca
- añadir_titulo()            # Texto centrado con sombras
- procesar_iconos()          # Descarga y escala iconos
- añadir_iconos()           # Coloca iconos en fila
- guardar_como_psd_simulado() # Exporta capas separadas
- generar_thumbnail()        # Función principal
```

## Ejemplos de Resultados

El script genera thumbnails profesionales con:
- Fondo desenfocado mantiendo proporción
- Texto legible con efectos de sombra
- Iconos tecnológicos centrados y proporcionados
- Calidad optimizada para web y redes sociales
