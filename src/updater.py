#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Factorio Server Updater
----------------------
Ein Automatisiertes Tool zum Aktualisieren von Factorio Servern

Entwickelt von: [MicroMasterMinds]
Version: 1.0.0
Erstellt am: 2024-11-11

Dieses Programm ermöglicht die automatische Aktualisierung
und initiale "Installierung" von Factorio-Servern

Funktionen:
- Automatische Erkennung der installierten Version
- Download der neuesten Factorio-Version
- Backup der bestehenden Installation
- Update-Durchführung
"""

__author__ = "[MicroMasterMinds]"
__version__ = "1.0.0"
__license__ = "MIT"

import os
import subprocess
import sys
import tarfile
import time
import re

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Installation of 'requests' package if not installed
try:
    import requests
except ImportError:
    install_package("requests")

# Configure the path to the Factorio installation
#factorio_path = "/Users/dominikkargl/Documents/05_Unternehmen/05_Projekte/99_Factorio"

class FactorioUpdater:
    def __init__(self, factorio_path:str="/opt/factorio", backup_path:str="/Backups"):
        self.factorio_path = factorio_path
        self.backup_path = backup_path
        self.factorio_filename = "factorio-headless_linux_latest.tar.xz"
        self.latest_version = None
        self.current_version = None       

    def check_current_version(self):
        try:
            # Führt den Befehl aus und fängt die Ausgabe ab
            result = subprocess.run(
                [f"{self.factorio_path}/factorio/bin/x64/factorio", "--version"],     # Der Befehl und seine Argumente
                capture_output=True,                     # Ausgabe abfangen
                text=True                                # Ausgabe als String
            )
            
            # Prüfen, ob der Befehl erfolgreich war
            if result.returncode == 0:
                # Rückgabe der Ausgabe
                return self.extract_version(result.stdout.strip())
            else:
                # Falls ein Fehler auftritt, die Fehlerausgabe anzeigen
                return f"ERROR: When executing the command: {result.stderr.strip()}"
                
        except FileNotFoundError:
            raise Exception("ERROR: Factorio installation not found.")
        except Exception as e:
            return f"ERROR: An unexpected error occurred: {e}"
        
    def extract_version(self, text):
        # Match version pattern at start of line
        pattern = r"Version: (\d+\.\d+\.\d+)"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None
        
    def check_latest_version(self):
        response = requests.get("https://factorio.com/api/latest-releases")
        if response.status_code == 200:
            data = response.json()
            self.latest_version = data["stable"]["headless"]  # Gibt die neueste stabile Version zurück
            self.factorio_filename = f"factorio-headless_linux_{self.latest_version}.tar.xz"
            return 0
        else:
            raise Exception("ERROR: Failed to fetch latest Factorio version.")
        
    def get_latest_version(self):
        save_path = os.path.join(self.factorio_path, self.factorio_filename)
        response = requests.get("https://factorio.com/get-download/stable/headless/linux64", stream=True)
        response.raise_for_status()
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Download and save the file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
    
        return save_path
    
    def extract_tarxz(self, archive_path, extract_path):
        with tarfile.open(archive_path, 'r:xz') as tar:
            tar.extractall(path=extract_path)

    def backup_factorio(self):
        # Erstelle den Backup-Pfad mit dem aktuellen Datum und Uhrzeit
        folder_name = f"{self.factorio_path}/factorio"
        output_file = os.path.join(f"{self.factorio_path}{self.backup_path}", time.strftime("%Y-%m-%d_%H-%M-%S.tar.xz"))

        # Wenn der Backup-Pfad nicht existiert, erstelle ihn
        if not os.path.exists(f"{self.factorio_path}{self.backup_path}"):
            os.makedirs(f"{self.factorio_path}{self.backup_path}")

        # Kopiere die Factorio-Installation in den Backup-Pfad
        with tarfile.open(output_file, "w:xz", preset=1) as tar:
            tar.add(folder_name)

def ask_backup():
    while True:
        response = input("Soll ein Backup erstellt werden? (j/n): ").lower()
        if response in ['j', 'ja']:
            return True
        if response in ['n', 'nein']:
            return False
        print("Bitte antworte mit 'j' oder 'n'")

# Beispielhafte Nutzung
updater = FactorioUpdater()
updater.check_latest_version()
print("Neueste Factorio Version:", updater.latest_version)

# Überprüfe die aktuell installierte Version
current_version = updater.check_current_version()
print("Installierte Factorio Version", current_version)

# Erstelle Backup
if ask_backup():
    print("Backup wird erstellt...")
    updater.backup_factorio()
else:
    print("Kein Backup gewünscht, fahre fort...")

# Beispielhafte Nutzung get_latest_version
print("Lade neueste Version herunter...")
latest_version = updater.get_latest_version()

# Entpacken der heruntergeladenen Datei
extracted_path = os.path.join(os.path.dirname(latest_version))
updater.extract_tarxz(latest_version, extracted_path)
