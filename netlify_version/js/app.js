/**
 * Aplicación Principal - Thumbnail Generator
 * ==========================================
 * 
 * Maneja la interfaz de usuario y la interacción
 */

class ThumbnailApp {
    constructor() {
        this.generator = new ThumbnailGenerator();
        this.backgroundImage = null;
        this.iconFiles = [];
        this.isGenerating = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.setupDragAndDrop();
        this.initializeCanvas();
    }

    initializeElements() {
        // Referencias DOM
        this.elements = {
            form: document.getElementById('thumbnailForm'),
            backgroundInput: document.getElementById('backgroundImage'),
            backgroundUpload: document.getElementById('backgroundUpload'),
            titleInput: document.getElementById('title'),
            charCount: document.getElementById('charCount'),
            iconsInput: document.getElementById('icons'),
            iconsUpload: document.getElementById('iconsUpload'),
            iconsPreview: document.getElementById('iconsPreview'),
            generateBtn: document.getElementById('generateBtn'),
            btnText: document.getElementById('btnText'),
            btnLoading: document.getElementById('btnLoading'),
            previewContainer: document.getElementById('previewContainer'),
            previewCanvas: document.getElementById('previewCanvas'),
            downloadBtn: document.getElementById('downloadBtn'),
            alerts: document.getElementById('alerts')
        };
    }

    setupEventListeners() {
        // Formulario
        this.elements.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateThumbnail();
        });

        // Archivos de fondo
        this.elements.backgroundInput.addEventListener('change', (e) => {
            this.handleBackgroundUpload(e.target.files[0]);
        });

        // Iconos
        this.elements.iconsInput.addEventListener('change', (e) => {
            this.handleIconsUpload(Array.from(e.target.files));
        });

        // Contador de caracteres
        this.elements.titleInput.addEventListener('input', (e) => {
            this.updateCharCount(e.target.value.length);
        });

        // Botón de descarga
        this.elements.downloadBtn.addEventListener('click', () => {
            this.downloadThumbnail();
        });

        // Prevenir comportamiento por defecto en drag events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            document.addEventListener(eventName, this.preventDefaults, false);
        });
    }

    setupDragAndDrop() {
        // Drag & Drop para imagen de fondo
        this.elements.backgroundUpload.addEventListener('dragenter', () => {
            this.elements.backgroundUpload.classList.add('drag-over');
        });

        this.elements.backgroundUpload.addEventListener('dragleave', (e) => {
            if (!e.currentTarget.contains(e.relatedTarget)) {
                this.elements.backgroundUpload.classList.remove('drag-over');
            }
        });

        this.elements.backgroundUpload.addEventListener('drop', (e) => {
            this.elements.backgroundUpload.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleBackgroundUpload(files[0]);
            }
        });

        // Drag & Drop para iconos
        this.elements.iconsUpload.addEventListener('dragenter', () => {
            this.elements.iconsUpload.classList.add('drag-over');
        });

        this.elements.iconsUpload.addEventListener('dragleave', (e) => {
            if (!e.currentTarget.contains(e.relatedTarget)) {
                this.elements.iconsUpload.classList.remove('drag-over');
            }
        });

        this.elements.iconsUpload.addEventListener('drop', (e) => {
            this.elements.iconsUpload.classList.remove('drag-over');
            const files = Array.from(e.dataTransfer.files);
            if (files.length > 0) {
                this.handleIconsUpload(files);
            }
        });
    }

    initializeCanvas() {
        this.generator.initCanvas(this.elements.previewCanvas);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    updateCharCount(count) {
        this.elements.charCount.textContent = `${count}/100 caracteres`;
        
        if (count > 80) {
            this.elements.charCount.style.color = '#d97706'; // Warning
        } else if (count > 95) {
            this.elements.charCount.style.color = '#dc2626'; // Error
        } else {
            this.elements.charCount.style.color = '#64748b'; // Normal
        }
    }

    async handleBackgroundUpload(file) {
        if (!this.validateImageFile(file)) {
            this.showAlert('Por favor, selecciona un archivo de imagen válido (PNG, JPG, WEBP)', 'error');
            return;
        }

        if (file.size > 10 * 1024 * 1024) { // 10MB
            this.showAlert('El archivo es demasiado grande. Máximo 10MB.', 'error');
            return;
        }

        try {
            this.backgroundImage = file;
            this.updateBackgroundUI(file);
            this.showAlert('✅ Imagen de fondo cargada correctamente', 'success');
        } catch (error) {
            this.showAlert('Error cargando la imagen de fondo', 'error');
            console.error(error);
        }
    }

    async handleIconsUpload(files) {
        const validFiles = files.filter(file => this.validateImageFile(file));
        
        if (validFiles.length === 0) {
            this.showAlert('No se encontraron archivos de imagen válidos', 'error');
            return;
        }

        if (validFiles.length > 4) {
            this.showAlert('Máximo 4 iconos permitidos. Se usarán los primeros 4.', 'warning');
            validFiles.splice(4);
        }

        this.iconFiles = validFiles;
        this.updateIconsUI(validFiles);
        
        if (validFiles.length > 0) {
            this.showAlert(`✅ ${validFiles.length} icono(s) cargado(s) correctamente`, 'success');
        }
    }

    validateImageFile(file) {
        const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/gif'];
        return validTypes.includes(file.type);
    }

    updateBackgroundUI(file) {
        const content = this.elements.backgroundUpload.querySelector('.file-upload-content');
        content.innerHTML = `
            <div class="file-upload-icon">✅</div>
            <p><strong>${file.name}</strong></p>
            <small>${this.formatFileSize(file.size)} - Imagen cargada</small>
        `;
    }

    updateIconsUI(files) {
        if (files.length === 0) {
            this.elements.iconsPreview.innerHTML = '';
            return;
        }

        const previewHTML = files.map((file, index) => `
            <div class="icon-preview" style="display: inline-block; margin: 5px; padding: 10px; background: #f1f5f9; border-radius: 8px;">
                <strong>Icono ${index + 1}:</strong> ${file.name}<br>
                <small>${this.formatFileSize(file.size)}</small>
            </div>
        `).join('');

        this.elements.iconsPreview.innerHTML = previewHTML;

        // Actualizar UI del upload
        const content = this.elements.iconsUpload.querySelector('.file-upload-content');
        content.innerHTML = `
            <div class="file-upload-icon">✅</div>
            <p><strong>${files.length} icono(s) seleccionado(s)</strong></p>
            <small>Haz clic para cambiar o añadir más</small>
        `;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async generateThumbnail() {
        if (this.isGenerating) return;

        // Validaciones
        if (!this.backgroundImage) {
            this.showAlert('Por favor, selecciona una imagen de fondo', 'error');
            return;
        }

        const title = this.elements.titleInput.value.trim();
        if (!title) {
            this.showAlert('Por favor, escribe un título para el thumbnail', 'error');
            return;
        }

        this.setGeneratingState(true);

        try {
            // Preparar datos para el backend serverless
            const backgroundBase64 = await this.imageToBase64(this.backgroundImage);
            
            // Convertir iconos a base64
            const iconsBase64 = [];
            for (const iconFile of this.iconFiles) {
                const iconBase64 = await this.imageToBase64(iconFile);
                iconsBase64.push(iconBase64);
            }

            // Llamar a la función serverless de Netlify
            const response = await fetch('/.netlify/functions/generate_thumbnail', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    background: backgroundBase64,
                    title: title,
                    icons: iconsBase64
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.success && result.thumbnail) {
                // Mostrar thumbnail generado en canvas
                await this.displayThumbnailFromBase64(result.thumbnail);
                
                // Mostrar vista previa
                this.elements.previewContainer.style.display = 'block';
                this.elements.previewContainer.scrollIntoView({ behavior: 'smooth' });
                
                this.showAlert('🎉 ¡Thumbnail generado exitosamente con backend Python!', 'success');

                // Google Analytics event (si está configurado)
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'thumbnail_generated', {
                        'event_category': 'engagement',
                        'event_label': 'serverless_success'
                    });
                }
            } else {
                throw new Error(result.error || 'Error desconocido generando thumbnail');
            }

        } catch (error) {
            console.error('Error generando thumbnail:', error);
            this.showAlert(`❌ Error: ${error.message}`, 'error');
        } finally {
            this.setGeneratingState(false);
        }
    }

    downloadThumbnail() {
        try {
            const title = this.elements.titleInput.value.trim();
            const filename = title ? 
                `${title.toLowerCase().replace(/[^a-z0-9]/g, '_')}_thumbnail.png` : 
                'thumbnail.png';

            this.generator.downloadThumbnail(filename);
            this.showAlert('📥 Descarga iniciada', 'success');

            // Google Analytics event
            if (typeof gtag !== 'undefined') {
                gtag('event', 'thumbnail_downloaded', {
                    'event_category': 'engagement',
                    'event_label': 'success'
                });
            }

        } catch (error) {
            console.error('Error descargando:', error);
            this.showAlert('Error al descargar el archivo', 'error');
        }
    }

    setGeneratingState(isGenerating) {
        this.isGenerating = isGenerating;
        this.elements.generateBtn.disabled = isGenerating;
        
        if (isGenerating) {
            this.elements.btnText.style.display = 'none';
            this.elements.btnLoading.style.display = 'inline-block';
        } else {
            this.elements.btnText.style.display = 'inline';
            this.elements.btnLoading.style.display = 'none';
        }
    }

    async imageToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    async displayThumbnailFromBase64(base64Data) {
        const canvas = this.elements.previewCanvas;
        const ctx = canvas.getContext('2d');
        
        // Crear imagen desde base64
        const img = new Image();
        
        return new Promise((resolve, reject) => {
            img.onload = () => {
                // Limpiar canvas
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Dibujar imagen generada por el backend Python
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                
                resolve();
            };
            
            img.onerror = reject;
            img.src = `data:image/png;base64,${base64Data}`;
        });
    }

    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        // Limpiar alertas anteriores
        this.elements.alerts.innerHTML = '';
        this.elements.alerts.appendChild(alertDiv);

        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);

        // Scroll a la alerta
        alertDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.thumbnailApp = new ThumbnailApp();
    
    console.log('🎨 Thumbnail Generator inicializado');
    
    // Google Analytics page view (si está configurado)
    if (typeof gtag !== 'undefined') {
        gtag('config', 'GA_MEASUREMENT_ID', {
            page_title: 'Thumbnail Generator',
            page_location: window.location.href
        });
    }
});
