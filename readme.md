
# Factorio Server Updater

Ein automatisiertes Tool zum Aktualisieren von Factorio Servern.

## Features

- Automatische Erkennung der installierten Version
- Download der neuesten Factorio-Version 
- Backup der bestehenden Installation
- Update-Durchführung

## Installation

1. Python 3.6+ wird benötigt
2. Abhängigkeiten installieren:

pip install requests

## Verwendung
Es wird ein übergeordneter Ordner erwartet indem der factorio-Ordner liegt, in welchem die aktuelle Version gespeichert ist.

Ordnerstruktur:
- /pfad/zu/factorio
  - /factorio
  - /backups
  - /updater.py

# Updater mit Standard-Pfaden initialisieren
updater = FactorioUpdater()

# Oder mit benutzerdefinierten Pfaden
updater = FactorioUpdater(
    factorio_path="/pfad/zu/factorio",
    backup_path="/pfad/für/backups"
)

# Prüfe neueste Version
updater.check_latest_version()

# Aktuelle Version prüfen
current_version = updater.check_current_version()

# Optional: Backup erstellen
updater.backup_factorio()

# Neue Version herunterladen und entpacken
latest_version = updater.get_latest_version()
updater.extract_tarxz(latest_version, extracted_path)


## Entwickler

Entwickelt von [MicroMasterMinds]

## Lizenz

MIT License
