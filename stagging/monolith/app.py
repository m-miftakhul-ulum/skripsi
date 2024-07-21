from flask import Flask, request, jsonify, send_file
import numpy as np
import os
from sympy import Matrix, gcd
import random
import string
import time
from img_dekripsi import decrypt_image
from img_enkripsi import generate_key_matrix, encrypt_image, generate_random_filename
from sound_enkrip import shift_cipher_13, encrypt_audio_to_txt, generate_random_filename
from sound_dekrip import decrypt_audio_from_txt


app = Flask(__name__)


@app.route("/enkripsi_gambar", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    if file:
        file_path = os.path.join("uploads", file.filename)
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        random_filename = (
            generate_random_filename() + os.path.splitext(file.filename)[1]
        )
        file_path = os.path.join("uploads", random_filename)
        file.save(file_path)
        key_matrix, key_image_path = generate_key_matrix(file_path)

        encrypted_image_path, encryption_time = encrypt_image(file_path, key_matrix)

        if os.path.exists(file_path):
            os.remove(file_path)
        return (
            jsonify(
                {
                    "message": "success",
                    "key_image_download": key_image_path,
                    "encrypted_image_download": encrypted_image_path,
                    # "encryption_time": encryption_time,
                }
            ),
            200,
        )

def generate_random_filename(extension=''):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(8))
    return random_string + extension

@app.route("/decrypt_image", methods=["POST"])
def api_decrypt_image():
    if "encrypted_image" not in request.files or "key_image" not in request.files:
        return jsonify({"error": "Encrypted image or key image file not provided"}), 400

    encrypted_image_file = request.files["encrypted_image"]
    key_image_file = request.files["key_image"]

    # Generate random filenames for the uploaded images
    encrypted_image_filename = generate_random_filename('.png')
    key_image_filename = generate_random_filename('.png')

    # Save the uploaded images to temporary locations
    encrypted_image_path = os.path.join("uploads", encrypted_image_filename)
    key_image_path = os.path.join("uploads", key_image_filename)
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    encrypted_image_file.save(encrypted_image_path)
    key_image_file.save(key_image_path)

    decrypted_image_path = decrypt_image(encrypted_image_path, key_image_path)

    # Attempt to delete the temporary image files after processing
    try:
        os.remove(encrypted_image_path)
        os.remove(key_image_path)
    except Exception as e:
        print(f"Failed to delete temporary files: {str(e)}")

    if not decrypted_image_path:
        return jsonify({"error": "Decryption failed"}), 500

    return jsonify({"decrypted_image_path": decrypted_image_path})

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



@app.route("/decrypt_audio", methods=["POST"])
def decrypt():
    user_key_plain = request.form.get("user_key_plain")
    input_text_file = request.files.get("input_text_file")
    output_file_name = request.form.get("output_audio_file")

    if not user_key_plain or len(user_key_plain) != 16:
        return jsonify({"error": "Kunci harus 16 byte."}), 400

    if not input_text_file :
        if not input_text_file:
            error_message = "File teks tidak ditemukan."
        # else:
        #     error_message = "Nama file output tidak ditemukan."
        return jsonify({"error": error_message}), 400

    user_key_cipher = shift_cipher_13(user_key_plain).encode("utf-8")

    # Simpan file teks ke folder temp
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    input_text_path = os.path.join(temp_dir, input_text_file.filename)
    input_text_file.save(input_text_path)

    # Simpan file hasil dekripsi ke folder dekrip
    dekrip_dir = "dekrip"
    if not os.path.exists(dekrip_dir):
        os.makedirs(dekrip_dir)

    random_name = generate_random_filename()

    output_audio_file = os.path.join(dekrip_dir, f"{random_name}_decrypted.wav")

    # return input_text_path

    decrypt_audio_from_txt(input_text_path, output_audio_file, user_key_cipher)

    try:
        os.remove(input_text_path)
    except Exception as e:
        print(f"Failed to delete temporary files: {str(e)}")

    return jsonify({"message": "Dekripsi selesai.", "output_file": output_audio_file})



@app.route("/", methods=["GET"])
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")