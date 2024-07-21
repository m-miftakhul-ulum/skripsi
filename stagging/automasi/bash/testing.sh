#!/bin/bash

# Update package lists
sudo apt update

# Install Python 3, pip, and virtualenv
sudo apt install python3-pip python3-dev -y
sudo pip3 install virtualenv

# Clone the repository
git clone https://github.com/m-miftakhul-ulum/monolith-thesis.git


cd skripsi/stagging/testing

# Create a virtual environment named "env"
virtualenv env

# Activate the virtual environment
source env/bin/activate

# Install the required Python packages
pip install --no-cache-dir -r requirements.txt

sudo ufw allow 8089/tcp

locust -f testing.py