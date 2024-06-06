#!/bin/bash

# Define variables
ACR_NAME="streamlit"
DOCKER_IMAGE="streamlit-app"
ACR_IMAGE="streamlit.azurecr.io/tca-app"

# Log in to Azure Container Registry (ACR)
echo "Logging in to Azure Container Registry..."
az acr login --name $ACR_NAME
echo "Logged in to Azure Container Registry."

# Build the Docker image
echo "Building the Docker image..."
docker build -t $DOCKER_IMAGE --platform linux/amd64 .
echo "Docker image built."

# Tag the Docker image for ACR
echo "Tagging the Docker image for ACR..."
docker tag $DOCKER_IMAGE $ACR_IMAGE
echo "Docker image tagged."

# Push the Docker image to ACR
echo "Pushing the Docker image to ACR..."
docker push $ACR_IMAGE
echo "Docker image pushed to ACR."
