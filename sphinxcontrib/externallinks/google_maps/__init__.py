# -*- coding: utf-8 -*-

from . import embed

def setup(app):
    app.add_node(embed.googlemaps,
                 html=(embed.visit_googlemaps_node, embed.depart_googlemaps_node))
    app.add_directive("google-maps", embed.GoogleMapsDirective)
