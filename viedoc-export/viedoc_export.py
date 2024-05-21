import argparse  # For parsing command-line arguments
import io  # For handling byte streams
import zipfile  # For handling zip files
import requests  # For making HTTP requests
import time  # For adding delays
import re  # For regular expression operations
import os  # For file and directory operations
import logging  # For logging information

# Configure logging to display info messages with a specific format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_token(url, client_id, client_secret):
    """
    Request an access token from the authentication server.
    
    Args:
    - url (str): URL to get the token from.
    - client_id (str): Client ID for authentication.
    - client_secret (str): Client secret for authentication.
    
    Returns:
    - str: Access token.
    """
    logging.info("Getting token...")
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()["access_token"]

def start_export(url, token, export_model):
    """
    Start the export process.

    Args:
    - url (str): URL to start the export.
    - token (str): Access token for authorization.
    - export_model (str): JSON string representing the export model.
    
    Returns:
    - str: Export ID.
    """
    logging.info("Starting export...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=export_model)
    
    if response.status_code > 399:
        logging.info("Error: %s", response.text)
        response.raise_for_status()  # Raise an exception for HTTP errors
    
    return response.json()["exportId"]

def check_export_status(url, token, export_id):
    """
    Check the status of the export until it's ready.

    Args:
    - url (str): URL to check the export status.
    - token (str): Access token for authorization.
    - export_id (str): ID of the export to check.
    """
    logging.info("Checking export status...")
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        response = requests.get(f"{url}?exportId={export_id}", headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        status = response.json()["exportStatus"]

        logging.info("Export status: %s", status)

        if status == "Error":
            raise Exception("Export failed")  # Raise an exception if the export failed

        if status == "Ready":
            return  # Exit the loop if the export is ready
        logging.info("Sleeping...")
        time.sleep(10)  # Wait for 10 seconds before checking again

def download_export(url, token, export_id, extract_zip, remove_prefix):
    """
    Download the export file and optionally extract it.

    Args:
    - url (str): URL to download the export.
    - token (str): Access token for authorization.
    - export_id (str): ID of the export to download.
    - extract_zip (bool): Whether to extract the zip file.
    - remove_prefix (bool): Whether to remove the prefix from extracted files.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}?exportId={export_id}", headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Extract the filename from the Content-Disposition header
    content_disposition_header = response.headers.get("Content-Disposition")
    filename = re.search("filename=(.+)", content_disposition_header).group(1)

    # Create the 'out' folder if it doesn't exist
    if not os.path.exists("out"):
        os.makedirs("out")

    folder_path = "out"

    logging.info("Folder path: %s", folder_path)

    # If the filename is .zip and extract_zip is True, extract the file
    if filename.endswith(".zip") and extract_zip:
        logging.info("Extracting zip file...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(folder_path)
        logging.info("File extracted successfully!")

        # Remove the prefix from the extracted files if required
        if remove_prefix:
            zip_filename_without_extension = os.path.splitext(filename)[0]
            extracted_files = os.listdir(folder_path)

            for file in extracted_files:
                if file.startswith(zip_filename_without_extension):
                    new_filename = file[len(zip_filename_without_extension):].lstrip("_")
                    new_file_path = os.path.join(folder_path, new_filename)
                    if os.path.exists(new_file_path):
                        os.remove(new_file_path)
                    os.rename(os.path.join(folder_path, file), new_file_path)
        return
    else:
        # Save the file to out/filename
        with open(os.path.join(folder_path, filename), "wb") as f:
            f.write(response.content)

def main(token_url, api_url, client_id, client_secret, export_model, extract_zip, remove_prefix):
    """
    Main function to execute the export process.

    Args:
    - token_url (str): URL to get the token.
    - api_url (str): Base API URL.
    - client_id (str): Client ID for authentication.
    - client_secret (str): Client secret for authentication.
    - export_model (str): JSON string representing the export model.
    - extract_zip (bool): Whether to extract the zip file.
    - remove_prefix (bool): Whether to remove the prefix from extracted files.
    
    Example export mode:
    {"outputFormat":"CSV","includeVisitDates":true,"includeEditStatus":true,"includeSignatures":true,"includeReviewStatus":true,"includeSdv":true,"includeQueries":true,"includeQueryHistory":true,"includeSubjectStatus":true,"includePendingForms":true}"
    """
    logging.info("ViedocExport@1")

    start_export_url = api_url + "/clinic/dataexport/start"
    check_status_url = api_url + "/clinic/dataexport/status"
    download_url = api_url + "/clinic/dataexport/download"

    logging.info("Token URL: %s", token_url)
    logging.info("Start export URL: %s", start_export_url)
    logging.info("Check status URL: %s", check_status_url)
    logging.info("Download URL: %s", download_url)

    # Log only the first 3 characters of the client_id and client_secret for security
    logging.info("Client ID: %s", client_id[:3] + '*' * (len(client_id) - 3))
    logging.info("Client secret: %s", client_secret[:3] + '*' * (len(client_secret) - 3))
    logging.info("Export model: %s", export_model)
    
    # Get the access token
    token = get_token(token_url, client_id, client_secret)

    # Start the export process
    export_id = start_export(start_export_url, token, export_model)
    logging.info("Export ID: %s", export_id)

    # Check the export status until it's ready
    check_export_status(check_status_url, token, export_id)
    
    # Download the export file
    download_export(download_url, token, export_id, extract_zip, remove_prefix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Viedoc export script")
    
    # Define command-line arguments
    parser.add_argument("--token_url", required=True, help="Token URL")
    parser.add_argument("--api_url", required=True, help="API URL")
    parser.add_argument("--client_id", required=True, help="Client ID")
    parser.add_argument("--client_secret", required=True, help="Client secret")
    parser.add_argument("--export_model", required=True, help="Export model")
    parser.add_argument("--extract_zip", required=False, default="Y", choices=["Y", "N"], help="Extract zip file (Y/N)")
    parser.add_argument("--remove_prefix", required=False, default="Y", choices=["Y", "N"], help="Remove prefix from extracted files (Y/N)")

    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.token_url, args.api_url, args.client_id, args.client_secret, args.export_model, args.extract_zip == "Y", args.remove_prefix == "Y")
