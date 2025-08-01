/**
 * Thumbnail Generator - JavaScript Image Processing Engine
 * ========================================================
 * 
 * Motor de procesamiento de imágenes puramente frontend
 * Compatible con Netlify y sin necesidad de backend
 */

class ThumbnailGenerator {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.config = {
            width: 1920,
            height: 1080,
            blur: 20,
            maxIcons: 4,
            font: {
                family: 'Alliance No.2 Bold Italic, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif',
                baseSize: 380,
                minSize: 280,
                maxLines: 2
            },
            effects: {
                text: {
                    dropShadow: {
                        opacity: 0.85,
                        distance: 9,
                        blur: 40,
                        color: 'rgba(0, 0, 0, 0.85)'
                    },
                    innerShadow: {
                        opacity: 0.45,
                        angle: 30,
                        distance: 8,
                        color: 'rgba(0, 0, 0, 0.45)'
                    }
                },
                icons: {
                    dropShadow: {
                        opacity: 0.85,
                        distance: 9,
                        blur: 40,
                        color: 'rgba(0, 0, 0, 0.85)'
                    }
                }
            }
        };
    }

    /**
     * Inicializa el canvas con las dimensiones correctas
     */
    initCanvas(canvasElement) {
        this.canvas = canvasElement;
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = this.config.width;
        this.canvas.height = this.config.height;
        
        // Configuración de renderizado de alta calidad
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
    }

    /**
     * Carga una imagen desde archivo o URL
     */
    loadImage(source) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = 'anonymous';
            
            img.onload = () => resolve(img);
            img.onerror = () => reject(new Error('Error cargando imagen'));
            
            if (source instanceof File) {
                const reader = new FileReader();
                reader.onload = (e) => img.src = e.target.result;
                reader.onerror = () => reject(new Error('Error leyendo archivo'));
                reader.readAsDataURL(source);
            } else if (typeof source === 'string') {
                img.src = source;
            } else {
                reject(new Error('Tipo de imagen no soportado'));
            }
        });
    }

    /**
     * Procesa la imagen de fondo con redimensionado y desenfoque
     */
    processBackground(img) {
        // Calcular dimensiones manteniendo aspecto
        const ratioOriginal = img.width / img.height;
        const ratioObjetivo = this.config.width / this.config.height;
        
        let newWidth, newHeight;
        if (ratioOriginal > ratioObjetivo) {
            newHeight = this.config.height;
            newWidth = newHeight * ratioOriginal;
        } else {
            newWidth = this.config.width;
            newHeight = newWidth / ratioOriginal;
        }

        // Limpiar canvas
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.config.width, this.config.height);

        // Centrar y dibujar imagen
        const x = (this.config.width - newWidth) / 2;
        const y = (this.config.height - newHeight) / 2;
        
        this.ctx.drawImage(img, x, y, newWidth, newHeight);

        // Aplicar desenfoque (simulado con múltiples capas de opacidad)
        this.applyBlurEffect();
    }

    /**
     * Aplica efecto de desenfoque al fondo
     */
    applyBlurEffect() {
        // Crear capa semitransparente para simular desenfoque
        const imageData = this.ctx.getImageData(0, 0, this.config.width, this.config.height);
        
        // Aplicar filtro CSS blur si está soportado
        this.ctx.filter = `blur(${this.config.blur}px)`;
        this.ctx.drawImage(this.canvas, 0, 0);
        this.ctx.filter = 'none';
        
        // Oscurecer ligeramente para mejor contraste del texto
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(0, 0, this.config.width, this.config.height);
    }

    /**
     * Calcula el tamaño óptimo de fuente para el texto
     */
    calculateOptimalFontSize(text) {
        let fontSize = this.config.font.baseSize;
        const maxWidth = this.config.width * 0.85; // 85% del ancho
        const maxHeight = this.config.height * 0.45; // 45% del alto
        
        while (fontSize > this.config.font.minSize) {
            this.ctx.font = `italic bold ${fontSize}px ${this.config.font.family}`;
            
            // Dividir texto en líneas
            const lines = this.wrapText(text, maxWidth);
            
            if (lines.length <= this.config.font.maxLines) {
                const totalHeight = lines.length * fontSize * 1.1;
                if (totalHeight <= maxHeight) {
                    return { fontSize, lines };
                }
            }
            
            fontSize -= 15; // Reducir en pasos más pequeños
        }
        
        // Fallback: usar tamaño mínimo
        this.ctx.font = `italic bold ${this.config.font.minSize}px ${this.config.font.family}`;
        const fallbackLines = this.wrapText(text, maxWidth);
        return { 
            fontSize: this.config.font.minSize, 
            lines: fallbackLines.slice(0, this.config.font.maxLines) 
        };
    }

    /**
     * Divide el texto en líneas que caben en el ancho especificado
     */
    wrapText(text, maxWidth) {
        const words = text.split(' ');
        const lines = [];
        let currentLine = '';

        for (const word of words) {
            const testLine = currentLine + (currentLine ? ' ' : '') + word;
            const metrics = this.ctx.measureText(testLine);
            
            if (metrics.width > maxWidth && currentLine) {
                lines.push(currentLine);
                currentLine = word;
            } else {
                currentLine = testLine;
            }
        }
        
        if (currentLine) {
            lines.push(currentLine);
        }
        
        return lines;
    }

    /**
     * Dibuja texto con efectos de sombra
     */
    drawTextWithEffects(lines, fontSize) {
        const centerX = this.config.width / 2;
        const lineHeight = fontSize * 1.2;
        const totalHeight = lines.length * lineHeight;
        const startY = (this.config.height / 2) - (totalHeight / 2) + (lineHeight / 2);

        lines.forEach((line, index) => {
            const y = startY + (index * lineHeight);
            
            // Sombra exterior (drop shadow)
            this.ctx.save();
            this.ctx.shadowColor = this.config.effects.text.dropShadow.color;
            this.ctx.shadowBlur = this.config.effects.text.dropShadow.blur;
            this.ctx.shadowOffsetX = this.config.effects.text.dropShadow.distance;
            this.ctx.shadowOffsetY = this.config.effects.text.dropShadow.distance;
            
            this.ctx.fillStyle = '#FFFFFF';
            this.ctx.font = `italic bold ${fontSize}px ${this.config.font.family}`;
            this.ctx.fillText(line, centerX, y);
            this.ctx.restore();

            // Sombra interior (simulada)
            this.ctx.save();
            this.ctx.globalCompositeOperation = 'multiply';
            this.ctx.fillStyle = this.config.effects.text.innerShadow.color;
            
            // Calcular offset basado en ángulo
            const angle = this.config.effects.text.innerShadow.angle * Math.PI / 180;
            const offsetX = Math.cos(angle) * this.config.effects.text.innerShadow.distance;
            const offsetY = Math.sin(angle) * this.config.effects.text.innerShadow.distance;
            
            this.ctx.fillText(line, centerX + offsetX, y + offsetY);
            this.ctx.restore();
        });
    }

    /**
     * Procesa y posiciona los iconos
     */
    async drawIcons(iconFiles) {
        if (!iconFiles || iconFiles.length === 0) return;
        
        const icons = await Promise.all(
            Array.from(iconFiles).slice(0, this.config.maxIcons).map(file => this.loadImage(file))
        );

        const iconSize = this.calculateIconSize(icons.length);
        const totalWidth = icons.length * iconSize + (icons.length - 1) * (iconSize * 0.15); // Menos separación
        const startX = (this.config.width - totalWidth) / 2;
        const iconY = this.config.height * 0.78; // Un poco más abajo (era 0.75)

        icons.forEach((icon, index) => {
            const x = startX + index * (iconSize + iconSize * 0.15); // Menos separación
            
            // Sombra para iconos
            this.ctx.save();
            this.ctx.shadowColor = this.config.effects.icons.dropShadow.color;
            this.ctx.shadowBlur = this.config.effects.icons.dropShadow.blur;
            this.ctx.shadowOffsetX = this.config.effects.icons.dropShadow.distance;
            this.ctx.shadowOffsetY = this.config.effects.icons.dropShadow.distance;
            
            this.ctx.drawImage(icon, x, iconY - iconSize/2, iconSize, iconSize);
            this.ctx.restore();
        });
    }

    /**
     * Calcula el tamaño óptimo para los iconos
     */
    calculateIconSize(iconCount) {
        const baseSize = 280; // Mucho más grande que antes (era 150)
        const maxWidth = this.config.width * 0.8; // 80% del ancho disponible
        
        // Calcular tamaño basado en cantidad de iconos
        let iconSize = baseSize;
        const totalWidthNeeded = iconCount * iconSize + (iconCount - 1) * (iconSize * 0.15);
        
        if (totalWidthNeeded > maxWidth) {
            iconSize = maxWidth / (iconCount + (iconCount - 1) * 0.15);
        }
        
        return Math.max(180, Math.min(320, iconSize)); // Entre 180px y 320px (antes era 80-200)
    }

    /**
     * Genera el thumbnail completo
     */
    async generateThumbnail(backgroundImage, title, iconFiles = []) {
        try {
            // Cargar imagen de fondo
            const bgImg = await this.loadImage(backgroundImage);
            
            // Procesar fondo
            this.processBackground(bgImg);
            
            // Calcular y dibujar texto
            const { fontSize, lines } = this.calculateOptimalFontSize(title);
            this.drawTextWithEffects(lines, fontSize);
            
            // Dibujar iconos si existen
            if (iconFiles.length > 0) {
                await this.drawIcons(iconFiles);
            }
            
            return this.canvas.toDataURL('image/png', 0.9);
            
        } catch (error) {
            console.error('Error generando thumbnail:', error);
            throw error;
        }
    }

    /**
     * Descarga el thumbnail como archivo
     */
    downloadThumbnail(filename = 'thumbnail.png') {
        const link = document.createElement('a');
        link.download = filename;
        link.href = this.canvas.toDataURL('image/png', 0.9);
        link.click();
    }
}

// Exportar para uso global
window.ThumbnailGenerator = ThumbnailGenerator;
