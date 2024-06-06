Write-Host "Building the new Docker image..."
Write-Host "docker build -t streamlit-image ."

Write-Host "Stopping the currently running container..."
docker stop streamlit-dashboard

Write-Host "Removing the stopped container..."
docker rm streamlit-dashboard

Write-Host "Running a new container with the updated image..."
docker run -d -p 8501:8501 --name streamlit-dashboard streamlit-image

Write-Host "Update complete."
