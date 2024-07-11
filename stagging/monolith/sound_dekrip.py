from flask import Flask, request, jsonify
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pydub import AudioSegment
import random
import string


def decrypt_audio_from_txt(input_file, output_file, aes_key):
    with open(input_file, "rb") as txt_file:
        encrypted_audio = txt_file.read()

    iv = encrypted_audio[: AES.block_size]  # Mendapatkan IV dari data terenkripsi
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)  # Menggunakan IV dalam mode CBC
    decrypted_audio = unpad(
        cipher.decrypt(encrypted_audio[AES.block_size :]), AES.block_size
    )

    audio = AudioSegment(
        data=decrypted_audio, sample_width=2, frame_rate=44100, channels=1
    )

    audio.export(output_file, format="wav")
