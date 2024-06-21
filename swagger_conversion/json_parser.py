from typing import Generator
from pathlib import Path
import json


def parse_document(path: Path) -> Generator:
    assert path.exists(), f"Path {path} does not exist."
    json_text = path.read_text()
    json_content = json.loads(json_text)
    for child in json_content["root"]["children"]:
        child_children = child["children"]
        for second_child in child_children:
            for custom_rest in second_child["customRests"]:
                route_json_text = custom_rest["routeJson"]
                route_json = json.loads(route_json_text)
                yield {**custom_rest, "routeJson": route_json}
