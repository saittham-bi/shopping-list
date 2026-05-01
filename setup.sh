#!/bin/bash
# ============================================================
# setup.sh – Erstkonfiguration auf Infomaniak Jelastic PaaS
# Einmal ausführen nach dem ersten Deployment
# ============================================================
set -e

echo "🔧 Installiere Abhängigkeiten..."
pip install -r requirements.txt

echo "📦 Sammle statische Dateien..."
python manage.py collectstatic --noinput

echo "🗄️  Führe Datenbankmigrationen durch..."
python manage.py migrate

echo "🏪 Lade Standardläden..."
python manage.py loaddata shopping/fixtures/initial_data.json

echo ""
echo "👤 Admin-Benutzer erstellen:"
python manage.py createsuperuser

echo ""
echo "✅ Setup abgeschlossen! Gunicorn starten mit:"
echo "   gunicorn einkaufsliste.wsgi:application --bind 0.0.0.0:8000"
