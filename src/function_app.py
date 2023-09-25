import logging
import azure.functions as func
import toml
import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from core import create_file_handler, LOG_FILE_PATH


TOML_FILE_PATH = "config.toml"
RESULT_CONTAINER_NAME = "results"
INGEST_CONTAINER_NAME = "ingest"

app = func.FunctionApp()


def read_blob_content(blob: func.InputStream):
    return blob.read().decode('utf-8')


def dump_to_local_toml(content: str) -> None:
    config = toml.loads(content)
    with open(TOML_FILE_PATH, "w") as toml_file:
        toml.dump(config, toml_file)
    return None


def create_result_base_path() -> str:
    current_date = datetime.now().strftime("%Y%m%d")
    current_date_time = datetime.now().strftime("%Y%m%d%H%M")
    run_folder_name = f"{current_date_time}_my_test"
    base_path = os.path.join(current_date, run_folder_name)
    return base_path


@app.function_name(name="BlobHandler")
@app.blob_trigger(arg_name="newblob",
                  path="ingest",
                  connection="StorageConnection")
def test_function(newblob: func.InputStream):
    # ATTACH FILE HANDLER
    logging.getLogger().addHandler(create_file_handler())

    content = read_blob_content(newblob)
    logging.info(f"Python blob trigger function processed blob: {newblob.name}")
    logging.info(f"Configuration file content:\n{content}")

    dump_to_local_toml(content)

    connection_string = os.environ["StorageConnection"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    result_base_path = create_result_base_path()

    # Create a ContainerClient
    container_client = blob_service_client.get_container_client(RESULT_CONTAINER_NAME)

    # Create or overwrite the file in Blob Storage
    blob_client = container_client.get_blob_client(result_base_path+"/config.toml")
    blob_client.upload_blob(content, overwrite=True)

    # Log the successful upload
    logging.info(f"Uploaded result files to '{result_base_path}' container")

    # Clean Ingest Stage
    ingest_container_client = blob_service_client.get_container_client(INGEST_CONTAINER_NAME)
    ingest_container_client.delete_blob("test.toml")
    logging.info(f"{newblob.name} successfully deleted from ingest area.")
    logging.info(f"Upload and remove '{LOG_FILE_PATH}'.")

    with open(LOG_FILE_PATH, "rb") as log_file:
        blob_client = container_client.get_blob_client(result_base_path+"/execution.log")
        blob_client.upload_blob(log_file, overwrite=True)

    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()

    # CLEAR LOCAL FILES
    if True:
        logging.getLogger().removeHandler(create_file_handler())
        if os.path.exists(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)

        if os.path.exists(TOML_FILE_PATH):
            os.remove(TOML_FILE_PATH)
