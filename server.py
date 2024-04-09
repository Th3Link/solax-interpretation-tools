from klein import run, route
import json
import os
from datetime import datetime, timedelta

# Pfad zur response.log Datei
log_file_path = os.path.expanduser('data/H3BC25XXXXXXXX/data.txt')

# Mapping von deutschen zu englischen Monatsnamen
month_translation = {
    "Jan": "Jan", "Feb": "Feb", "Mär": "Mar", "Apr": "Apr", "Mai": "May", "Jun": "Jun",
    "Jul": "Jul", "Aug": "Aug", "Sep": "Sep", "Okt": "Oct", "Nov": "Nov", "Dez": "Dec"
}

@route('/', methods=["POST", "GET"])
def home(request):
    closest_data = None
    smallest_diff = timedelta.max
    now = datetime.now()
    #now = datetime(now.year, now.month, now.day, 13, 15)
    with open(log_file_path, 'r') as file:
        for line in file:
            try:
                # Trennen des JSON-Objekts und der Zeitangabe
                json_part, time_part = line.rsplit('}', 1)
                json_part += '}'  # JSON-Objekt wiederherstellen
                
                # Parsen des JSON-Objekts
                json_data = json.loads(json_part)
                
                # Zeitangabe extrahieren und vorbereiten
                parts = time_part.strip().split(' ')
                time_part = ' '.join(parts[1:]).replace('.', '')
                time_part = ' '.join(time_part.split(' ')[:-2] + [time_part.split(' ')[-1]])
                
                for de, en in month_translation.items():
                    time_part = time_part.replace(de, en)
                
                time_format = "%d %b %H:%M:%S %Y"
                time_data = datetime.strptime(time_part, time_format)
                
                # Creating new datetime object with adjusted date
                adjusted_time_data = datetime(now.year, now.month, now.day, time_data.hour, time_data.minute)
                
                # Berechnung der Zeitdifferenz
                diff = abs(now - adjusted_time_data)
                
                if diff < smallest_diff:
                    smallest_diff = diff
                    closest_data = json_data
                
            except (json.decoder.JSONDecodeError, ValueError) as e:
                print(f"Fehler: {e}")
                continue
    
    if closest_data:
        # Entfernen des 'timestamp' Schlüssels, falls vorhanden
        closest_data.pop("timestamp", None)
        return json.dumps(closest_data).encode('utf-8')
    else:
        return json.dumps({"error": "No data found"}).encode('utf-8')

if __name__ == '__main__':
    run("0.0.0.0", 8080)
