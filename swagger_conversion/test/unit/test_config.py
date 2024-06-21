from swagger_conversion.config import cfg


def test_config_values():
    assert cfg.openai_api_key is not None
    assert cfg.openai_api_model is not None
    assert cfg.openai_api_temperature is not None
