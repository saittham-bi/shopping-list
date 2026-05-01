# 🛒 Einkaufsliste

Eine Django Web-App zur Verwaltung von Einkaufslisten – optimiert für Infomaniak Jelastic PaaS.

## Features

- ✅ Einkaufsartikel mit Laden-Zuweisung verwalten
- 🏪 Offene Einkäufe nach Laden gruppiert (Default: «Egal»)
- ☑️ Artikel als gekauft/offen markieren
- 📋 Gekaufte Artikel separat auflisten
- 🔐 Login-Pflicht (Session Cookie persistiert 30 Tage)
- 👤 Nur Admin kann Benutzer erstellen
- 🔑 Benutzer können ihr Passwort selbst ändern
- 🛠 Django Admin-Interface unter `/admin/`

## Projektstruktur

```
einkaufsliste/
├── einkaufsliste/          # Django-Projektkonfiguration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shopping/               # Haupt-App
│   ├── models.py           # Laden, Einkauf
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── fixtures/
│       └── initial_data.json   # Standardläden (CH)
├── templates/
│   ├── base.html
│   ├── registration/       # Login, Passwort
│   └── shopping/           # App-Templates
├── requirements.txt
├── manage.py
├── Procfile                # Gunicorn für Jelastic
├── setup.sh                # Erstkonfiguration
└── .env.example
```

## Modelle

### `Laden`
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| name | CharField | Name des Ladens (eindeutig) |
| reihenfolge | PositiveIntegerField | Sortierreihenfolge |

### `Einkauf`
| Feld | Typ | Beschreibung |
|------|-----|--------------|
| artikel | CharField | Name des Artikels |
| gekauft | BooleanField | Kaufstatus (True/False) |
| laden | ForeignKey → Laden | Ziel-Laden (optional, «Egal») |
| geaendert | DateTimeField | Automatisch bei Änderung |
| erstellt | DateTimeField | Automatisch beim Erstellen |
| erstellt_von | ForeignKey → User | Ersteller |

---

## Deployment auf Infomaniak Jelastic PaaS

### 1. Jelastic-Umgebung erstellen

1. Im Jelastic-Dashboard: **Create Environment**
2. **Python** als Application Server wählen (z. B. Python 3.11)
3. Optional: **PostgreSQL** als Datenbankknoten hinzufügen
4. Umgebungsname vergeben und erstellen

### 2. Code deployen

**Option A – Git (empfohlen):**
```bash
# Im Jelastic Dashboard unter Deployment Manager
# Repository-URL eintragen und deployen
```

**Option B – ZIP-Upload:**
```bash
# Projektordner zippen
zip -r einkaufsliste.zip einkaufsliste/
# Im Jelastic Dashboard hochladen
```

### 3. Umgebungsvariablen setzen

Im Jelastic Dashboard → **Config** → **Variables**:

```
DJANGO_SECRET_KEY=<langer-zufaelliger-string>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<deine-domain>.hidora.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=einkaufsliste
DB_USER=<db-user>
DB_PASSWORD=<db-passwort>
DB_HOST=<db-host-von-jelastic>
DB_PORT=5432
```

**Secret Key generieren:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Erstkonfiguration (einmalig)

Via SSH im Jelastic-Terminal oder Web-SSH:
```bash
cd /var/www/webroot/ROOT
bash setup.sh
```

Das Skript führt folgende Schritte aus:
- `pip install -r requirements.txt`
- `python manage.py collectstatic --noinput`
- `python manage.py migrate`
- `python manage.py loaddata shopping/fixtures/initial_data.json`
- `python manage.py createsuperuser` (interaktiv)

### 5. Gunicorn starten

Jelastic startet Gunicorn automatisch über den `Procfile`:
```
web: gunicorn einkaufsliste.wsgi:application --bind 0.0.0.0:8000 --workers 2
```

Oder manuell:
```bash
gunicorn einkaufsliste.wsgi:application --bind 0.0.0.0:8000 --workers 2 --daemon
```

---

## Lokale Entwicklung

```bash
# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Umgebungsvariablen setzen (oder .env mit python-dotenv)
export DJANGO_DEBUG=True
export DJANGO_SECRET_KEY=dev-secret-key

# Datenbank initialisieren
python manage.py migrate
python manage.py loaddata shopping/fixtures/initial_data.json
python manage.py createsuperuser

# Server starten
python manage.py runserver
```

App läuft auf: http://127.0.0.1:8000

---

## Benutzerverwaltung

- **Admin-URL:** `/admin/`
- Nur der Admin (Staff/Superuser) kann Benutzer erstellen
- Benutzer können ihr eigenes Passwort unter `/password-change/` ändern
- Session-Cookie bleibt **30 Tage** aktiv (konfigurierbar in `settings.py`)

## Standard-Läden (Schweiz)

Die Fixture lädt diese Läden automatisch:
- Migros
- Coop  
- Aldi
- Lidl
- Denner

Weitere Läden können im Admin-Interface verwaltet werden.
