# Apery API Export Conversion

Used to convert Appery Express exports into OpenAPI Swagger definitions.

## Install

Create a Conda environmeent first with:

```bash
conda create -n swagger_conversion python=3.12 -y
conda activate swagger_conversion
pip install poetry
poetry install
```

## Running 

If you want to generate directly swagger files:

```bash
python .\swagger_conversion\cli\main.py --type swagger --location /development/bk/ukstats/swagger_conversion/docs/appery_api_express_export.json --target_folder /development/bk/ukstats/swagger_conversion/generated
```