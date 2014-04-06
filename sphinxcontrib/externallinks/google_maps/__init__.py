# -*- coding: utf-8 -*-

from . import embed
from . import embed_legacy

def setup(app):
    embed.setup(app)
    embed_legacy.setup(app)
