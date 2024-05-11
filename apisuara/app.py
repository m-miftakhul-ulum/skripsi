from flask import Flask, jsonify, request
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import wave
import io

app = Flask(__name__)

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

def encrypt_audio_to_txt(input_file_path, output_text_file, key):
    # Membaca file audio
    with wave.open(input_file_path, 'rb') as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
    
    # Encrypt data
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(frames, AES.block_size))

    # Menulis hasil enkripsi ke file teks
    with open(output_text_file, 'wb') as f:
        f.write(cipher.iv)
        f.write(encrypted_data)
        
def decrypt_audio_from_txt(encrypted_text_file, output_audio_file, key):
    # Membuka dan membaca file yang berisi data terenkripsi
    with open(encrypted_text_file, 'rb') as f:
        iv = f.read(16)  # 16 byte pertama untuk IV
        encrypted_data = f.read()  # Sisa file adalah data terenkripsi

    # Mengatur dekripsi AES
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # Menulis data yang telah didekripsi ke file output
    with wave.open(output_audio_file, 'wb') as wav_file:
        wav_file.writeframes(decrypted_data)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"name": "John", "age": 30}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    return jsonify(data), 201

@app.route('/encrypt_audio', methods=['POST'])
def encrypt():
    data = request.json
    user_key_plain = data.get('user_key_plain')
    input_audio_file = data.get('input_audio_file')
    output_file_name = data.get('output_file_name')

    if len(user_key_plain) != 16:
        return jsonify({"error": "Kunci harus 16 byte."}), 400

    user_key_cipher = shift_cipher_13(user_key_plain).encode('utf-8')
    output_text_file = f"{output_file_name}.txt"

    start_time = time.time()
    encrypt_audio_to_txt(input_audio_file, output_text_file, user_key_cipher)
    end_time = time.time()

    return jsonify({
        "message": "Enkripsi selesai.",
        "encryption_time": f"{end_time - start_time:.4f} detik"
    })

@app.route('/decrypt_audio', methods=['POST'])
def decrypt():
    data = request.json
    user_key_plain = data.get('user_key_plain')
    encrypted_audio_file = data.get('encrypted_audio_file')
    output_audio_file = data.get('output_audio_file')

    if len(user_key_plain) != 16:
        return jsonify({"error": "Kunci harus 16 byte."}), 400

    user_key_cipher = shift_cipher_13(user_key_plain).encode('utf-8')

    decrypt_audio_from_txt(encrypted_audio_file, output_audio_file, user_key_cipher)

    return jsonify({"message": "Dekripsi selesai."})

if __name__ == '__main__':
    app.run(debug=True)
