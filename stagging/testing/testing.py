import os
from locust import HttpUser, TaskSet, task, between

# Ganti dengan path folder yang ingin Anda daftarkan file-filenya
path_enkripsi_gambar = 'enkgambar'
path_enkripsi_suara = 'enksuara'

# List semua file dalam folder
files = os.listdir(path_enkripsi_gambar)
files = [f for f in files if os.path.isfile(os.path.join(path_enkripsi_gambar, f))]


enksuara = os.listdir(path_enkripsi_suara)
enksuara = [f for f in enksuara if os.path.isfile(os.path.join(path_enkripsi_suara, f))]



class UserBehavior(TaskSet):
    
    # enkripsi gambar
    @task
    def upload_file(self):
        for file in files:
            file_path = os.path.join(path_enkripsi_gambar, file)
            with open(file_path, 'rb') as f:
                response = self.client.post("/enkripsi_gambar", files={'file': f})
                print(f"Sent {file_path}: {response.status_code}")

    @task
    def test_enkripsi_suara(self):
        for file in enksuara:
            file_path = os.path.join(path_enkripsi_suara, file)
            with open(file_path, 'rb') as f:
                response = self.client.post("/encrypt_audio", files={'input_audio_file': f}, data={'user_key_plain': 1234567890123456})
                print(f"Sent {file_path}: {response.status_code}")    
    
    
    @task
    def wait(self):
        self.wait_time = between(1, 2)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)

    def on_start(self):
        self.client.base_url = "http://127.0.0.1:81"
