import os
# from locust import HttpUser, TaskSet, task, between

# List semua file dekripsi gambar

path_key = 'keydekgambar'
path_dekgambar = 'dekgambar'


keydekgambar = os.listdir(path_key)
keydekgambar = [f for f in keydekgambar if os.path.isfile(os.path.join(path_key, f))]

dekgambar = os.listdir(path_dekgambar)
dekgambar = [f for f in dekgambar if os.path.isfile(os.path.join(path_dekgambar, f))]

for file in range(len(dekgambar)):            
    key = os.path.join(path_key, keydekgambar[file])
    dekrigambar = os.path.join(path_dekgambar, dekgambar[file])
    with open(key, 'rb') as f, open(dekrigambar, 'rb') as gam:
        print(key)