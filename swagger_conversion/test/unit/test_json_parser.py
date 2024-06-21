import json
from swagger_conversion.json_parser import parse_document
from swagger_conversion.config import cfg


def test_json_parser():
    appery_api_express_export = (
        cfg.project_folder / "docs/appery_api_express_export.json"
    )
    assert appery_api_express_export.exists()
    for json_doc in parse_document(appery_api_express_export):
        print(json.dumps(json_doc, indent=4))
