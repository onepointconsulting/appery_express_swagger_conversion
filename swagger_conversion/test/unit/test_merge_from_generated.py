from pathlib import Path
from swagger_conversion.swagger.merge_schemas import merge_from_generated, validate_file, post_process


def test_merge_from_generated():
    combined = merge_from_generated()
    assert combined is not None
    assert isinstance(combined, Path)
    validation_result = validate_file(combined)
    assert isinstance(validation_result, dict)
    post_processed = post_process(combined)
    assert post_processed.exists()
