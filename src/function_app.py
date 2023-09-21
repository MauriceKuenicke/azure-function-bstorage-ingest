import logging
import azure.functions as func

app = func.FunctionApp()


@app.function_name(name="BlobTrigger1")
@app.blob_trigger(arg_name="newblob",
                  path="ingest",
                  connection="StorageConnection")
def test_function(newblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {newblob.name}\n"
                 f"Blob Size: {newblob.length} bytes")