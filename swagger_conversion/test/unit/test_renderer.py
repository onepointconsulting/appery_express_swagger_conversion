from swagger_conversion.templates.renderer import Renderer
from swagger_conversion.config import cfg


def test_renderer():
    renderer = Renderer(cfg.template_dir)
    res = renderer.render_template("swagger_conversion.prompt", {"json": "{}"})
    assert res is not None
    print(res)
    res = renderer.render_template("swagger_conversion_system.prompt", {})
    assert (
        res
        == "You are a code generator, specialized in generating either code or formats like JSON, YAML."
    )
