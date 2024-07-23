-set e

sudo apt update

sudo apt install python3 python3-pip

sudo apt install unzip

pip3 install locust

pip3 install gdown

export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc

git clone https://github.com/m-miftakhul-ulum/skripsi.git

sudo apt install python3-locust

pip3 install --upgrade locust

sudo ufw allow 8089/tcp

cd skripsi/stagging/testing

# download file enkripsi suara
gdown https://drive.google.com/uc?id=10qrteCXqbMjovvzCC2MPofTZgt55PxFS

# download file dekripsi suara
gdown https://drive.google.com/uc?id=1UjmU0K5mMjflzCW9-9oRxMrwwXzpeKGM

# download file enkripsi gambar
gdown https://drive.google.com/uc?id=1RjjCGBQO5TxuJvCkrDAMDwEOaOVU8372

# download file dekripsi gambar
gdown https://drive.google.com/uc?id=1-oHhSOijctgKID3-Zd5pvWVNWxB4oPQi

sudo unzip test_enkrip_gambar.zip
sudo unzip test_dekrip_gambar.zip

sudo unzip test_enkrip_suara.zip
sudo unzip test_dekrip_suara.zip
