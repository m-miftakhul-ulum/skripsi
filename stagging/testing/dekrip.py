import os
from locust import HttpUser, TaskSet, task, between

# List semua file dekripsi gambar

path_key = 'keydekgambar'
path_dekgambar = 'dekgambar'
keydekgambar = os.listdir(path_key)
keydekgambar = [f for f in keydekgambar if os.path.isfile(os.path.join(path_key, f))]
dekgambar = os.listdir(path_dekgambar)
dekgambar = [f for f in dekgambar if os.path.isfile(os.path.join(path_dekgambar, f))]



path_deksuara = "deksuara"
deksuara = os.listdir(path_deksuara)
deksuara = [f for f in deksuara if os.path.isfile(os.path.join(path_deksuara, f))] 


class UserBehavior(TaskSet):


# dekripsi gambar
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
                response = self.client.post("/decrypt_image", files=data)
                print(f"Sent {dekrigambar}: {response.status_code}")
   
    @task
    def test_enkripsi_suara(self):
        for file in deksuara:
            file_path = os.path.join(path_deksuara, file)
            with open(file_path, 'rb') as f:
                response = self.client.post("/decrypt_audio", files={'input_text_file': f}, data={'user_key_plain': 1234567890123456})
                print(f"Sent {file_path}: {response.status_code}")    
    
            
    @task
    def wait(self):
        self.wait_time = between(1, 2)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)

    def on_start(self):
        self.client.base_url = "http://127.0.0.1:81"
   