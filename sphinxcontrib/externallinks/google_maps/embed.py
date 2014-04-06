# -*- coding: utf-8 -*-

import urllib

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.util.compat import Directive

IFRAME_TAG = """\
<iframe
  width="{width}"
  height="{height}"
  frameborder="0" style="border:0"
  src="https://www.google.com/maps/embed/v1/{mode}?{query}">
</iframe>\
"""

class googlemaps(nodes.General, nodes.Element):
    pass

class GoogleMapsDirective(Directive):
    """Directive for embedding google-maps"""

    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "width": directives.unchanged,
        "height": directives.unchanged,
        "q": directives.unchanged,
        "mode": directives.unchanged,
        "origin": directives.unchanged,
        "destination": directives.unchanged,
        "avoid": directives.unchanged,
        "key": directives.unchanged,
        "center": directives.unchanged,
        "zoom": directives.unchanged,
        "maptype": directives.unchanged,
        "language": directives.unchanged,
        "region": directives.unchanged,
    }

    def run(self):
        node = googlemaps()
        if self.arguments:
            node["q"] = " ".join(self.arguments)
        for key, value in self.options.items():
            node[key] = value
        return [node]

def make_visit_googlemaps_node(app):

    def visit_googlemaps_node(self, node):
        options = dict()
        for key, value in node.attlist():
          options[key] = node[key]
        width = options.pop("width", 600)
        height = options.pop("height", 450)
        mode = options.pop("mode", "place")
        options["key"] = app.config.google_api_key
        self.body.append(IFRAME_TAG.format(width=width, height=height, mode=mode,
                                         query=urllib.urlencode(options)))

    return visit_googlemaps_node

def depart_googlemaps_node(self, node):
    pass

def setup(app):
    app.add_config_value("google_api_key", None, "env")
    app.add_node(googlemaps,
                 html=(make_visit_googlemaps_node(app), depart_googlemaps_node))
    app.add_directive("google-maps", GoogleMapsDirective)
