# Viedoc Export Script

These Python and R scripts trigger and download exports from Viedoc EDC. They include functionalities to:
- Authenticate and obtain an access token.
- Initiate the export process.
- Check the status of the export.
- Download and optionally extract the exported files.

For multi-study Python runs, see [multistudy_ingest.md](./multistudy_ingest.md).

## Endpoint reference

This tool uses the Viedoc Web API and its STS token endpoint.

The source of truth for the API base URL and STS URL remains:

- the exact values shown during API client setup in Viedoc Admin
- the endpoint lists published by Viedoc Help: <https://help.viedoc.net/l/debc54/>

For the repository reference list of Viedoc UI, Web API, STS, Swagger, and WCF URLs, see [../viedoc-api-endpoints.yaml](../viedoc-api-endpoints.yaml).

## Usage
To run the Viedoc Export Script, use the following command:

- For python: 

Install dependencies

```sh
pip install -r requirements.txt
```
Run:

```sh
python viedoc_export.py --token_url <TOKEN_URL> --api_url <API_URL> --client_id <CLIENT_ID> --client_secret <CLIENT_SECRET> --export_model <EXPORT_MODEL_OR_JSON_FILE> [--output_path <OUTPUT_DIR>] [--extract_zip Y/N] [--remove_prefix Y/N]
```
Examples:

```sh
python viedoc_export.py --token_url "https://v4ststraining.viedoc.net/connect/token" --api_url "https://v4apitraining.viedoc.net" --client_id "84731234-1234-1234-1234-1234cf658d98" --client_secret "FAaaTZaxxxxxxxxxxxxxxxxxxxxxxJzfw" --export_model '{"outputFormat":"CSV","includeVisitDates":true}'
```

```sh
python viedoc_export.py --token_url "https://v4ststraining.viedoc.net/connect/token" --api_url "https://v4apitraining.viedoc.net" --client_id "84731234-1234-1234-1234-1234cf658d98" --client_secret "FAaaTZaxxxxxxxxxxxxxxxxxxxxxxJzfw" --export_model export_model.example.json --output_path "C:/Users/<you>/ViedocExports"
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
- --export_model: Inline JSON, a JSON file path, or `@path/to/file.json`. For less error-prone runs, start from [export_model.example.json](./export_model.example.json).
- --output_path: Output directory. Defaults to `out`.
- --extract_zip: (Optional) Extract the zip file if set to Y. Default is Y.
- --remove_prefix: (Optional) Remove the download filename prefix from extracted files if set to Y. Default is Y.
- --timeout_seconds: (Optional) Per-request timeout. Default is 60.
- --poll_interval_seconds: (Optional) Seconds between export status checks. Default is 10.
- --max_wait_seconds: (Optional) Maximum total wait time for the export to become ready. Default is 600.

```
{"outputFormat":"CSV","includeVisitDates":false,"includeEditStatus":false,"includeSignatures":false,"includeReviewStatus":false,"includeSdv":false,"includeQueries":false,"includeQueryHistory":false,"includeSubjectStatus":false,"includePendingForms":false}
```
