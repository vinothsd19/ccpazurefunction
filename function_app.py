import azure.functions as func
import logging
import pandas as pd
from azure.storage.blob import BlobServiceClient
import requests

logging.basicConfig(level=logging.INFO)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


def get_data():
    coincap_api_url = 'https://api.coincap.io/v2/assets'
    try:
        response = requests.get(coincap_api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()['data']
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching data from CoinCap API: {e}")
        return None

def transform_data(data):
    try:
        df = pd.DataFrame(data)
        cols = ['supply', 'rank', 'maxSupply', 'marketCapUsd', 'volumeUsd24Hr', 'priceUsd', 'changePercent24Hr', 'vwap24Hr']
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
        df = df.drop(['explorer'], axis=1)
        return df
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        return None

def save_df_to_azure_blob(account_name, account_key, container_name, blob_name, df):
    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient(account_url=f'https://{account_name}.blob.core.windows.net', credential=account_key)

    # Get a reference to the target container
    target_container_client = blob_service_client.get_container_client(container_name)

    # Convert the DataFrame to CSV format
    csv_content = df.to_csv(index=False)

    # Get a reference to the target blob
    target_blob_client = target_container_client.get_blob_client(blob_name)

    # Upload the transformed data to the target blob
    target_blob_client.upload_blob(csv_content, overwrite=True)


@app.route(route="http_trigger_vdh_blob")
def http_trigger_vdh_blob(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    account_name = 'coincapbatchetl'
    account_key = 'MvtIzGziZXCQnUXsIYj7oA2d8s2S5id65II+xsadT09aYWRXk48xI59MjrpeDrgz7MlBq+Wq3WQM+AStc0SlpA=='
    container_name = 'output'
    blob_name = 'coincap.csv'

    # Extract data from the CoinCap API
    extracted_data = get_data()

    if extracted_data:
        # Transform the extracted data
        transformed_data = transform_data(extracted_data)

        if transformed_data is not None:
            # Save the transformed data to Azure Blob Storage
            save_df_to_azure_blob(account_name, account_key, container_name, blob_name, transformed_data)
            return func.HttpResponse("ETL process completed successfully via CICD VDH Yes", status_code=200)
        else:
            return func.HttpResponse("Error occurred during data transformation", status_code=500)
    else:
        return func.HttpResponse("Error occurred during data extraction", status_code=500)