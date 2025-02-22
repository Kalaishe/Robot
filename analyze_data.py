import sqlite3
import json
from datetime import datetime
from collections import Counter
import re

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('rasa.db')

# Daten aus der Tabelle "events" extrahieren
query = "SELECT sender_id, type_name, timestamp, intent_name, action_name, data FROM events"
cursor = conn.cursor()
cursor.execute(query)
events = cursor.fetchall()

# Verbindung schließen
conn.close()

def format_timestamp(unix_timestamp):
    """Unix-Timestamp in lesbares Datum-Zeit-Format umwandeln."""
    return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def shorten_sender_id(sender_id):
    """Verkürzen der sender_id auf die ersten 8 Zeichen."""
    return sender_id[:8]

def format_event(event):
    """Formatiert Ereignisse und extrahiert den Text."""
    sender_id, type_name, timestamp, intent_name, action_name, data = event

    try:
        parsed_data = json.loads(data)
    except json.JSONDecodeError:
        parsed_data = {}

    formatted_time = format_timestamp(timestamp)
    short_sender_id = shorten_sender_id(sender_id)

    if type_name == 'user':
        text = parsed_data.get('text', '[No text]')
        return f"User ({short_sender_id}) at {formatted_time}: {text}", text, timestamp
    elif type_name == 'bot':
        text = parsed_data.get('text', '[No text]')
        return f"Bot at {formatted_time}: {text}", None, timestamp
    else:
        return None, None, None

def analyze_text(text):
    """Berechnet Satzlänge, Wortanzahl und Zeichenanzahl."""
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)  # Satztrennung
    num_sentences = len(sentences)
    num_words = len(re.findall(r'\b\w+\b', text))
    num_characters = len(text)
    
    return num_sentences, num_words, num_characters

def calculate_type_token_ratio(words):
    """Berechnet das Type-Token-Ratio (TTR)."""
    unique_words = set(words)
    num_unique_words = len(unique_words)
    num_total_words = len(words)
    
    return num_unique_words / num_total_words if num_total_words > 0 else 0

# Ereignisse formatieren und sammeln
formatted_events = []
user_texts = []
user_data = {}

for event in events:
    formatted_event, user_text, timestamp = format_event(event)
    if formatted_event is not None:
        formatted_events.append(formatted_event)
        if user_text is not None:
            user_texts.append(user_text)
            sender_id = shorten_sender_id(event[0])
            if sender_id not in user_data:
                user_data[sender_id] = {
                    'texts': [],
                    'num_sentences': 0,
                    'num_words': 0,
                    'num_characters': 0,
                    'turns': 0,  # Anzahl der Turns für jeden Benutzer
                    'timestamps': []
                }
            user_data[sender_id]['texts'].append(user_text)
            user_data[sender_id]['turns'] += 1  # Turn für diesen Benutzer erhöhen
            user_data[sender_id]['timestamps'].append(timestamp)
            s, w, c = analyze_text(user_text)
            user_data[sender_id]['num_sentences'] += s
            user_data[sender_id]['num_words'] += w
            user_data[sender_id]['num_characters'] += c

# Ergebnisse für jeden Benutzer speichern (inklusive Texte und Zeiten)
for user_id, data in user_data.items():
    all_texts = ' '.join(data['texts']).lower()  # Alle Texte des Benutzers zu einem String zusammenfügen
    words = re.findall(r'\b\w+\b', all_texts)  # Wörter extrahieren
    word_counter = Counter(words)  # Häufigkeit der Wörter zählen
    ttr = calculate_type_token_ratio(words)

    # Berechnung der Zeiten
    start_time = min(data['timestamps'])
    end_time = max(data['timestamps'])
    time_taken = (datetime.fromtimestamp(end_time) - datetime.fromtimestamp(start_time)).total_seconds()

    # Durchschnittliche Satzlänge und Wortlänge berechnen
    avg_sentence_length = data['num_words'] / data['num_sentences'] if data['num_sentences'] > 0 else 0
    avg_word_length = data['num_characters'] / data['num_words'] if data['num_words'] > 0 else 0

    # Ergebnisse in eine Textdatei speichern
    results_filename = f'text_analysis_results_{user_id}.txt'
    with open(results_filename, 'w', encoding='utf-8') as file:
        # Benutzertexte hinzufügen
        file.write(f"Texte des Benutzers {user_id}:\n")
        for text in data['texts']:
            file.write(f"{text}\n")
        
        file.write("\nHäufigkeit der Wörter:\n")
        for word, frequency in word_counter.items():
            file.write(f"{word}: {frequency}\n")
    
        # Satzlänge, Wortanzahl, Zeichenanzahl und Turns
        file.write(f"\nGesamtanzahl der Sätze: {data['num_sentences']}\n")
        file.write(f"Gesamtanzahl der Wörter: {data['num_words']}\n")
        file.write(f"Gesamtanzahl der Zeichen: {data['num_characters']}\n")
        file.write(f"Gesamtanzahl der Turns: {data['turns']}\n")  # Anzahl der Turns hinzufügen
    
        # Type-Token-Ratio (TTR)
        file.write(f"Type-Token-Ratio (TTR): {ttr:.4f}\n")
        # Zeit für die Aufgabe
        file.write(f"Gesamtzeit für die Aufgabe (in Sekunden): {time_taken:.2f}\n")
        # Durchschnittliche Satzlänge und Wortlänge
        file.write(f"Durchschnittliche Satzlänge: {avg_sentence_length:.2f}\n")
        file.write(f"Durchschnittliche Wortlänge: {avg_word_length:.2f}\n")

    print(f"Ergebnisse für Benutzer {user_id} wurden in '{results_filename}' gespeichert.")

# Häufigkeit der Wörter analysieren
all_user_texts = ' '.join(user_texts).lower()  # Alle Nutzertexte zu einem String zusammenfügen
words = re.findall(r'\b\w+\b', all_user_texts)  # Wörter extrahieren
word_counter = Counter(words)  # Häufigkeit der Wörter zählen

# Satzlänge, Wortanzahl und Zeichenanzahl berechnen
num_sentences, num_words, num_characters = 0, 0, 0
total_turns = 0  # Gesamtanzahl der Turns für alle Benutzer

for text in user_texts:
    s, w, c = analyze_text(text)
    num_sentences += s
    num_words += w
    num_characters += c
    total_turns += 1  # Zählt alle Turns

# Gesamtzeit für die Aufgabe berechnen (kumuliert für alle Benutzer)
total_time_for_task = sum(
    (datetime.fromtimestamp(max(data['timestamps'])) - datetime.fromtimestamp(min(data['timestamps']))).total_seconds() 
    for data in user_data.values() if len(data['timestamps']) > 1
)

# Durchschnittliche Satzlänge und Wortlänge berechnen
avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
avg_word_length = num_characters / num_words if num_words > 0 else 0

# Type-Token-Ratio (TTR) für alle Benutzer berechnen
all_words = []
for user_id, data in user_data.items():
    all_words.extend(re.findall(r'\b\w+\b', ' '.join(data['texts']).lower()))
    
total_ttr = calculate_type_token_ratio(all_words)

# Zusammenfassung der Ergebnisse ausgeben
print("Chatprotokoll:")
for event in formatted_events:
    print(event)

print("\nHäufigkeit der Wörter:")
for word, frequency in word_counter.items():
    print(f"{word}: {frequency}")

print(f"\nGesamtanzahl der Sätze: {num_sentences}")
print(f"Gesamtanzahl der Wörter: {num_words}")
print(f"Gesamtanzahl der Zeichen: {num_characters}")
print(f"Gesamtanzahl der Turns: {total_turns}")  # Gesamtanzahl der Turns ausgeben
print(f"Gesamtzeit für die Aufgabe (in Sekunden): {total_time_for_task:.2f}")
print(f"Durchschnittliche Satzlänge: {avg_sentence_length:.2f}")
print(f"Durchschnittliche Wortlänge: {avg_word_length:.2f}")
print(f"Gesamt-Type-Token-Ratio (TTR) für alle Benutzer: {total_ttr:.4f}")

# Ergebnisse in eine Zusammenfassungsdatei speichern
results_filename = 'text_analysis_results_summary.txt'
with open(results_filename, 'w', encoding='utf-8') as file:
    # Zusammenfassung der Texte und Häufigkeiten
    file.write("Chatprotokoll:\n")
    for event in formatted_events:
        file.write(f"{event}\n")

    file.write("\nHäufigkeit der Wörter:\n")
    for word, frequency in word_counter.items():
        file.write(f"{word}: {frequency}\n")

    # Gesamtstatistiken
    file.write(f"\nGesamtanzahl der Sätze: {num_sentences}\n")
    file.write(f"Gesamtanzahl der Wörter: {num_words}\n")
    file.write(f"Gesamtanzahl der Zeichen: {num_characters}\n")
    file.write(f"Gesamtanzahl der Turns: {total_turns}\n")  # Gesamtanzahl der Turns hinzufügen
    file.write(f"Gesamtzeit für die Aufgabe (in Sekunden): {total_time_for_task:.2f}\n")
    
    # Durchschnittliche Satzlänge und Wortlänge
    file.write(f"Durchschnittliche Satzlänge: {avg_sentence_length:.2f}\n")
    file.write(f"Durchschnittliche Wortlänge: {avg_word_length:.2f}\n")
    
    # Type-Token-Ratio (TTR)
    file.write(f"Gesamt-Type-Token-Ratio (TTR) für alle Benutzer: {total_ttr:.4f}\n")

print(f"\nZusammenfassung der Ergebnisse wurde in '{results_filename}' gespeichert.")
