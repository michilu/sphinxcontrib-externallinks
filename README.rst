sphinxcontrib.externallinks
===========================

Roles
-----

This module defines some roles.

`google` It takes a single, requiredargument, keywords for search::

    :google:`world heritage sites in japan`

`google-images` It takes a single, requiredargument, keywords for image search::

    :google-images:`world heritage sites in japan`

`google-maps-fromto` It takes a single, requiredargument, keywords for maps search::

    :google-maps-fromto:`from Mt.Fuji to Hiraizumi` by public transit
    :google-maps-fromto:`driving from Mt.Fuji to Hiraizumi` by car
    :google-maps-fromto:`walking from Mt.Fuji to Hiraizumi`

    :google-maps-fromto:`from Mt.Fuji to Hiraizumi <富士山,平泉町>` by public transit
    :google-maps-fromto:`driving from Mt.Fuji to Hiraizumi <富士山,平泉町,d>` by car
    :google-maps-fromto:`walking from Mt.Fuji to Hiraizumi <富士山,平泉町,w>`

`img-altfix` It takes a single, requiredargument, image url.
This example, `http://example.com/alt.png` is not none, so fail over `src` attribute to local file of `img` as example.com::

    :img-altfix:`http://example.com/alt.png`

`tenkipast` It takes a single, requiredargument, prefecture and date for the weather of the past in Japan(tenki.jp)::

    :tenkipast:`東京,2013/07/16`

`wikipedia` It takes a single, requiredargument, langage and keywords for wikipedia's url::

    :wikipedia:`ja,フィリピンのバロック様式教会群`

`whc` , `whct` and `whcl` It takes a single, requiredargument, number of UNESCO's World Heritage sites list or tentative list::

    :whc:`0662` Yakushima (list of World Heritage sites)
    :whct:`0370` Temples, Shrines and other structures of Ancient Kamakura (tentative list of World Heritage)
    :whcl:`ph` Philippines: Properties inscribed on the World Heritage List

Directives
----------

This module defines some directives.

Google Maps
^^^^^^^^^^^

`google-maps` It takes a single, requiredargument, keywords for maps search.

Default mode is `place`::

    .. google-maps:: Fisht Olympic Stadium, Sochi Russia

as::

    .. google-maps::
      :mode: place
      :q:    Fisht Olympic Stadium, Sochi Russia

other modes as below::

    .. google-maps::
      :mode:        directions
      :origin:      Oslo Norway
      :destination: Telemark Norway
      :avoid:       tolls|highways

    .. google-maps:: record stores in Seattle
      :mode: search

    .. google-maps::
      :mode:    view
      :center:  37.4218,-122.0840
      :zoom:    18
      :maptype: satellite

Modes:

- place
- directions
- search
- view

Optional parameters:

:width:     default 600
:height:    default 450
:q:
:mode:
:origin:
:destination:
:avoid:
:key:       Google API key
:center:
:zoom:
:maptype:
:language:
:region:

see the Google Maps Embed API: https://developers.google.com/maps/documentation/embed/guide


`google-maps-legacy` It takes a single, requiredargument, keywords for maps search::

    .. google-maps-legacy:: Yakushima
      :zoom: 10

    .. google-maps-legacy:: Philippines
      :latitude: 12.3
      :longtitude: 123.4
      :zoom: 5

    .. google-maps-legacy:: driving from Mt.Fuji to Hiraizumi
      :saddr: 富士山
      :daddr: 平泉町
      :dirflg: d
