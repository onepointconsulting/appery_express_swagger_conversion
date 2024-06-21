import click
import json
import asyncio
from pathlib import Path
from enum import StrEnum

from swagger_conversion.templates.renderer import Renderer
from swagger_conversion.json_parser import parse_document
from swagger_conversion.llm.openai_client import OpenAIClient
from swagger_conversion.model.message_container import MessageContainer
from swagger_conversion.templates.renderer import Renderer
from swagger_conversion.model.function_description import function_description_swagger_result
from swagger_conversion.config import cfg
from swagger_conversion.log_init import logger


class GenType(StrEnum):
    TYPE_SWAGGER = "swagger"


@click.command()
@click.option(
    "--type",
    prompt="The type of the conversion",
    default=GenType.TYPE_SWAGGER,
    help="The type of conversion",
)
@click.option(
    "--location",
    prompt="The location of the JSON file",
    help="The location of the JSON file",
)
@click.option(
    "--target_folder",
    prompt="The target folder into which the ",
    help="The location of the JSON file",
)
def swagger_conversion(type: str, location: str, target_folder: str):
    """Simple program that generates swagger definitions"""
    click.echo(f"Starting generation from {location} for {type}.")
    match type:
        case GenType.TYPE_SWAGGER:
            click.echo(f"Detected {type}.")
            renderer = Renderer(cfg.template_dir)
            swagger_conversion_system = renderer.render_template("swagger_conversion_system.prompt", {})
            
            json_path = Path(location)
            assert json_path.exists, f"Could not find {json_path}. Is the path correct?"

            target_folder_path = Path(target_folder)
            if not target_folder_path.exists():
                target_folder_path.mkdir(parents=True, exist_ok=True)
                assert target_folder_path.exists(), f"{target_folder_path} does not exist."

            click.echo(f"{json_path} exists.")
            api = OpenAIClient()
            for i, json_doc in enumerate(parse_document(json_path)):
                res = renderer.render_template("swagger_conversion.prompt", {"json": json.dumps(json_doc)})
                message = MessageContainer(swagger_conversion_system)
                message.user(res)
                try:
                    response = asyncio.run(api.make_request(message, functions=[function_description_swagger_result]))
                    json_response = json.loads(response[0])
                    description = json_response["description"]
                    (target_folder_path/f"swagger_{i}.yaml").write_text(json_response["swagger_definition"])
                    (target_folder_path/f"swagger_{i}_description.txt").write_text(description)
                    logger.info(f"Generated service nr. {i}: {description}")
                except Exception as e:
                    logger.exception(f"Cannot process {i} definition.")

        case _:
            click.echo(f"Unrecognized type {type}. Please use one of {GenType.TYPE_SWAGGER}")


if __name__ == "__main__":
    swagger_conversion()
