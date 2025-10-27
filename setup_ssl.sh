#!/bin/bash
# Configuración SSL con Let's Encrypt
# Ejecutar después del despliegue básico

set -e

echo "🔒 CONFIGURACIÓN SSL CON LET'S ENCRYPT"
echo "====================================="

# Instalar certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado
read -p "Ingresa tu dominio (ej: thumbnail.midominio.com): " DOMAIN

if [ -n "$DOMAIN" ]; then
    sudo certbot --nginx -d $DOMAIN

    echo "✅ SSL configurado para: https://$DOMAIN"
    echo ""
    echo "🔄 Certbot renovará automáticamente los certificados"
    echo "📅 Verifica renovación: sudo certbot renew --dry-run"
else
    echo "⚠️  SSL no configurado. Tu sitio seguirá usando HTTP."
fi