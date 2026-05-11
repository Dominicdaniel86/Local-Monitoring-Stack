#!/bin/bash
set -e

# Installs Git, Docker, Docker Compose plugin, and Docker Buildx plugin globally.

COMPOSE_VERSION="v2.40.3"
BUILDX_VERSION="v0.19.3"

# Install Git and Docker
sudo dnf update -y || sudo yum update -y
sudo dnf install -y git docker curl || sudo yum install -y git docker curl

# Start Docker
sudo systemctl enable --now docker

# Add ec2-user to docker group
sudo usermod -aG docker ec2-user

# Docker CLI plugin directory
sudo mkdir -p /usr/local/lib/docker/cli-plugins

# Install Docker Compose plugin globally
sudo curl -SL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-x86_64" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose

sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Install Docker Buildx plugin globally
sudo curl -SL "https://github.com/docker/buildx/releases/download/${BUILDX_VERSION}/buildx-${BUILDX_VERSION}.linux-amd64" \
  -o /usr/local/lib/docker/cli-plugins/docker-buildx

sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx

# Verify installs
git --version
docker --version
docker compose version
docker buildx version

echo "Setup complete."
echo "If Docker permission fails, log out and SSH back in."
echo "Then run:"
echo "cd ~/Local-Monitoring-Stack"
echo "docker compose up --build -d"
