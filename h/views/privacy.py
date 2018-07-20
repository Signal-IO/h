# -*- coding: utf-8 -*-

"""Help and documentation views."""

from __future__ import unicode_literals

import binascii
import os

from pyramid import httpexceptions as exc
from pyramid.view import view_config


@view_config(renderer='h:templates/privacy.html.jinja2', route_name='privacy')
def privacy_page(context, request):
    return {
        'embed_js_url': request.route_path('embed'),
        'is_privacy': True,
    }   

def _random_word():
    return binascii.hexlify(os.urandom(8))
