from docutils import nodes, utils
from functools import wraps
import urllib

from sphinx.util.nodes import split_explicit_title

def split_title(text):
    _has_explicit, title, other = split_explicit_title(utils.unescape(text))
    return title, other

def quote_plus(text):
    return urllib.quote_plus(text.encode("utf-8")).decode("utf-8")

def gen_role(func):

  @wraps(func)
  def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
      title, other = split_title(text)
      node = nodes.raw("", u"<a href='{url}'>{title}</a>".format(title=title, url=func(other)), format="html")
      return [node], []

  return role

def google_role(other):
    return u"https://www.google.com/search?q={query}".format(query=quote_plus(other))

def setup(app):
    app.add_role("google", gen_role(google_role))
