import tkinter as tk
import numpy as np
import secrets
import time
import os
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from sympy import Matrix
from math import gcd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class HillCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enkripsi Dan Dekripsi Menggunakan Kunci Acak")
        self.root.state("zoomed")
        
        # Frame utama
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inisialisasi atribut
        self.image = None
        self.key_matrix = None
        self.key_image_path = None
        self.encrypted_image_path = None
        self.decrypted_image_path = None
        
        # Membuat folder jika belum ada
        self.create_key_folder()
        self.create_encryption_folder()
        self.create_decryption_folder()
        
        # Frame 1 Gambar input
        self.frame1 = ttk.Frame(self.main_frame)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.create_frame1_widgets()
        
        # Frame 2 Generate kunci acak
        self.frame2 = ttk.Frame(self.main_frame)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.create_frame2_widgets()

        # Frame 3 Hasil enkripsi
        self.frame3 = ttk.Frame(self.main_frame)
        self.frame3.grid(row=0, column=1, sticky="nsew")
        self.create_frame3_widgets()
        
        # Frame 4 Hasil dekripsi
        self.frame4 = ttk.Frame(self.main_frame)
        self.frame4.grid(row=1, column=1, sticky="nsew")
        self.create_frame4_widgets()
        
        # Set ukuran kolom dan baris
        self.main_frame.columnconfigure((0,1), weight=1)
        
    def create_key_folder(self):
        if not os.path.exists('kunci'):
            os.makedirs('kunci')
    
    def create_encryption_folder(self):
        if not os.path.exists('enkripsi'):
            os.makedirs('enkripsi')
            
    def create_decryption_folder(self):
        if not os.path.exists('dekripsi'):
            os.makedirs('dekripsi')
        
    def create_frame1_widgets(self):
        self.image_label = ttk.Label(self.frame1, text="Gambar")
        self.image_label.pack()

        self.frame11 = ttk.Frame(self.frame1)
        self.frame11.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame11, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image_button = ttk.Button(self.frame11, text="Pilih Gambar", command=self.load_image)
        self.image_button.pack(side=tk.LEFT)

        self.reset_button = ttk.Button(self.frame11, text="Reset", command=self.reset_all)
        self.reset_button.pack(side=tk.RIGHT)
        
    def create_frame2_widgets(self):
        self.key_label = ttk.Label(self.frame2, text="Kunci Acak")
        self.key_label.pack()
        
        self.frame22 = ttk.Frame(self.frame2)
        self.frame22.pack(fill=tk.BOTH, expand=True)

        self.key_figure = Figure(figsize=(2.5,2.5), dpi=100)
        self.key_canvas = FigureCanvasTkAgg(self.key_figure, master=self.frame22)
        self.key_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.generate_key_button = ttk.Button(self.frame22, text="Generate Kunci", command=self.generate_key)
        self.generate_key_button.pack(side=tk.LEFT)

        self.add_key_button = ttk.Button(self.frame22, text="Tambah Kunci", command=self.add_key)
        self.add_key_button.pack(side=tk.LEFT)

        self.reset_key_button = ttk.Button(self.frame22, text="Reset Kunci", command=self.reset_key)
        self.reset_key_button.pack(side=tk.LEFT)
        
    def create_frame3_widgets(self):
        self.encrypt_label = ttk.Label(self.frame3, text="Hasil Enkripsi")
        self.encrypt_label.pack()
        
        self.frame33 = ttk.Frame(self.frame3)
        self.frame33.pack(fill=tk.BOTH, expand=True)

        self.encrypted_canvas = tk.Canvas(self.frame33, background="white")
        self.encrypted_canvas.pack(fill=tk.BOTH, expand=True)

        self.encrypt_button = ttk.Button(self.frame33, text="Enkripsi", command=self.encrypt)
        self.encrypt_button.pack(side=tk.LEFT)

        self.encrypt_time_label = ttk.Label(self.frame33, text="Waktu Enkripsi:")
        self.encrypt_time_label.pack()
        
    def create_frame4_widgets(self):
        self.decrypt_label = ttk.Label(self.frame4, text="Hasil Dekripsi")
        self.decrypt_label.pack()

        self.frame44 = ttk.Frame(self.frame4)
        self.frame44.pack(fill=tk.BOTH, expand=True)

        self.decrypted_canvas = tk.Canvas(self.frame44, background="white")
        self.decrypted_canvas.pack(fill=tk.BOTH, expand=True)

        self.decrypt_button = ttk.Button(self.frame44, text="Dekripsi", command=self.decrypt)
        self.decrypt_button.pack(side=tk.LEFT)

        self.decrypt_time_label = ttk.Label(self.frame44, text="Waktu Dekripsi:")
        self.decrypt_time_label.pack()
        
    def reset_all(self):
        self.reset_key()
        self.reset_image()
        self.reset_time_labels()
        
    def reset_image(self):
        self.image = None
        self.canvas.delete("all")
        self.encrypted_canvas.delete("all")
        self.decrypted_canvas.delete("all")
        
    def reset_key(self):
        self.key_matrix = None
        self.key_figure.clf()
        self.key_canvas.draw()
        
    def reset_time_labels(self):
        self.encrypt_time_label.config(text="Waktu Enkripsi:")
        self.decrypt_time_label.config(text="Waktu Dekripsi:")
        
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if file_path:
            self.image = Image.open(file_path)
            self.show_image()

    def show_image(self):
        if self.image:
            self.canvas.delete("all")
            image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.image = image_tk
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width = image_tk.width()
            image_height = image_tk.height()
            x_center = (canvas_width - image_width) // 2
            y_center = (canvas_height - image_height) // 2
            self.canvas.create_image(x_center, y_center, anchor="nw", image=image_tk)


    def generate_key(self):
        if self.image is None:
            messagebox.showerror("Error", "Mohon pilih gambar terlebih dahulu!")
            return

        pixels = np.array(self.image)
        modulus = 256

        while True:
            # Tentukan panjang kunci dengan mengacak nilai dari 3 sampai 20
            key_length = secrets.randbelow(18) + 3
            # Cek kondisi jika hasil panjang kunci dapat membagi habis pixels.size
            if pixels.size % key_length == 0:
                # Jika berhasil, buat matriks acak sepanjang kunci
                key_matrix = [[secrets.randbelow(modulus) for _ in range(key_length)] for _ in range(key_length)]

                # Cek kondisi matriks, jika matriks memiliki invers lanjut
                if np.linalg.matrix_rank(key_matrix) == key_length:
                    sympy_matrix = Matrix(key_matrix)

                    # Cek kondisi matriks, jika matriks relatif prima dengan 256 lanjut
                    if gcd(int(sympy_matrix.det()), modulus) == 1:
                        # Cek kondisi, jika determinan matriks bernilai 1 lanjut
                        if np.linalg.det(key_matrix) != 0:
                            break  # Keluar dari loop jika kriteria terpenuhi

        self.key_matrix = np.array(key_matrix)

        # Menampilkan hasil kunci
        self.plot_key_matrix()

        # Simpan kunci sebagai gambar
        self.save_key_image()
        
    def add_key(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if file_path:
            key_image = Image.open(file_path)
            self.key_matrix = np.array(key_image)
            self.plot_key_matrix()
            self.save_key_image()
        
    def plot_key_matrix(self):
        ax = self.key_figure.add_subplot(111)
        ax.imshow(self.key_matrix, cmap='gray')
        ax.axis('off')
        self.key_canvas.draw()
        
    def save_key_image(self):
        key_image = Image.fromarray(self.key_matrix.astype('uint8'))
        filename = os.path.basename(self.image.filename)
        key_image_path = os.path.join('kunci', filename.split('.')[0] + '_key.png')
        key_image.save(key_image_path)
        print(f'Kunci Tersimpan Dalam Folder {key_image_path}')
        messagebox.showinfo("Sukses", f'Kunci Tersimpan Dalam Folder {key_image_path}')  # Notifikasi berhasil
        
    def encrypt(self):
        if self.image is None or self.key_matrix is None:
            messagebox.showerror("Error", "Mohon pilih gambar dan generate kunci terlebih dahulu!")
            return
        
        modulus = 256
        size = self.key_matrix.shape[0]
        
        start_time = time.time()
        
        encrypted_image_path = self.get_encrypted_image_path()
        
        pixels = np.array(self.image)
        flat_pixels = pixels.reshape(-1, size)
        encrypted_pixels = (flat_pixels.dot(self.key_matrix)) % modulus
        encrypted_image = encrypted_pixels.reshape(pixels.shape)
        Image.fromarray(np.uint8(encrypted_image)).save(encrypted_image_path)
        
        self.show_encrypted_image(encrypted_image)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Waktu Enkripsi Gambar: {elapsed_time:.2f} detik")
        print(f"Gambar Enkripsi Tersimpan Dalam Folder {encrypted_image_path}")
        self.encrypt_time_label.config(text=f"Waktu Enkripsi: {elapsed_time:.2f} detik")

        self.encrypted_image_path = encrypted_image_path
        messagebox.showinfo("Sukses", f"Gambar Enkripsi Tersimpan Dalam Folder {encrypted_image_path}")  # Notifikasi berhasil
        
    def get_encrypted_image_path(self):
        filename = os.path.basename(self.image.filename)
        return os.path.join('enkripsi', filename.split('.')[0] + '_encrypted.png')
        
    def show_encrypted_image(self, encrypted_image):
        self.encrypted_canvas.delete("all")
        image_tk = ImageTk.PhotoImage(Image.fromarray(np.uint8(encrypted_image)))
        self.encrypted_canvas.image = image_tk
        canvas_width = self.encrypted_canvas.winfo_width()
        canvas_height = self.encrypted_canvas.winfo_height()
        image_width = image_tk.width()
        image_height = image_tk.height()
        x_center = (canvas_width - image_width) // 2
        y_center = (canvas_height - image_height) // 2
        self.encrypted_canvas.create_image(x_center, y_center, anchor="nw", image=image_tk)
        
    def decrypt(self):
        if self.image is None or self.key_matrix is None or self.encrypted_image_path is None:
            messagebox.showerror("Error", "Mohon pilih gambar, generate kunci, dan enkripsi gambar terlebih dahulu!")
            return
        
        modulus = 256
        size = self.key_matrix.shape[0]
        
        start_time = time.time()
        
        key_matrix_inv = Matrix(self.key_matrix).inv_mod(modulus)
        
        encrypted_image = Image.open(self.encrypted_image_path)
        encrypted_pixels = np.array(encrypted_image)
        flat_encrypted_pixels = encrypted_pixels.reshape(-1, size)
        decrypted_pixels = (flat_encrypted_pixels.dot(key_matrix_inv)) % modulus
        decrypted_image = decrypted_pixels.reshape(encrypted_pixels.shape)
        
        decrypted_image_path = self.get_decrypted_image_path()
        Image.fromarray(np.uint8(decrypted_image)).save(decrypted_image_path)
        
        self.show_decrypted_image(decrypted_image)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Waktu Dekripsi Gambar: {elapsed_time:.2f} detik")
        print(f"Gambar Dekripsi Tersimpan Dalam Folder {decrypted_image_path}")
        self.decrypt_time_label.config(text=f"Waktu Dekripsi: {elapsed_time:.2f} detik")

        self.decrypted_image_path = decrypted_image_path
        messagebox.showinfo("Sukses", f"Gambar Dekripsi Tersimpan Dalam Folder {decrypted_image_path}")  # Notifikasi berhasil
        
    def get_decrypted_image_path(self):
        filename = os.path.basename(self.image.filename)
        return os.path.join('dekripsi', filename.split('.')[0] + '_decrypted.png')
        
    def show_decrypted_image(self, decrypted_image):
        self.decrypted_canvas.delete("all")
        image_tk = ImageTk.PhotoImage(Image.fromarray(np.uint8(decrypted_image)))
        self.decrypted_canvas.image = image_tk
        canvas_width = self.decrypted_canvas.winfo_width()
        canvas_height = self.decrypted_canvas.winfo_height()
        image_width = image_tk.width()
        image_height = image_tk.height()
        x_center = (canvas_width - image_width) // 2
        y_center = (canvas_height - image_height) // 2
        self.decrypted_canvas.create_image(x_center, y_center, anchor="nw", image=image_tk)

# Main program
root = tk.Tk()
app = HillCipherApp(root)
root.mainloop()