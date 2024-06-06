import os
from io import StringIO

import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def read_blob_to_df(container_name, blob_name, connection_string):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Download blob content as bytes
    blob_data = blob_client.download_blob().readall()

    # Convert bytes to a pandas DataFrame
    df = pd.read_csv(StringIO(blob_data.decode("utf-8")))
    return df


def load_data_from_azure():
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("CONTAINER_NAME")

    cancellation_percentages_df = read_blob_to_df(
        container_name, "cancellation_percentages.csv", connection_string
    )
    agencia_distribution = read_blob_to_df(
        container_name, "agencia_distribution.csv", connection_string
    )
    canal_distribution = read_blob_to_df(
        container_name, "canal_distribution.csv", connection_string
    )
    median_values = read_blob_to_df(
        container_name, "median_values.csv", connection_string
    )
    mean_values = read_blob_to_df(container_name, "mean_values.csv", connection_string)

    return {
        "cancellation_percentages_df": cancellation_percentages_df,
        "agencia_distribution": agencia_distribution,
        "canal_distribution": canal_distribution,
        "median_values": median_values,
        "mean_values": mean_values,
    }
