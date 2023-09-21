import logging
import azure.functions as func
import tempfile
import toml
import os
import zipfile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


app = func.FunctionApp()


@app.function_name(name="BlobHandler")
@app.blob_trigger(arg_name="newblob",
                  path="ingest",
                  connection="StorageConnection")
def test_function(newblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob: {newblob.name}")
    content = newblob.read().decode('utf-8')
    logging.info("Configuration file content:")
    logging.info(content)
    config = toml.loads(content)

    with open("config.toml", "w") as toml_file:
        toml.dump(config, toml_file)

    connection_string = os.environ["StorageConnection"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_name = "results"
    ingest_container_name = "ingest"
    current_date = "20230921"
    run_folder_name = "202309212319_my_test"
    base_path = os.path.join(current_date, run_folder_name)

    # Create a ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    # Create or overwrite the zip file in Blob Storage
    blob_client = container_client.get_blob_client(base_path+"/config.toml")
    blob_client.upload_blob(content, overwrite=True)

    # Log the successful upload
    logging.info(f"Uploaded result files to '{base_path}' container")

    # Clean Ingest Stage
    ingest_container_client = blob_service_client.get_container_client(ingest_container_name)
    ingest_container_client.delete_blob("test.toml")
    logging.info(f"{newblob.name} successfully deleted from ingest area.")
