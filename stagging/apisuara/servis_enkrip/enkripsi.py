import wave
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, jsonify
import os
import random
import string

app = Flask(__name__)


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


@app.route("/encrypt_audio", methods=["POST"])
def encrypt():
    user_key_plain = request.form.get("user_key_plain")
    input_audio_file = request.files.get("input_audio_file")
    # output_file_name = request.form.get("output_file_name")

    if not user_key_plain or len(user_key_plain) != 16:
        return jsonify({"error": "Kunci harus 16 byte."}), 400

    # if not input_audio_file:
    if not input_audio_file:
        error_message = "File audio tidak ditemukan."
        return jsonify({"error": error_message}), 400
    # else:
        # error_message = "Nama file output tidak ditemukan."
    # return jsonify({"error": error_message}), 400

    user_key_cipher = shift_cipher_13(user_key_plain).encode("utf-8")
    # output_text_file = f"{output_file_name}.txt"

    # Simpan file audio ke folder temp
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    random_name = generate_random_filename()
    random_filename = random_name + os.path.splitext(input_audio_file.filename)[1]

    input_audio_path = os.path.join(temp_dir, random_filename)
    input_audio_file.save(input_audio_path)

    # Simpan file hasil enkripsi ke folder enkrip
    enkrip_dir = "enkrip"
    if not os.path.exists(enkrip_dir):
        os.makedirs(enkrip_dir)

    output_text_file = os.path.join(enkrip_dir, f"{random_name}.txt")

    start_time = time.time()
    encrypt_audio_to_txt(input_audio_path, output_text_file, user_key_cipher)
    end_time = time.time()
    
    try:
        os.remove(input_audio_path)
    except Exception as e:
        print(f"Failed to delete temporary files: {str(e)}")

    return jsonify(
        {
            "message": "success",
            "encrypted_audio_download": input_audio_path
        }
    ), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5002")
