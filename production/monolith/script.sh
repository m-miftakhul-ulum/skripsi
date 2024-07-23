#!/bin/bash

set -e

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install Python 3, pip, and nginx
echo "Installing Python 3, pip, and nginx..."
sudo apt install python3-pip python3-dev nginx -y

echo "Installing virtualenv..."
sudo pip3 install virtualenv

# Clone the repository
echo "Cloning the repository..."
git clone https://github.com/m-miftakhul-ulum/monolith-thesis.git

# Navigate into the cloned repository directory
cd monolith-thesis

# Create a virtual environment and activate it
echo "Creating and activating virtual environment..."
virtualenv env
source env/bin/activate

# Install the required Python packages
echo "Installing Python packages..."
pip3 install --no-cache-dir -r requirements.txt
pip3 install flask gunicorn

# Create systemd service file for Gunicorn
echo "Creating systemd service file for Gunicorn..."
sudo tee /etc/systemd/system/app.service > /dev/null <<EOL
[Unit]
Description=Gunicorn instance to serve monolith
After=network.target

[Service]
User=cloud_user_p_85b877e1
Group=www-data
WorkingDirectory=/home/cloud_user_p_85b877e1/monolith-thesis/
Environment="PATH=/home/cloud_user_p_85b877e1/monolith-thesis/env/bin"
ExecStart=/home/cloud_user_p_85b877e1/monolith-thesis/env/bin/gunicorn --workers 3 --bind unix:/home/cloud_user_p_85b877e1/monolith-thesis/app.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to pick up the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Start and enable the Gunicorn service
echo "Starting and enabling Gunicorn service..."
sudo systemctl start app
sudo systemctl enable app

# Create Nginx configuration file
echo "Creating Nginx configuration file..."
sudo tee /etc/nginx/sites-available/app > /dev/null <<EOL
server {
    listen 80;
    server_name 35.226.64.145;
    client_max_body_size 50M;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/cloud_user_p_85b877e1/monolith-thesis/app.sock;
    }

    location /static {
        include /etc/nginx/mime.types;
        root /home/cloud_user_p_85b877e1/monolith-thesis;
    }
}
EOL

# Enable the Nginx configuration
echo "Enabling Nginx configuration..."
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled

# Adjust permissions
echo "Adjusting permissions..."
sudo chmod 775 -R /home/cloud_user_p_85b877e1/monolith-thesis
sudo chmod 775 -R /home/cloud_user_p_85b877e1

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

# Allow Nginx Full in UFW
echo "Allowing Nginx Full in UFW..."
sudo ufw allow 'Nginx Full'

echo "Deployment script completed successfully!"