import os
from locust import HttpUser, TaskSet, task, between

# Path untuk enkripsi gambar dan suara
path_enkripsi_gambar = 'enkgambar'
path_enkripsi_suara = 'enksuara'

# Path untuk dekripsi gambar dan suara
path_key = 'keydekgambar'
path_dekgambar = 'dekgambar'
path_deksuara = 'deksuara'

# List semua file dalam folder enkripsi
files_enkripsi_gambar = os.listdir(path_enkripsi_gambar)
files_enkripsi_gambar = [f for f in files_enkripsi_gambar if os.path.isfile(os.path.join(path_enkripsi_gambar, f))]

files_enkripsi_suara = os.listdir(path_enkripsi_suara)
files_enkripsi_suara = [f for f in files_enkripsi_suara if os.path.isfile(os.path.join(path_enkripsi_suara, f))]

# List semua file dalam folder dekripsi
keydekgambar = os.listdir(path_key)
keydekgambar = [f for f in keydekgambar if os.path.isfile(os.path.join(path_key, f))]

dekgambar = os.listdir(path_dekgambar)
dekgambar = [f for f in dekgambar if os.path.isfile(os.path.join(path_dekgambar, f))]

deksuara = os.listdir(path_deksuara)
deksuara = [f for f in deksuara if os.path.isfile(os.path.join(path_deksuara, f))] 


class UserBehavior(TaskSet):
    # Enkripsi gambar
    @task
    def upload_file(self):
        for file in files_enkripsi_gambar:
            file_path = os.path.join(path_enkripsi_gambar, file)
            with open(file_path, 'rb') as f:
                response = self.client.post("http://localhost:5000/enkripsi_gambar", files={'file': f})
                print(f"Sent {file_path}: {response.status_code}")

    # Enkripsi suara
    @task
    def test_enkripsi_suara(self):
        for file in files_enkripsi_suara:
            file_path = os.path.join(path_enkripsi_suara, file)
            with open(file_path, 'rb') as f:
                response = self.client.post("http://localhost:5002/encrypt_audio", files={'input_audio_file': f}, data={'user_key_plain': 1234567890123456})
                print(f"Sent {file_path}: {response.status_code}")    
    
    # Dekripsi gambar
    @task
    def dekrip(self):
        for file in range(len(dekgambar)):
            key = os.path.join(path_key, keydekgambar[file])
            dekrigambar = os.path.join(path_dekgambar, dekgambar[file])
           
            with open(dekrigambar, 'rb') as gam, open(key, 'rb') as f:
                data = {
                    "encrypted_image" : gam, 
                    "key_image" : f
                }
                response = self.client.post("http://localhost:5001/decrypt_image", files=data)
                print(f"Sent {dekrigambar}: {response.status_code}")
   
    # Dekripsi suara
    @task
    def test_dekripsi_suara(self):
        for file in deksuara:
            file_path = os.path.join(path_deksuara, file)
            with open(file_path, 'rb') as f:
                response = self.client.post("http://localhost:5003/decrypt_audio", files={'input_text_file': f}, data={'user_key_plain': 1234567890123456})
                print(f"Sent {file_path}: {response.status_code}")    
    
    @task
    def wait(self):
        self.wait_time = between(1, 2)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)

    def on_start(self):
        self.client.base_url = "http://127.0.0.1:5000/"
