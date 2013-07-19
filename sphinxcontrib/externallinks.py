# -*- coding: utf-8 -*-

from docutils import nodes, utils
from functools import wraps
from xml.sax import saxutils
import time
import urllib

from sphinx.util.nodes import split_explicit_title

def html_escape(value):
    return saxutils.escape(value, {"\'":"&apos;", "\"":"&quot;"})

def split_title(text):
    _has_explicit, title, other = split_explicit_title(utils.unescape(text))
    return title, other

def quote_plus(text):
    return urllib.quote_plus(text.encode("utf-8")).decode("utf-8")

def gen_role(func):

    @wraps(func)
    def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
        title, other = split_title(text)
        node = nodes.raw("", u"<a href='{url}'>{title}</a>".format(title=title, url=html_escape(func(other))), format="html")
        return [node], []

    return role

tenki_past_prefs = [u"n/a",u"道北",u"道央",u"道東",u"道南",u"青森",u"岩手",u"宮城",u"秋田",u"山形",u"福島",u"茨城",u"栃木",u"群馬",u"埼玉",u"千葉",u"東京",u"神奈川",u"山梨",u"長野",u"新潟",u"富山",u"石川",u"福井",u"岐阜",u"静岡",u"愛知",u"三重",u"滋賀",u"京都",u"大阪",u"兵庫",u"奈良",u"和歌山",u"鳥取",u"島根",u"岡山",u"広島",u"山口",u"徳島",u"香川",u"愛媛",u"高知",u"福岡",u"佐賀",u"長崎",u"熊本",u"大分",u"宮崎",u"鹿児島",u"沖縄"]
tenki_past_prefs_dict = dict((y,x) for x,y in enumerate(tenki_past_prefs))

def tenki_past(text):
    pref, date = text.split(u",", 1)
    pref_no = tenki_past_prefs_dict.get(pref, u"")
    year, month, day = time.strptime(date, u"%Y/%m/%d")[:3]
    return u"http://tenki.jp/past/detail/pref-{pref_no}.html?year={year}&month={month}&day={day}".format(pref_no=pref_no, year=year, month=month, day=day)

def setup(app):
    app.add_role("google", gen_role(lambda x:u"https://www.google.com/search?q={query}".format(query=quote_plus(x))))
    app.add_role("tenkipast", gen_role(tenki_past))
