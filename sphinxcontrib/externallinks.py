from docutils import nodes, utils
import urllib

from sphinx.util.nodes import split_explicit_title

URL = u"https://www.google.com/search?q={query}"

def split_title(text):
    _has_explicit, title, other = split_explicit_title(utils.unescape(text))
    return title, other

def quote_plus(text):
    return urllib.quote_plus(text.encode("utf-8")).decode("utf-8")

def google_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to Google search.
    """
    title, other = split_title(text)
    query = quote_plus(other)
    url = URL.format(query=query)
    node = nodes.raw("", u"<a href='{url}'>{title}</a>".format(title=title, url=url), format="html")
    return [node], []

def setup(app):
    app.add_role("google", google_role)
