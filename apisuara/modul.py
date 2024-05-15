import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pydub import AudioSegment
import os
import time
import string
import random

# Fungsi Shift Cipher 13
def shift_cipher_13(text):
    shifted_text = ""
    for char in text:
        if 'A' <= char <= 'Z':
            shifted_char = chr(((ord(char) - ord('A') + 13) % 26) + ord('A'))
        elif 'a' <= char <= 'z':
            shifted_char = chr(((ord(char) - ord('a') + 13) % 26) + ord('a'))
        else:
            shifted_char = char
        shifted_text += shifted_char
    return shifted_text

# Fungsi untuk mengenkripsi dan menyimpan data audio dalam file teks
def encrypt_audio_to_txt(input_file, output_file, aes_key):
    iv = os.urandom(AES.block_size)  # Generate IV
    with open(input_file, 'rb') as audio_file:
        audio_data = audio_file.read()

    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)  # Menggunakan IV dalam mode CBC
    encrypted_audio = iv + cipher.encrypt(pad(audio_data, AES.block_size))

    with open(output_file, 'wb') as txt_file:
        txt_file.write(encrypted_audio)

# Fungsi untuk mendekripsi data audio dari file teks
def decrypt_audio_from_txt(input_file, output_file, aes_key):
    with open(input_file, 'rb') as txt_file:
        encrypted_audio = txt_file.read()

    iv = encrypted_audio[:AES.block_size]  # Mendapatkan IV dari data terenkripsi
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)  # Menggunakan IV dalam mode CBC
    decrypted_audio = unpad(cipher.decrypt(encrypted_audio[AES.block_size:]), AES.block_size)

    audio = AudioSegment(
        data=decrypted_audio,
        sample_width=2,
        frame_rate=44100,
        channels=2
    )

    audio.export(output_file, format="wav")

# Fungsi untuk memilih file audio atau teks tergantung pada mode
def browse_file():
    if encrypt_mode.get() == 1:
        filetypes = [("Audio Files", "*.wav")]
    else:
        filetypes = [("Text Files", "*.txt")]
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

# Fungsi untuk mengatur operasi enkripsi atau dekripsi
def process_operation():
    if output_file_entry.get() == "":
        result_label.config(text="Nama file output kosong.")
    else:
        if encrypt_mode.get() == 1:
            encrypt()
        else:
            decrypt()

# Fungsi untuk mengenkripsi
def encrypt():
    user_key_plain = key_input.get()
    
    # Memeriksa panjang kunci, harus 16 byte (128 bit) untuk AES
    if len(user_key_plain) != 16:
        result_label.config(text="Enkripsi gagal, kunci harus 16 byte.")
        return

    user_key_cipher = shift_cipher_13(user_key_plain)

    aes_key = user_key_cipher.encode('utf-8')
    input_audio_file = input_file_entry.get()
    output_file_name = output_file_entry.get()
    output_text_file = f"{output_file_name}.txt"  # Ganti ekstensi menjadi .txt

    start_time = time.time()  # Catat waktu mulai enkripsi
    encrypt_audio_to_txt(input_audio_file, output_text_file, aes_key)
    end_time = time.time()  # Catat waktu selesai enkripsi

    encryption_time_text.set(f"{end_time - start_time:.4f} detik")  # Tampilkan waktu proses

    result_label.config(text="Enkripsi selesai.")

# Fungsi untuk mendekripsi
def decrypt():
    user_key_plain = key_input.get()

    user_key_cipher = shift_cipher_13(user_key_plain)

    aes_key = user_key_cipher.encode('utf-8')
    input_text_file = input_file_entry.get()
    output_file_name = output_file_entry.get()
    output_audio_file = f"{output_file_name}.wav"

    try:
        start_time = time.time()  # Catat waktu mulai dekripsi
        decrypt_audio_from_txt(input_text_file, output_audio_file, aes_key)
        end_time = time.time()  # Catat waktu selesai dekripsi

        decryption_time_text.set(f"{end_time - start_time:.4f} detik")  # Tampilkan waktu proses

        # Memeriksa apakah dekripsi berhasil atau tidak
        if os.path.exists(output_audio_file):
            result_label.config(text="Dekripsi selesai.")
        else:
            result_label.config(text="Dekripsi gagal, kunci salah.")
    except Exception as e:
        # Menangani exception jika terjadi kesalahan selama dekripsi
        result_label.config(text="Dekripsi gagal, kunci salah.")


# Membuat jendela utama
root = tk.Tk()
root.title("Kriptografi AES Dan Shift Cipher Keamanan Audio WAV")

# Label
tk.Label(root, text="Kunci:").grid(row=0, column=0, pady=5, padx=10)
key_input = tk.Entry(root)
key_input.grid(row=0, column=1, pady=10, padx=10)

# Fungsi untuk menghasilkan kunci acak
def generate_random_key():
    random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    key_input.delete(0, tk.END)
    key_input.insert(0, random_key)

# Tombol untuk menghasilkan kunci acak
random_key_button = tk.Button(root, text="Kunci Acak", command=generate_random_key)
random_key_button.grid(row=0, column=2, pady=10, padx=3)

# Label dan Entry untuk input file
tk.Label(root, text="File Input:").grid(row=1, column=0, pady=5, padx=10)
input_file_entry = tk.Entry(root)
input_file_entry.grid(row=1, column=1, pady=10, padx=10)
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, pady=10, padx=3)

# Label dan Entry untuk output file
tk.Label(root, text="File Output:").grid(row=2, column=0, pady=5, padx=10)
output_file_entry = tk.Entry(root)
output_file_entry.grid(row=2, column=1, pady=10, padx=10)

# Radio button untuk mode enkripsi atau dekripsi
encrypt_mode = tk.IntVar()
encrypt_mode.set(1)  # Mode enkripsi
tk.Radiobutton(root, text="Enkripsi", variable=encrypt_mode, value=1).grid(row=3, column=0, pady=5, padx=10)
tk.Radiobutton(root, text="Dekripsi", variable=encrypt_mode, value=2).grid(row=3, column=1, pady=5, padx=10)

# Tombol Enkripsi atau Dekripsi
process_button_text = tk.StringVar()
process_button_text.set("Mulai")
process_button = tk.Button(root, textvariable=process_button_text, command=process_operation)
process_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

# Label untuk menampilkan hasil
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, pady=20)

# Label untuk menampilkan waktu enkripsi dan dekripsi
encryption_time_text = tk.StringVar()
decryption_time_text = tk.StringVar()

tk.Label(root, text="Waktu Enkripsi:").grid(row=6, column=0, pady=5, padx=10)
encryption_time_label = tk.Label(root, textvariable=encryption_time_text)
encryption_time_label.grid(row=6, column=1, pady=10, padx=10)

tk.Label(root, text="Waktu Dekripsi:").grid(row=7, column=0, pady=5, padx=10)
decryption_time_label = tk.Label(root, textvariable=decryption_time_text)
decryption_time_label.grid(row=7, column=1, pady=10, padx=10)

root.mainloop()
