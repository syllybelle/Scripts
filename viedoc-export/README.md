# Viedoc Export Script

This Python script triggers and downloads exports from Viedoc EDC. It includes functionalities to:
- Authenticate and obtain an access token.
- Initiate the export process.
- Check the status of the export.
- Download and optionally extract the exported files.

## Usage

To run the Viedoc Export Script, use the following command:

```sh
python viedoc_export.py --token_url <TOKEN_URL> --api_url <API_URL> --client_id <CLIENT_ID> --client_secret <CLIENT_SECRET> --export_model <EXPORT_MODEL> [--extract_zip Y/N] [--remove_prefix Y/N]
```

## Arguments:
- --token_url: URL to get the authentication token.
- --api_url: Base URL for the Viedoc API.
- --client_id: Client ID for authentication.
- --client_secret: Client secret for authentication.
- --export_model: JSON string representing the export model.
- --extract_zip: (Optional) Extract the zip file if set to Y. Default is Y.
- --remove_prefix: (Optional) Remove the prefix from extracted files if set to Y. Default is Y.