#!/bin/bash

# Update package lists
sudo apt update

# Install Python 3, pip, and virtualenv
sudo apt install python3-pip python3-dev -y
sudo pip3 install virtualenv

# Create a directory named "testing" and navigate into it
mkdir testing && cd testing

# Create a virtual environment named "env"
virtualenv env

# Activate the virtual environment
source env/bin/activate

# Clone the repository
git clone https://github.com/m-miftakhul-ulum/skripsi/tree/main/stagging/testing

# Navigate into the cloned repository directory
cd testing

# Install the required Python packages
pip install --no-cache-dir -r requirements.txt
