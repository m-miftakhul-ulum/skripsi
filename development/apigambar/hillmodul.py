import os
import numpy as np
from sympy import Matrix
from math import gcd
from PIL import Image
import time

def generate_key_matrix(image_path, modulus=256):
    if not image_path:
        print("Empty image path. Please provide a valid image file path.")
        return None

    if not os.path.exists(image_path):
        print(f"File '{image_path}' not found. Please provide a valid image file path.")
        return None

    try:
        with open(image_path, 'rb') as file:
            image = Image.open(file)
    except Exception as e:
        print(f"Error opening image file: {str(e)}")
        return None
    
    image = Image.open(image_path)
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
    
    # Save key image
    key_image = Image.fromarray(key_matrix.astype('uint8'))
    key_folder = 'kunci'
    if not os.path.exists(key_folder):
        os.makedirs(key_folder)
    key_image_path = os.path.join(key_folder, os.path.basename(image_path).split('.')[0] + '_key.png')
    key_image.save(key_image_path)
    print(f'Key image saved to {key_image_path}')
        
    return key_matrix

def encrypt_image(image_path, key_matrix, modulus=256):
    start_time = time.time()
    image = Image.open(image_path)
    pixels = np.array(image)
    
    size = key_matrix.shape[0]
    flat_pixels = pixels.reshape(-1, size)
    encrypted_pixels = (flat_pixels.dot(key_matrix)) % modulus
    encrypted_image = encrypted_pixels.reshape(pixels.shape)
    
    end_time = time.time()
    print(f"Encryption time: {end_time - start_time} seconds")

    # Save encrypted image to 'enkripsi' folder
    encrypted_image_folder = 'enkripsi'
    if not os.path.exists(encrypted_image_folder):
        os.makedirs(encrypted_image_folder)
    encrypted_image_path = os.path.join(encrypted_image_folder, os.path.basename(image_path).split('.')[0] + '_encrypted.png')
    save_image(encrypted_image, encrypted_image_path)
    
    return encrypted_image

def decrypt_image(encrypted_image, key_matrix, modulus=256):
    start_time = time.time()
    size = key_matrix.shape[0]
    key_matrix_inv = Matrix(key_matrix).inv_mod(modulus)
    flat_encrypted_pixels = encrypted_image.reshape(-1, size)
    decrypted_pixels = (flat_encrypted_pixels.dot(key_matrix_inv)) % modulus
    decrypted_image = decrypted_pixels.reshape(encrypted_image.shape)
    
    end_time = time.time()
    print(f"Decryption time: {end_time - start_time} seconds")

    # Save decrypted image to 'dekripsi' folder
    decrypted_image_folder = 'dekripsi'
    if not os.path.exists(decrypted_image_folder):
        os.makedirs(decrypted_image_folder)
    decrypted_image_path = os.path.join(decrypted_image_folder, os.path.basename(image_path).split('.')[0] + '_decrypted.png')
    save_image(decrypted_image, decrypted_image_path)
    
    return decrypted_image

# done 
def save_image(image, image_path):
    Image.fromarray(np.uint8(image)).save(image_path)
    print(f"Image saved to {image_path}")

if __name__ == "__main__":
    image_path = '12.jpg'

    # Generate key matrix
    key_matrix = generate_key_matrix(image_path)


    print(key_matrix.shape[0])
    
    # Encrypt image
    encrypted_image = encrypt_image(image_path, key_matrix)

    # Decrypt image
    decrypted_image = decrypt_image(encrypted_image, key_matrix)
    # decrypted_image = decrypt_image('enkripsi/tempimage_encrypted.png', key_matrix)