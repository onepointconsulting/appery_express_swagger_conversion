from swagger_conversion.swagger.validate_schema import validate_schema
from swagger_conversion.config import cfg


def test_validate():
    examples = cfg.project_folder / "docs/examples"
    assert examples.exists()
    validation_files = list(examples.glob("*.yaml"))
    assert len(validation_files) > 0
    for validation_file in validation_files:
        mapping = validate_schema(validation_file)
        assert mapping is not None
