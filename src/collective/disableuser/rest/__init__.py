# -*- coding: utf-8 -*-
from collective.disableuser import PAS_ID
from persistent.list import PersistentList
from plone import api
from plone.restapi.services import Service
from zope.interface import alsoProvides

import json
import plone


class Get(Service):
    """ Lists all disabled users
    """

    def reply(self):
        acl = api.portal.get_tool('acl_users')
        plugin = acl[PAS_ID]
        return json.dumps(list(plugin.disabled_user_ids))


class Patch(Service):
    """ Updates the list of disabled users
    """

    def reply(self):
        acl = api.portal.get_tool('acl_users')
        plugin = acl[PAS_ID]
        data = json.loads(self.request.get('BODY', '{}'))  # noqa: P103

        for userid, disabled in data.items():
            if disabled:
                if userid not in plugin.disabled_user_ids:
                    plugin.disabled_user_ids.append(userid)
            else:
                if userid in plugin.disabled_user_ids:
                    plugin.disabled_user_ids.remove(userid)

        return json.dumps(list(plugin.disabled_user_ids))


class Post(Service):
    """ Sets the list of disabled users
    """

    def reply(self):
        # Disable CSRF protection
        if 'IDisableCSRFProtection' in dir(plone.protect.interfaces):
            alsoProvides(self.request,
                         plone.protect.interfaces.IDisableCSRFProtection)

        acl = api.portal.get_tool('acl_users')
        plugin = acl[PAS_ID]
        data = json.loads(self.request.get('BODY', '{}'))  # noqa: P103

        disabled_userids = [
            userid for userid, disabled in data.items() if disabled
        ]

        plugin.disabled_user_ids = PersistentList(disabled_userids)
        return json.dumps(list(plugin.disabled_user_ids))


class Delete(Service):
    """ Clears the list of disabled users
    """

    def reply(self):
        acl = api.portal.get_tool('acl_users')
        plugin = acl[PAS_ID]

        plugin.disabled_user_ids = PersistentList()
        return json.dumps(list(plugin.disabled_user_ids))
