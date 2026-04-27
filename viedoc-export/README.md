# Viedoc Export Script

These Python and R scripts trigger and download exports from Viedoc EDC. They include functionalities to:
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
python viedoc_export.py --token_url <TOKEN_URL> --api_url <API_URL> --client_id <CLIENT_ID> --client_secret <CLIENT_SECRET> --export_model <EXPORT_MODEL_OR_JSON_FILE> [--output_path <OUTPUT_DIR>] [--extract_zip Y/N] [--remove_prefix Y/N]
```
Examples:

```sh
python viedoc_export.py --token_url "https://v4ststraining.viedoc.net/connect/token" --api_url "https://v4apitraining.viedoc.net" --client_id "84731234-1234-1234-1234-1234cf658d98" --client_secret "FAaaTZaxxxxxxxxxxxxxxxxxxxxxxJzfw" --export_model '{"outputFormat":"CSV","includeVisitDates":true}'
```

```sh
python viedoc_export.py --token_url "https://v4ststraining.viedoc.net/connect/token" --api_url "https://v4apitraining.viedoc.net" --client_id "84731234-1234-1234-1234-1234cf658d98" --client_secret "FAaaTZaxxxxxxxxxxxxxxxxxxxxxxJzfw" --export_model @export_model.example.json --output_path "C:/Users/<you>/ViedocExports"
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

### Shell Quoting Notes

The `--export_model` parameter accepts JSON. Proper quoting depends on your shell:

**Linux/macOS (bash/zsh):**
```sh
python viedoc_export.py ... --export_model '{"outputFormat":"CSV"}'
```
Use single quotes to preserve double quotes in the JSON.

**Windows (PowerShell):**
```powershell
python viedoc_export.py ... --export_model '{\"outputFormat\":\"CSV\"}'
```
Escape inner double quotes with backslashes, or use:
```powershell
python viedoc_export.py ... --export_model "{'outputFormat':'CSV'}"
```

**Windows (cmd.exe):**
```cmd
python viedoc_export.py ... --export_model "{\"outputFormat\":\"CSV\"}"
```
Escape inner double quotes with backslashes.

**Recommended approach (all platforms):**
Use a JSON file to avoid quoting issues entirely:
```sh
python viedoc_export.py ... --export_model export_model.json
```
or
```sh
python viedoc_export.py ... --export_model @export_model.json
```

Example JSON file:
```
{"outputFormat":"CSV","includeVisitDates":false,"includeEditStatus":false,"includeSignatures":false,"includeReviewStatus":false,"includeSdv":false,"includeQueries":false,"includeQueryHistory":false,"includeSubjectStatus":false,"includePendingForms":false}
```
