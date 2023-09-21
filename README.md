# Azure Functions Blob Storage Ingest Template

https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob-trigger?tabs=python-v2%2Cin-process%2Cnodejs-v4&pivots=programming-language-python#configuration


## Local Development Setup
Install Azure Storage Explorer
```
https://azure.microsoft.com/en-in/products/storage/storage-explorer/
```

Run Azurite Blob Storage Service locally with
````bash
 docker run -p 10000:10000 -p 10001:10001 -p 10002:10002 -v c:/azurite:/data mcr.microsoft.com/azure-storage/azurite
 ````
Connect to your local blob containers using the Storage Explorer.

### Blob Container Setup
Create a new blob container named `ingest`.

Install Azure Functions Core Tool
```
https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python#install-the-azure-functions-core-tools
```
Start local function from the `\src` directory with 

```
func start
```


### local.settings.json
```
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "StorageConnection": "..."
  }
}
```