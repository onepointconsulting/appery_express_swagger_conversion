from typing import Any
from jinja2 import Environment, FileSystemLoader


class Renderer:
    """
    Render a Jinja template

    Sets up Jinja renderer and renders one or more templates
    using provided context.

    * `render_template` renders a single template
    * `render_tree` renders all templates starting from a predefined
      root folder (which must reside inside templates folder structure)

    Rendered template(s) are returned as strings. Nothing is written
    to disk.

    Usage:

    >>> import Renderer from render
    >>> r = Renderer('path/to/templates')
    >>> output_string = r.render_template('template.html', {'key': 'value'})
    >>> output_tree = r.render_tree('tree/root', {'key': 'value'})
    """

    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False,
            lstrip_blocks=True,
            trim_blocks=True,
            keep_trailing_newline=True,
        )
        # Add filters here
        # self.jinja_env.filters["qstr"] = qstr

    def render_template(self, template: str, context: Any) -> str:
        """
        Render a single template to a string using provided context

        :param template: Name of the template file, relative to `template_dir`.
        :param context: Context to render the template with.
        :return: The resulting string.
        """

        # Jinja2 always uses /, even on Windows
        template = template.replace("\\", "/")

        tpl_object = self.jinja_env.get_template(template)
        return tpl_object.render(context)
