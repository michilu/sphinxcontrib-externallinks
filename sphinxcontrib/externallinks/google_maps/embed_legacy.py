# -*- coding: utf-8 -*-

import urllib

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.util.compat import Directive

class googlemaps_legacy(nodes.General, nodes.Element):
    pass

class GoogleMapsDirective(Directive):
    """Directive for embedding google-maps"""

    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "lang": unicode,
        "saddr": unicode,
        "daddr": unicode,
        "dirflg": directives.single_char_or_unicode,
        "latitude": float,
        "longtitude": float,
        "zoom": directives.nonnegative_int,
    }

    def run(self):
        node = googlemaps_legacy()
        if self.arguments:
            node["query"] = " ".join(self.arguments)
        for key in self.option_spec.keys():
            if self.options.has_key(key):
                node[key] = self.options[key]
        return [node]


def visit_googlemaps_node(self, node):
    params = dict(f="q",
                  t="m",
                  om=0,
                  ie="UTF8",
                  oe="UTF8",
                  output="embed")

    if "lang" in node:
        params["hl"] = node["lang"].encode("utf-8")
    if "query" in node:
        params["q"] = node["query"].encode("utf-8")
    if "saddr" in node:
        params["saddr"] = node["saddr"].encode("utf-8")
    if "daddr" in node:
        params["daddr"] = node["daddr"].encode("utf-8")
    if "dirflg" in node:
        params["dirflg"] = node["dirflg"].encode("utf-8")
    if "latitude" in node and "longtitude" in node:
        params["ll"] = "%f,%f" % (node["latitude"], node["longtitude"])
    if "zoom" in node:
        params["z"] = str(node["zoom"])

    baseurl = "http://maps.google.com/maps?"
    iframe = """<iframe width="600" height="350" frameborder="0"
                        scrolling="no" marginheight="0"
                        marginwidth="0" src="%s">
                </iframe>"""

    url = baseurl + urllib.urlencode(params)
    self.body.append(iframe % url)

def depart_googlemaps_node(self, node):
    pass

def setup(app):
    app.add_node(googlemaps_legacy,
                 html=(visit_googlemaps_node, depart_googlemaps_node))
    app.add_directive("google-maps-legacy", GoogleMapsDirective)
