# 🤖 Workflow de Generación de IA

## Flujo de Usuario Completo

### 1. **Iniciar Sesión / Registrarse**
- El usuario debe tener una cuenta para usar la funcionalidad de IA
- Botones visibles en la barra superior

### 2. **Configurar Token de OpenAI**
- Hacer clic en "⚙️ Configurar Token IA"
- Pegar el token de OpenAI desde: https://platform.openai.com/api-keys
- El badge cambiará a "✓ Token IA activo"
- **La sección de IA solo aparece cuando hay token configurado**

### 3. **Generar Imagen de Fondo con IA**

#### Paso 1: Describir el Post
```
Ejemplo: "Tutorial de programación en Python, fondo tecnológico 
con código, colores azules y morados, estilo moderno"
```

#### Paso 2: Hacer clic en "🤖 Generar con IA"
- Tiempo de espera: 10-30 segundos
- Se muestra un spinner de carga con mensaje

#### Paso 3: Ver Preview
- La imagen aparece en un preview debajo del botón
- **NO se asigna automáticamente al formulario**

#### Paso 4: Decidir qué hacer con la imagen
Tres opciones:

**A) ✓ Usar esta imagen**
- Asigna la imagen al campo "Imagen de fondo" del formulario
- Puedes continuar llenando el resto del formulario normalmente
- La imagen se ve reflejada en "background_info"

**B) 📥 Descargar**
- Descarga la imagen a tu computadora
- Útil si quieres guardarla para uso futuro
- La imagen NO se asigna al formulario automáticamente

**C) 🔄 Regenerar**
- Genera una nueva versión con el mismo prompt
- Útil si no te gusta el resultado
- Crea una imagen completamente nueva

### 4. **Continuar con el Formulario**
- Si usaste la imagen de IA, ya tienes el fondo listo
- Completa los demás campos (texto, iconos, etc.)
- Haz clic en "✨ Generar Miniatura"

---

## 🔧 Detalles Técnicos

### Backend (Python)

#### Rutas de API
```python
POST /generate_ai_background
- Requiere: @login_required
- Body: { "description": "texto del prompt" }
- Respuesta: { "filename": "uuid.png", "preview_base64": "..." }

POST /generate_ai_icon
- Requiere: @login_required
- Body: { "description": "...", "icon_number": 1 }
- Respuesta: { "filename": "uuid.png", "preview_base64": "...", "icon_number": 1 }
```

#### Generación de Imágenes
```python
# ai_generator.py
- DALL-E 3 (model: "dall-e-3")
- Fondo: 1792x1024 → resize a 1920x1080
- Icono: 1024x1024 con fondo transparente
- Timeout: 60 segundos
- Guardado en: .uploads/
```

### Frontend (JavaScript)

#### Funciones Principales

**generateAiBackground()**
```javascript
- Valida que hay prompt
- Muestra loading
- POST /generate_ai_background
- Guarda en aiGeneratedImage = { filename, preview, prompt }
- Muestra preview
```

**useAiImage()**
```javascript
- Convierte base64 → blob → File
- Asigna a uploadedFiles.background
- Actualiza background_info
- Oculta label de upload
- Scroll al formulario
```

**downloadAiImage()**
```javascript
- Crea blob desde base64
- Crea elemento <a> temporal
- Trigger download
- Limpia objeto URL
```

**regenerateAiImage()**
```javascript
- Confirma con usuario
- Llama generateAiBackground() de nuevo
- Usa el mismo prompt guardado
```

#### Control de Visibilidad
```javascript
// Mostrar/ocultar sección IA
if (user.has_openai_token) {
    ai_section.style.display = 'block';
} else {
    ai_section.style.display = 'none';
}
```

---

## 📋 Estructura de Datos

### Base de Datos (SQLite)

#### Tabla `users`
```sql
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- password_hash (TEXT)
- salt (TEXT)
- openai_token (TEXT) -- Token de API de OpenAI
- created_at (TIMESTAMP)
- last_login (TIMESTAMP)
```

#### Tabla `sessions`
```sql
- session_id (TEXT PRIMARY KEY)
- user_id (INTEGER FOREIGN KEY)
- created_at (TIMESTAMP)
- expires_at (TIMESTAMP)
```

### Estado del Cliente (JavaScript)

```javascript
let currentUser = {
    id: 123,
    username: "usuario",
    has_openai_token: true
};

let aiGeneratedImage = {
    filename: "uuid-timestamp.png",
    preview: "base64_encoded_string",
    prompt: "descripción usada"
};

let uploadedFiles = {
    background: File,  // ← Aquí se asigna con useAiImage()
    icons: [],
    person_photo: null,
    icon1_template3: null,
    icon2_template3: null
};
```

---

## 🎨 Prompts Optimizados

### Fondo (1920x1080)
```
"Create a professional stock photo background image for {description}. 
Style: Clean, modern, high-quality stock photography. 
Composition: Landscape orientation, leave negative space for text overlay. 
Colors: Vibrant but professional. 
Size: 1920x1080 pixels. 
NO text, NO logos, NO watermarks."
```

### Icono (1024x1024)
```
"Create a minimalist icon for {description}. 
Style: Simple, clean, professional. 
CRITICAL: TRANSPARENT BACKGROUND (PNG format with alpha channel). 
Design: Centered subject, bold colors, scalable. 
Size: 1024x1024 pixels. 
NO text, NO background, TRANSPARENT ONLY."
```

---

## ⚠️ Consideraciones Importantes

### Transparencia en Iconos
- Los iconos **DEBEN** tener fondo transparente
- El prompt enfatiza: "TRANSPARENT BACKGROUND (PNG format with alpha channel)"
- DALL-E 3 a veces ignora esto, puede requerir regeneración

### Tiempos de Espera
- Generación normal: 10-20 segundos
- Con tráfico alto: hasta 30 segundos
- Timeout del servidor: 60 segundos

### Límites de OpenAI
- Costo: ~$0.04 por imagen (dall-e-3, standard quality)
- Rate limit: Depende del plan del usuario
- Errores comunes: Token inválido, límite excedido, contenido no permitido

### Seguridad
- Token **NUNCA** se envía al frontend
- Guardado con `text NOT NULL DEFAULT ''`
- Usuario puede remover token dejando campo vacío

---

## 🧪 Testing Local

### 1. Inicializar Base de Datos
```bash
python3 init_db.py
```

### 2. Instalar Dependencias
```bash
pip3 install -r requirements.txt
```

### 3. Ejecutar Servidor
```bash
python3 web_app.py
```

### 4. Probar Workflow
1. Abrir http://localhost:5000
2. Registrar usuario
3. Configurar token OpenAI válido
4. Seleccionar plantilla
5. Escribir prompt en sección IA
6. Generar imagen (esperar 10-30s)
7. Verificar preview aparece
8. Hacer clic en "Usar esta imagen"
9. Verificar que background_info muestra el archivo
10. Completar formulario y generar miniatura
11. Verificar que thumbnail usa imagen de IA

---

## 🐛 Troubleshooting

### "No hay imagen generada para usar"
- Genera la imagen primero con el botón "Generar con IA"
- Espera a que aparezca el preview

### "Error al generar imagen con IA"
- Verifica que el token OpenAI sea válido
- Verifica que tengas créditos en tu cuenta OpenAI
- Revisa la consola del servidor para errores específicos

### La sección de IA no aparece
- Verifica que estés logueado
- Configura un token OpenAI válido
- El badge debe decir "✓ Token IA activo"

### La imagen no tiene fondo transparente (iconos)
- Es un problema conocido de DALL-E 3
- Solución: Hacer clic en "🔄 Regenerar" hasta obtener transparencia
- O usar herramienta externa para remover fondo

### Timeout al generar
- Es normal si OpenAI tiene tráfico alto
- Intenta de nuevo
- El servidor tiene timeout de 60 segundos

---

## 📦 Deployment

### Actualizar Dockerfile
```dockerfile
# Agregar dependencias
RUN pip install --no-cache-dir openai>=1.0.0 bcrypt>=4.0.0

# Copiar archivos nuevos
COPY database.py .
COPY ai_generator.py .
COPY init_db.py .

# Inicializar DB
RUN python3 init_db.py
```

### Variables de Entorno (Opcional)
```bash
# No necesarias, tokens guardados en DB
# Pero útil para configuración global
OPENAI_DEFAULT_MODEL=dall-e-3
OPENAI_TIMEOUT=60
```

### Persistencia de Datos
```yaml
# docker-compose.yml
volumes:
  - ./thumbnail_users.db:/app/thumbnail_users.db
  - ./.uploads:/app/.uploads
```

---

## 📚 Referencias

- [OpenAI DALL-E 3 Docs](https://platform.openai.com/docs/guides/images)
- [Flask Sessions](https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions)
- [Pillow Image Library](https://pillow.readthedocs.io/)
