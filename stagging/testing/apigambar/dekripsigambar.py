from locust import HttpUser, TaskSet, task, between
import os

class UserBehavior(TaskSet):
    @task(1)
    def load_test(self):
        # Path to the 'dekripsi' folder
        dekripsi_folder = os.path.join(os.path.expanduser("~"), "dekripsi")
        
        encrypted_image_path = os.path.join(dekripsi_folder, "axanopmw_encrypted.png")
        key_image_path = os.path.join(dekripsi_folder, "axanopmw_key.png")
        
        files = {
            'encrypted_image': ('axanopmw_encrypted.png', open(encrypted_image_path, 'rb')),
            'key_image': ('axanopmw_key.png', open(key_image_path, 'rb'))
        }
        
        self.client.post("/upload", files=files)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)


# steps
# locust -f locustfile.py --host=http://yourtargetwebsite.com
# sudo apt-get install wrk
# wrk -t12 -c400 -d30s http://yourtargetwebsite.com
