# Proyecto de Análisis de Reservaciones

Este repositorio contiene un proyecto para el análisis de reservaciones en la industria hotelera. Se proporcionan varios archivos para su configuración y despliegue.

## Archivos incluidos

1. **app/app.py**: Este archivo contiene el código principal de la aplicación para el análisis de reservaciones. Utiliza bibliotecas como Plotly, Streamlit y Azure Blob Storage para cargar datos y crear visualizaciones interactivas.

2. **Dockerfile**: Este archivo se utiliza para construir la imagen Docker necesaria para ejecutar la aplicación de análisis de reservaciones.

3. **deploy_doc.sh**: Este script facilita el despliegue de la aplicación en Azure Container Registry (ACR). Contiene los comandos necesarios para compilar la imagen Docker, etiquetarla y subirla a ACR.

4. **requirements.txt**: Este archivo especifica las dependencias Python necesarias para ejecutar la aplicación. Incluye bibliotecas como Streamlit, Pandas, Plotly, Azure Storage Blob, Python Dotenv y Scikit-learn.

## Instrucciones de Uso

Para utilizar este proyecto, sigue los siguientes pasos:

1. Clona este repositorio en tu máquina local utilizando el comando `git clone`.

2. Instala las dependencias Python especificadas en el archivo `requirements.txt` utilizando el gestor de paquetes de Python de tu elección, como `pip`.

```bash
pip install -r requirements.txt
```

3. Construye la imagen Docker utilizando el Dockerfile proporcionado.

```bash
docker build -t nombre_imagen .
```

4. Ejecuta el script `deploy_docker.sh` para desplegar la aplicación en Azure Container Registry (ACR).

```bash
bash deploy_docker.sh
```

Una vez completados estos pasos, la aplicación estará lista para ser desplegada y utilizada para el análisis de reservaciones en la industria hotelera.
