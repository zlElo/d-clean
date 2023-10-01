import os
import shutil

def overwriter(selected_drive):
    print('[log] Write maximum of drive...')
    total, used, free = shutil.disk_usage(selected_drive)
    print(f'[log] Drive size: {total} bytes')
    
    # Größe der Datei in Bytes
    file_size = total

    # Pfad zur Datei
    file_path = f"{selected_drive}/file.bin"

    # Öffnen der Datei im Schreibmodus
    with open(file_path, "wb") as f:
        # Schleife zum Schreiben von Daten in die Datei
        while os.path.getsize(file_path) < file_size:
            # Schreiben von zufälligen Daten in die Datei
            f.write(os.urandom(1024))
