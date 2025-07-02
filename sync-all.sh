#!/bin/bash

set -e  # Detener en errores

echo "🧪 Configurando contexto Dev..."
./grafana-sync/config/dev-context.sh
echo "📥 Extrayendo dashboards Dev..."
grr pull -d grafana-sync/dashboards/dev

echo "🧪 Configurando contexto Replicate..."
./grafana-sync/config/replicate-context.sh
echo "📥 Extrayendo dashboards Replicate..."
grr pull -d grafana-sync/dashboards/replicate

echo "🔍 Comparando y sincronizando paneles modificados..."
python3 grafana-sync/sync_panels.py

echo "📤 Aplicando cambios a Replicate..."
grr apply grafana-sync/dashboards/replicate

echo "✅ Sincronización completa."