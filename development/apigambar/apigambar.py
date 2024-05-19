from flask import Flask, request, jsonify, send_file
from PIL import Image
import numpy as np
import os
import time
from sympy import Matrix, gcd
import random

app = Flask(__name__)

def generate_key_matrix(image_path, modulus=256):
    try:
        image = Image.open(image_path)
    except Exception as e:
        return None, f"Error opening image file: {str(e)}"

    pixels = np.array(image)
    key_matrix = None
    size = None

    while key_matrix is None:
        size = np.random.randint(3, 21)
        key_matrix = np.random.randint(0, modulus, size=(size, size))

        if pixels.size % size != 0 or np.linalg.matrix_rank(key_matrix) != size:
            key_matrix = None

    sympy_matrix = Matrix(key_matrix)

    while gcd(int(sympy_matrix.det()), modulus) != 1:
        key_matrix = np.random.randint(0, modulus, size=(size, size))
        sympy_matrix = Matrix(key_matrix)

    matrix_string = '\n'.join(' '.join(str(cell) for cell in row) for row in key_matrix)

    # Menyimpan matriks ke file txt
    filename = "key_matrix.txt"
    with open(filename, "w") as file:
        file.write(matrix_string)


    # Save key image
    key_folder = 'kunci'
    if not os.path.exists(key_folder):
        os.makedirs(key_folder)
    key_image_path = os.path.join(key_folder, os.path.basename(image_path).split('.')[0] + '_key.png')
    key_image = Image.fromarray(key_matrix.astype('uint8'))
    key_image.save(key_image_path)

    return key_matrix, key_image_path

def encrypt_image(image_path, key_matrix, modulus=256):
    start_time = time.time()
    image = Image.open(image_path)
    pixels = np.array(image)

    size = key_matrix.shape[0]
    flat_pixels = pixels.reshape(-1, size)
    encrypted_pixels = (flat_pixels.dot(key_matrix)) % modulus
    encrypted_image = encrypted_pixels.reshape(pixels.shape)

    encrypted_image_path = 'enkripsi/' + os.path.basename(image_path).split('.')[0] + '_encrypted.png'
    enc_image = Image.fromarray(encrypted_image.astype('uint8'))
    enc_image.save(encrypted_image_path)

    end_time = time.time()
    return encrypted_image_path, end_time - start_time



@app.route('/enkripsi_gambar', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        key_matrix, key_image_path = generate_key_matrix(file_path)
        
        encrypted_image_path, encryption_time = encrypt_image(file_path, key_matrix)
        return jsonify({
            'message': 'File processed',
            'key_image': key_image_path,
            'encrypted_image': encrypted_image_path,
            'encryption_time': encryption_time
        }), 200

@app.route('/dekripsi_gambar', methods=['POST'])
def deksripsigambar():
    return 'wow'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")