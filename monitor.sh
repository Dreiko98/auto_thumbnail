#!/bin/bash
# Script de monitoreo y mantenimiento
# Uso: ./monitor.sh

echo "📊 ESTADO DEL SERVICIO THUMBNAIL GENERATOR"
echo "==========================================="

# Estado del servicio
echo "🔧 Estado del servicio:"
sudo systemctl status thumbnail-generator --no-pager -l

echo ""
echo "🌐 Estado de Nginx:"
sudo systemctl status nginx --no-pager

echo ""
echo "📈 Uso de recursos:"
echo "CPU y Memoria:"
ps aux --no-headers -o pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -10

echo ""
echo "💾 Espacio en disco:"
df -h /home/germanmallo

echo ""
echo "📝 Últimas líneas de logs:"
echo "App logs:"
sudo journalctl -u thumbnail-generator -n 10 --no-pager

echo ""
echo "Nginx logs:"
sudo tail -10 /var/log/nginx/thumbnail_access.log

echo ""
echo "🔍 Health check:"
curl -s http://localhost/health || echo "❌ Health check falló"

echo ""
echo "🛠️  Comandos de mantenimiento:"
echo "   • Reiniciar app: sudo systemctl restart thumbnail-generator"
echo "   • Reiniciar nginx: sudo systemctl reload nginx"
echo "   • Ver logs completos: sudo journalctl -u thumbnail-generator -f"
echo "   • Limpiar logs: sudo journalctl --vacuum-time=7d"