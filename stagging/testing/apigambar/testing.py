import os
import requests
import threading
import time

# URL target
url = "http://127.0.0.1:30000/enkripsi_gambar"

# Ganti dengan path folder yang ingin Anda daftarkan file-filenya
folder_path = '100 - 200'

# List semua file dalam folder
files = os.listdir(folder_path)
files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

# Function to send HTTP request
def send_request(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            print(f"Sent {file_path}: {response.status_code}")
    except Exception as e:
        print(f"Error sending {file_path}: {e}")

# Function to start multiple threads for sending requests
def start_attack():
    threads = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        thread = threading.Thread(target=send_request, args=(file_path,))
        threads.append(thread)
        thread.start()
        # time.sleep(0.1)  # Adjust the sleep time as needed
        time.sleep(1)  # Adjust the sleep time as needed

    for thread in threads:
        thread.join()

# Start the attack
start_attack()
