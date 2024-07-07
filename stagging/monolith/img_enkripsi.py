
import string
import random
import time
from PIL import Image
import numpy as np
from sympy import Matrix, gcd
import os


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

    # matrix_string = "\n".join(" ".join(str(cell) for cell in row) for row in key_matrix)

    # Menyimpan matriks ke file txt
    # filename = "key_matrix.txt"
    # with open(filename, "w") as file:
    #     file.write(matrix_string)

    # Save key image
    key_folder = "kunci"
    if not os.path.exists(key_folder):
        os.makedirs(key_folder)
    key_image_path = os.path.join(
        key_folder, os.path.basename(image_path).split(".")[0] + "_key.png"
    )
    key_image = Image.fromarray(key_matrix.astype("uint8"))
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

    end_time = time.time()
    encrypted_image_path = (
        "enkripsi/" + os.path.basename(image_path).split(".")[0] + "_encrypted.png"
    )
    key_folder = "enkripsi"
    if not os.path.exists(key_folder):
        os.makedirs(key_folder)
    enc_image = Image.fromarray(encrypted_image.astype("uint8"))
    enc_image.save(encrypted_image_path)

    return encrypted_image_path, end_time - start_time


def generate_random_filename(length=8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
