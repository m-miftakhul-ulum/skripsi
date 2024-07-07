import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import random
import string



def shift_cipher_13(text):
    shifted_text = ""
    for char in text:
        if "A" <= char <= "Z":
            shifted_char = chr(((ord(char) - ord("A") + 13) % 26) + ord("A"))
        elif "a" <= char <= "z":
            shifted_char = chr(((ord(char) - ord("a") + 13) % 26) + ord("a"))
        else:
            shifted_char = char
        shifted_text += shifted_char
    return shifted_text


def encrypt_audio_to_txt(input_file, output_file, aes_key):
    iv = os.urandom(AES.block_size)  # Generate IV
    with open(input_file, "rb") as audio_file:
        audio_data = audio_file.read()

    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)  # Menggunakan IV dalam mode CBC
    encrypted_audio = iv + cipher.encrypt(pad(audio_data, AES.block_size))

    with open(output_file, "wb") as txt_file:
        txt_file.write(encrypted_audio)


def generate_random_filename(length=8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

