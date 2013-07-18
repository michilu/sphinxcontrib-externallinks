from docutils import nodes, utils
import urllib

from sphinx.util.nodes import split_explicit_title

def goolge_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to Google search.
    """
    _has_explicit, title, keywords = split_explicit_title(utils.unescape(text))
    query = urllib.quote_plus(keywords.encode("utf-8")).decode("utf-8")
    base = u"<a href='https://www.google.com/search?q={query}'>{title}</a>"
    node = nodes.raw("", base.format(title=title, query=query), format="html")
    return [node], []

def setup(app):
    app.add_role("google", goolge_role)
