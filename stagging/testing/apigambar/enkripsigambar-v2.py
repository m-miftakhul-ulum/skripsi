import os
from locust import HttpUser, TaskSet, task, between

# Ganti dengan path folder yang ingin Anda daftarkan file-filenya
folder_path = '100 - 200'

# List semua file dalam folder
files = os.listdir(folder_path)
files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

class UserBehavior(TaskSet):
    @task
    def upload_file(self):
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'rb') as f:
                response = self.client.post("/enkripsi_gambar", files={'file': f})
                print(f"Sent {file_path}: {response.status_code}")
                
    @task
    def wait(self):
        self.wait_time = between(1, 2)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)

    def on_start(self):
        self.client.base_url = "http://127.0.0.1:30000"
