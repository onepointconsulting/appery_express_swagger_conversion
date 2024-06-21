import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key is not None
    openai_api_model = os.getenv("OPENAI_API_MODEL", "gpt-4-turbo")
    assert openai_api_model is not None
    openai_api_temperature = float(os.getenv("OPENAI_API_TEMPERATURE", "0.0"))
    assert openai_api_temperature is not None

    project_folder = Path(os.getenv("PROJECT_FOLDER"))
    assert project_folder.exists(), f"Project folder {project_folder} does not exist."

    connect_timeout = float(os.getenv("CONNECT_TIMEOUT", 60))
    assert connect_timeout > 0, f"Read timeout should be greater than 0"
    read_timeout = float(os.getenv("READ_TIMEOUT", 10))
    assert read_timeout > 0, f"Connect timeout should be greater than 0"

    template_dir = os.getenv("TEMPLATE_DIR")
    assert template_dir is not None, "Template directory was not defined."


cfg = Config()
