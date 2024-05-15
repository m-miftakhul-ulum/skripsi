from flask import Flask, request, jsonify, send_file
from PIL import Image
import numpy as np
import os
import time
from sympy import Matrix, gcd
import random

app = Flask(__name__)


def decrypt_image(encrypted_image_path, key_image_path, modulus=256):
    start_time = time.time()

    # Read the encrypted image
    encrypted_image = Image.open(encrypted_image_path)
    encrypted_pixels = np.array(encrypted_image)

    # Read the key image
    key_image = Image.open(key_image_path)
    key_matrix = np.array(key_image)

    size = key_matrix.shape[0]
    key_matrix_inv = Matrix(key_matrix).inv_mod(modulus)
    flat_encrypted_pixels = encrypted_pixels.reshape(-1, size)
    decrypted_pixels = (
        flat_encrypted_pixels.dot(np.array(key_matrix_inv).astype(np.int64))
    ) % modulus
    decrypted_image = decrypted_pixels.reshape(encrypted_pixels.shape)

    end_time = time.time()
    print(f"Decryption time: {end_time - start_time} seconds")

    # Save decrypted image to 'dekripsi' folder
    decrypted_image_folder = "dekripsi"
    if not os.path.exists(decrypted_image_folder):
        os.makedirs(decrypted_image_folder)
    decrypted_image_path = os.path.join(
        decrypted_image_folder,
        os.path.basename(encrypted_image_path).split(".")[0] + "_decrypted.png",
    )
    save_image(decrypted_image, decrypted_image_path)

    return decrypted_image_path


def save_image(image, image_path):
    Image.fromarray(np.uint8(image)).save(image_path)
    print(f"Image saved to {image_path}")


@app.route("/decrypt_image", methods=["POST"])
def api_decrypt_image():
    if "encrypted_image" not in request.files or "key_image" not in request.files:
        return jsonify({"error": "Encrypted image or key image file not provided"}), 400

    encrypted_image_file = request.files["encrypted_image"]
    key_image_file = request.files["key_image"]

    # Save the uploaded images to temporary locations
    encrypted_image_path = os.path.join("uploads", encrypted_image_file.filename)
    key_image_path = os.path.join("uploads", key_image_file.filename)
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


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
