#!/bin/bash -i

sudo apt update
sudo apt upgrade -y

## deps install
sudo apt install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
ffmpeg ffmpeg libsm6 libxext6

## asdf install
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.0
echo '. "$HOME/.asdf/asdf.sh"' >> ~/.bashrc
echo '. "$HOME/.asdf/completions/asdf.bash"' >> ~/.bashrc
source $HOME/.bashrc

asdf plugin-add python
asdf install python latest
asdf global python latest

## app install
git clone https://github.com/indie-rok/upspeak-back.git
cd upspeak-back/
python -m venv env
source env/bin/activate
pip install -r requirements.txt
mkdir logs

## new version of ffmpeg (fastest)
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz
tar -xf ffmpeg-release-arm64-static.tar.xz
sudo mv ./ffmpeg-7.0.1-arm64-static/ffmpeg /usr/local/bin
rm ffmpeg-release-arm64-static.tar.xz
rm -rf ffmpeg-7.0.1-arm64-static/

cp .env.copy .env

# Create and edit the systemd service file
sudo bash -c 'cat <<EOF > /etc/systemd/system/myproject.service
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/upspeak-back
Environment="PATH=/home/ubuntu/upspeak-back/env/bin:/usr/bin"
ExecStart=/home/ubuntu/upspeak-back/env/bin/gunicorn --config gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
EOF'

# Start the systemd service
sudo systemctl start myproject

# Enable the service to start on boot
sudo systemctl enable myproject

reboot