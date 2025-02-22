Die Lizenz CC BY-SA 4.0 erlaubt die Weiterverwendung, Bearbeitung und Weitergabe des Inhalts unter der Bedingung, dass die ursprüngliche Autorin genannt wird und das neue Material unter derselben Lizenz veröffentlicht wird.

Für eine Basiseinführung in Rasa Open Source Chatbot ist ein kostenloser Kurs von Prof. Dr. Irene Weber verfügbar. Ursprünglich auf der Plattform KI-Campus veröffentlicht (https://ki-campus.org/), ist er nun unter folgendem Link abrufbar:
https://lms.futureskills-sh.de/blocks/ildmetaselect/detailpage.php?id=135

Die offizielle Dokumentation von Rasa Open Source ist hier einsehbar:
https://rasa.com/docs/rasa/

Der ursprünglich im Kurs verwendete Chatroom-Container wurde ebenfalls von Irene Weber bereitgestellt, allerdings später geändert. Der Originalcode ist auf GitHub abrufbar:
https://github.com/weberi/aicampus-chatbot-course

Die Bilder und Videos wurden mit Kling AI https://klingai.com/ generiert und anschließend auf YouTube hochgeladen (https://www.youtube.com/) sowie auf Imgur geteilt (https://imgur.com/). Der gesamte Prozess wurde in einem HTML-basierten Chatroom gespeichert.

# Rasa Chatbot lokal mit Datenanalyse

## 🤖 Projektübersicht
Dieses Projekt beinhaltet einen Chatbot, der mit [Rasa](https://rasa.com/) entwickelt wurde, sowie ein Python-Skript zur Analyse der Chat-Daten. Ziel der Analyse ist es, zu untersuchen, wie verschiedene Chatbot-Designs die Interaktion der Nutzer beeinflussen.

## ⚙️ Anforderungen
Bevor das Projekt ausgeführt werden kann, sollten die folgenden Voraussetzungen erfüllt sein:
- **Python** 3.8 bis 3.10 (Empfohlen: 3.9.10)
- **pip** (Python Paket-Manager)
- **Virtuelle Umgebung** (optional, aber empfohlen)
- Folgende Python-Bibliotheken:
  - Rasa
  - Pandas
  - Matplotlib

## 🛠️ Installation
### 1. Repository klonen
Klonen Sie das Repository auf Ihren lokalen Rechner:
```sh
 git clone https://github.com/Kalaishe/Robot.git
 cd Robot
```

### 2. Virtuelle Umgebung erstellen und aktivieren
Erstellen und aktivieren Sie eine virtuelle Umgebung, um Abhängigkeiten isoliert zu verwalten:
```sh
 python -m venv Hbot_env  # Erstellen der virtuellen Umgebung
```

**Windows:**
```sh
 Hbot_env\Scripts\activate
```

**Linux/macOS:**
```sh
 source Hbot_env/bin/activate
```

### 3. Abhängigkeiten installieren
Installieren Sie die erforderlichen Pakete:
```sh
 pip install -r requirements.txt
```

## 🔧 Rasa Chatbot ausführen
### 1. Rasa-Modell trainieren
Bevor der Chatbot gestartet wird, muss das Modell trainiert werden:
```sh
 rasa train
```

### 2. Chatbot starten
Der Rasa-Server kann mit folgendem Befehl gestartet werden:
```sh
 rasa run --port 5005 --enable-api --cors "*"
```
Dadurch wird der Chatbot unter `http://localhost:5005` erreichbar sein.

### 3. HTML-Chatroom öffnen
Der Chatbot kann über eine HTML-Seite verwendet werden. Einfach die entsprechende Datei im Browser öffnen.

## 📝 Datenanalyse
Die Chat-Daten werden lokal in einer SQLite-Datenbank gespeichert.
**Wichtige Konfigurationsdatei:** `endpoints.yml`
```yaml
tracker_store:
  type: sql
  dialect: "sqlite"
  database: "rasa.db"  # Lokale Speicherung der Chat-Daten
```

### 1. Daten auswerten
Python-Skript analysiert die gespeicherten Daten und erstellt Chatprotokolle:
```sh
 python analyze_data.py
```

## ✨ Weitere Informationen
- Rasa-Dokumentation: [Installation & Setup](https://rasa.com/docs/rasa/installation/environment-set-up)
- SQLite-Datenbank: [SQLite Docs](https://www.sqlite.org/docs.html)



---
Falls Fragen oder Probleme auftreten, bitte ein Issue im Repository erstellen.

