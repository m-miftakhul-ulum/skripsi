from flask import Flask, request, jsonify
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pydub import AudioSegment

app = Flask(__name__)

def shift_cipher_13(text):
    # Implementasi dari shift cipher 13
    pass

def decrypt_audio_from_txt(input_file, output_file, aes_key):
    with open(input_file, 'rb') as txt_file:
        encrypted_audio = txt_file.read()

    iv = encrypted_audio[:AES.block_size]  # Mendapatkan IV dari data terenkripsi
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)  # Menggunakan IV dalam mode CBC
    decrypted_audio = unpad(cipher.decrypt(encrypted_audio[AES.block_size:]), AES.block_size)

    audio = AudioSegment(
        data=decrypted_audio,
        sample_width=2,
        frame_rate=44100,
        channels=2
    )

    audio.export(output_file, format="wav")

@app.route("/decrypt_audio", methods=["POST"])
def decrypt():
    user_key_plain = request.form.get("user_key_plain")
    input_text_file = request.files.get("input_text_file")
    output_file_name = request.form.get("output_file_name")

    if not user_key_plain or len(user_key_plain) != 16:
        return jsonify({"error": "Kunci harus 16 byte."}), 400

    if not input_text_file or not output_file_name:
        if not input_text_file:
            error_message = "File teks tidak ditemukan."
        else:
            error_message = "Nama file output tidak ditemukan."
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

    output_audio_file = os.path.join(dekrip_dir, f"{output_file_name}.wav")

    decrypt_audio_from_txt(input_text_path, output_audio_file, user_key_cipher)

    return jsonify(
        {
            "message": "Dekripsi selesai.",
            "output_file": output_audio_file
        }
    )

if __name__ == "__main__":
    app.run(debug=True)
