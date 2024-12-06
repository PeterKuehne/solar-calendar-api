# Solar Calendar API

Ein FastAPI-basierter Microservice für die Verwaltung von Kalenderterminen für das Solar-Bot Projekt.

## Features

- Terminverfügbarkeit prüfen
- Termine erstellen
- Google Calendar Integration
- REST API Endpunkte

## Setup

1. Python-Umgebung erstellen:
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Umgebungsvariablen konfigurieren:
- Kopiere `.env.example` zu `.env`
- Füge deine Google Calendar Credentials ein

4. Server starten:
```bash
uvicorn app.main:app --reload
```

## API Endpunkte

- `GET /availability?datetime=ISO8601` - Prüft Verfügbarkeit eines Zeitslots
- `POST /appointments` - Erstellt einen neuen Termin
- `GET /appointments` - Listet alle Termine
- `DELETE /appointments/{id}` - Storniert einen Termin
