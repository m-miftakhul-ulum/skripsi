#!/bin/bash

# Update package lists
sudo apt update

# Install Python 3, pip, and nginx
sudo apt install python3-pip python3-dev nginx -y
sudo pip3 install virtualenv

# Clone the repository
git clone https://github.com/m-miftakhul-ulum/monolith-thesis.git

# Navigate into the cloned repository directory
cd monolith-thesis

# Create a virtual environment and activate it
virtualenv env
source env/bin/activate

# Install the required Python packages
pip3 install --no-cache-dir -r requirements.txt
pip3 install flask gunicorn

# Start Gunicorn to ensure it's working (temporary, to be replaced by systemd service)
# gunicorn --bind 0.0.0.0:5000 wsgi:app &

# Create systemd service file for Gunicorn
sudo tee /etc/systemd/system/app.service > /dev/null <<EOL
[Unit]
Description=Gunicorn instance to serve monolith
After=network.target

[Service]
User=cloud_user
Group=www-data
WorkingDirectory=/home/cloud_user/monolith-thesis/
Environment="PATH=/home/cloud_user/monolith-thesis/env/bin"
ExecStart=/home/cloud_user/monolith-thesis/env/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
EOL

# Start and enable the Gunicorn service
sudo systemctl start app
sudo systemctl enable app

# Create Nginx configuration file
sudo tee /etc/nginx/sites-available/app > /dev/null <<EOL
server {
    listen 80;
    server_name 194.195.112.179;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/cloud_user/monolith-thesis/app.sock;
    }

    location /static {
        include /etc/nginx/mime.types;
        root /home/cloud_user/monolith-thesis;
    }
}
EOL

# Enable the Nginx configuration
sudo ln -s /etc/nginx/sites-available/app 
sudo ln -s /etc/nginx/sites-enabled

# Adjust permissions
sudo chmod 775 -R /home/cloud_user/monolith-thesis
sudo chmod 775 -R /home/cloud_user

# Restart Nginx
sudo systemctl restart nginx

# Allow Nginx Full in UFW
sudo ufw allow 'Nginx Full'
