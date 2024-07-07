import time
from PIL import Image
import numpy as np
from sympy import Matrix, gcd
import os



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
    # decrypted_pixels = (flat_encrypted_pixels.dot(key_matrix_inv)) % modulus

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
