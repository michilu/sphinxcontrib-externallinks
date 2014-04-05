# -*- coding: utf-8 -*-

from docutils import nodes, utils
from functools import wraps
from xml.sax import saxutils
import os.path
import re
import subprocess
import time
import urllib

from sphinx.util.nodes import split_explicit_title

re_IMG_ALTFIX = re.compile(r":img-altfix:`.+?`")
re_IMG_ALTFIX_TAG = re.compile(r"^:img-altfix:`")
re_WHC = re.compile(r"^0+")

def html_escape(value):
    return saxutils.escape(value, {"\'":"&apos;", "\"":"&quot;"})

def quote_plus(text):
    return urllib.quote_plus(text.encode("utf-8")).decode("utf-8")

def gen_role(func, use_explicit=False):

    @wraps(func)
    def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
        has_explicit, title, other = split_explicit_title(utils.unescape(text))
        args = [other]
        if use_explicit:
            args.append(has_explicit)
        result = func(*args)
        if isinstance(result, (list, tuple)):
            url, title = result
        else:
            url = result
        node = nodes.raw("", u"<a href='{url}'>{title}</a>".format(title=title, url=html_escape(url)), format="html")
        return [node], []

    return role

tenki_past_prefs = [u"n/a",u"道北",u"道央",u"道東",u"道南",u"青森",u"岩手",u"宮城",u"秋田",u"山形",u"福島",u"茨城",u"栃木",u"群馬",u"埼玉",u"千葉",u"東京",u"神奈川",u"山梨",u"長野",u"新潟",u"富山",u"石川",u"福井",u"岐阜",u"静岡",u"愛知",u"三重",u"滋賀",u"京都",u"大阪",u"兵庫",u"奈良",u"和歌山",u"鳥取",u"島根",u"岡山",u"広島",u"山口",u"徳島",u"香川",u"愛媛",u"高知",u"福岡",u"佐賀",u"長崎",u"熊本",u"大分",u"宮崎",u"鹿児島",u"沖縄"]
tenki_past_prefs_dict = dict((y,x) for x,y in enumerate(tenki_past_prefs))

def google_maps_fromto(text, has_explicit):
    if has_explicit:
        texts = text.split(u",", 2) + [""] * 3
        saddr, daddr, dirflg = texts[:3]
    else:
        assert "from " in text
        assert " to " in text.split("from ", 1)[-1]
        if not text.startswith("from "):
            dirflg = text[0].lower()
        else:
            dirflg = "r"
        saddr = text.split("from ", 1)[-1].split(" to ")[0]
        daddr = text.split(" to ", 1)[-1]
    return u"https://maps.google.com/maps?saddr={saddr}&daddr={daddr}&dirflg={dirflg}".format(saddr=saddr, daddr=daddr, dirflg=dirflg)

def set_img_altfix_base(app, _docname, source):
    source[0] = re_IMG_ALTFIX.sub(
        lambda matchobj: re_IMG_ALTFIX_TAG.sub(":img-altfix:`{0},".format(app.config.img_altfix_base), matchobj.group()),
        source[0])

def img_altfix(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    img_altfix_base, text = text.split(",", 1)
    has_explicit, alt, src = split_explicit_title(utils.unescape(text))
    basename = os.path.basename(src)
    if not has_explicit:
        alt = basename
    output = subprocess.check_output(["find", "-L", ".", "-name", basename], cwd=img_altfix_base)
    template = u"<img src='{src}' alt='{alt}'{altfix}>"
    altfix = ""
    for line in output.splitlines():
        altfix = u" onerror='this.onerror=null;delete this.onerror;this.src=\"{0}\";'".format(html_escape(line.lstrip(".")))
        break
    node = nodes.raw("", template.format(src=html_escape(src), alt=html_escape(alt), altfix=altfix), format="html")
    return [node], []

def tenki_past(text):
    pref, date = text.split(u",", 1)
    pref_no = tenki_past_prefs_dict.get(pref, u"")
    year, month, day = time.strptime(date, u"%Y/%m/%d")[:3]
    return u"http://tenki.jp/past/detail/pref-{pref_no}.html?year={year}&month={month}&day={day}".format(pref_no=pref_no, year=year, month=month, day=day)

def wikipedia(text):
    lang, query = text.split(",", 1)
    return u"http://{lang}.wikipedia.org/wiki/{query}".format(lang=lang, query=quote_plus(query)), query

def setup(app):
    app.add_role("google", gen_role(lambda x:u"https://www.google.com/search?q={query}".format(query=quote_plus(x))))
    app.add_role("google-images", gen_role(lambda x:u"https://www.google.com/search?q={query}&tbm=isch".format(query=quote_plus(x))))
    app.add_role("google-maps-fromto", gen_role(google_maps_fromto, use_explicit=True))
    app.add_role("tenkipast", gen_role(tenki_past))
    app.add_role("wikipedia", gen_role(wikipedia))
    app.add_role("whc", gen_role(lambda x:u"http://whc.unesco.org/en/list/{query}".format(query=quote_plus(re_WHC.sub("", x)))))
    app.add_role("whcl", gen_role(lambda x:u"http://whc.unesco.org/en/statesparties/{query}".format(query=x)))
    app.add_role("whct", gen_role(lambda x:u"http://whc.unesco.org/en/tentativelists/{query}".format(query=quote_plus(re_WHC.sub("", x)))))

    app.add_config_value("img_altfix_base", None, "env")
    app.connect('source-read', set_img_altfix_base)
    app.add_role("img-altfix", img_altfix)

