# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer

PAS_ID = 'disableuser'
PAS_TITLE = 'Disable User Plugin'
PROP_DISABLED = 'disabled'


class ICollectivedisableuserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
