# ETL Pipeline in Azure Function and deployed using CI/CD

This repository contains the code for an ETL (Extract, Transform, Load) pipeline that retrieves data from the Coincap API and stores the transformed data in an Azure Blob Storage. The ETL pipeline is designed to run via Azure Functions, providing a serverless and cloud-based solution.

## Code Overview
The main components of the ETL pipeline code include:
- Data extraction from the Coincap API using a Python script.
- Data transformation using Pandas to process the extracted data.
- Storage of the transformed data in an Azure Blob Storage container.
- ETL Sciprt wrapped inside azure function 'function_app.py' file
- Used CI/CD Yaml file to manage integration and deployment 
- use [Continuous delivery by using GitHub Actions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions?tabs=linux%2Cpython&pivots=method-manual) this link to follow the steps

## Azure Functions
Azure Functions are utilized to orchestrate the ETL process. The most common triggers used in the data pipeline are HTTP triggers, blob triggers, and timer triggers. In this case, the HTTP trigger is used to extract and transform the data from the Coincap API, and the blob trigger can be used to activate the function when a new file is added to the Azure Blob Storage.

## Deployment
The Azure Function extension in Visual Studio Code is used to author the function in Python. The `function_app.py` file contains the function code, and the required Python packages are listed in the `requirements.txt` file. The deployment of the function to the Azure Function App in the cloud is done using the Azure icon in VS Code and clicking the deploy button.

## Running the ETL Pipeline
Once the function is deployed and the triggers are set up, the ETL pipeline will run automatically based on the trigger conditions. The ETL process can be orchestrated and monitored through the Azure portal.

For detailed instructions on setting up and running the ETL pipeline, please refer to the code and comments in the provided Python script.

For further details and examples, you can refer to the [Azure-Samples/msdocs-python-etl-serverless](https://github.com/Azure-Samples/msdocs-python-etl-serverless) repository.

---
This readme provides an overview of the ETL pipeline that retrieves data from the Coincap API and stores it in an Azure Blob Storage using Azure Functions. For detailed instructions and examples, please refer to the provided code and external resources.
