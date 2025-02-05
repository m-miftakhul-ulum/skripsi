from flask import Flask, request, jsonify
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pydub import AudioSegment
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


def decrypt_audio_from_txt(input_file, output_file, aes_key):
    with open(input_file, "rb") as txt_file:
        encrypted_audio = txt_file.read()

    iv = encrypted_audio[: AES.block_size]  # Mendapatkan IV dari data terenkripsi
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)  # Menggunakan IV dalam mode CBC
    decrypted_audio = unpad(
        cipher.decrypt(encrypted_audio[AES.block_size :]), AES.block_size
    )

    audio = AudioSegment(
        data=decrypted_audio, sample_width=2, frame_rate=44100 * 2, channels=1
    )

    audio.export(output_file, format="wav")


def generate_random_filename(length=8):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5003")
