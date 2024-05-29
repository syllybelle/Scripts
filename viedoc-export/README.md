# Viedoc Export Script

These Python and R scripts triggers and downloads exports from Viedoc EDC. They include functionalities to:
- Authenticate and obtain an access token.
- Initiate the export process.
- Check the status of the export.
- Download and optionally extract the exported files.

## Usage
To run the Viedoc Export Script, use the following command:

- For python: 

Install dependencies

```sh
pip install requests
```
Run:

```sh
python viedoc_export.py --token_url <TOKEN_URL> --api_url <API_URL> --client_id <CLIENT_ID> --client_secret <CLIENT_SECRET> --export_model <EXPORT_MODEL> [--output_path <OUTPUT_PATH>][--extract_zip Y/N] [--remove_prefix Y/N]
```
Example:

```sh
python viedoc_export.py --token_url "https://v4ststraining.viedoc.net/connect/token" --api_url "https://v4apitraining.viedoc.net" --client_id "84731234-1234-1234-1234-1234cf658d98" --client_secret "FAaaTZaxxxxxxxxxxxxxxxxxxxxxxJzfw" --export_model '{"outputFormat":"CSV","includeVisitDates":true}'
```

- For R:

Install dependencies:

```sh
Rscript -e 'install.packages(c("httr", "jsonlite", "logging", "argparse", "stringr", "tools", "zip"), repos = "https://cran.r-project.org")'
```
Run: 

```sh
Rscript viedoc_export.R --token_url <TOKEN_URL> --api_url <API_URL> --client_id <CLIENT_ID> --client_secret <CLIENT_SECRET> --export_model <EXPORT_MODEL> [--output_path <OUTPUT_PATH>] [--extract_zip Y/N] [--remove_prefix Y/N]
```

Example:
```sh
Rscript viedoc_export.R --token_url "https://v4ststraining.viedoc.net/connect/token" --api_url "https://v4apitraining.viedoc.net" --client_id "84731234-1234-1234-1234-1234cf658d98" --client_secret "FAaaTZaxxxxxxxxxxxxxxxxxxxxxxJzfw" --export_model '{"outputFormat":"CSV","includeVisitDates":true}'
```sh

## Arguments:
- --token_url: URL to get the authentication token.
- --api_url: Base URL for the Viedoc API.
- --client_id: Client ID for authentication.
- --client_secret: Client secret for authentication.
- --export_model: JSON string representing the export model. Ex. 

```
{"outputFormat":"CSV","includeVisitDates":false,"includeEditStatus":false,"includeSignatures":false,"includeReviewStatus":false,"includeSdv":false,"includeQueries":false,"includeQueryHistory":false,"includeSubjectStatus":false,"includePendingForms":false}"
```

- --extract_zip: (Optional) Extract the zip file if set to Y. Default is Y.
- --remove_prefix: (Optional) Remove the prefix from extracted files if set to Y. Default is Y.