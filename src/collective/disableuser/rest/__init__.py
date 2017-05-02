# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.services import Service
from zope.interface import alsoProvides

import json
import plone

from collective.disableuser.interfaces import PROP_DISABLED


def get_disabled_userids(self):
    disabled_userids = [
        user.getId() for user in api.user.get_users()
        if user.getProperty(PROP_DISABLED, False)
    ]
    return disabled_userids


class Get(Service):
    """ Lists all disabled users
    """

    def reply(self):
        return json.dumps(get_disabled_userids(self))


class Patch(Service):
    """ Updates the list of disabled users
    """

    def reply(self):
        data = json.loads(self.request.get('BODY', '{}'))  # noqa: P103

        for userid, disabled in data.items():
            user = api.user.get(userid=userid)
            user.setMemberProperties(mapping={PROP_DISABLED: disabled})

        return json.dumps(get_disabled_userids(self))


class Post(Service):
    """ Sets the list of disabled users
    """

    def reply(self):
        # Disable CSRF protection
        if 'IDisableCSRFProtection' in dir(plone.protect.interfaces):
            alsoProvides(self.request,
                         plone.protect.interfaces.IDisableCSRFProtection)

        data = json.loads(self.request.get('BODY', '{}'))  # noqa: P103

        disabled_userids = [
            userid for userid, disabled in data.items() if disabled
        ]

        for user in api.user.get_users():
            disabled = user.getId() in disabled_userids
            user.setMemberProperties(mapping={PROP_DISABLED: disabled})

        return json.dumps(get_disabled_userids(self))


class Delete(Service):
    """ Clears the list of disabled users
    """

    def reply(self):
        for user in api.user.get_users():
            if not user.getProperty(PROP_DISABLED, False):
                continue
            user.setMemberProperties(mapping={PROP_DISABLED: False})

        return json.dumps(get_disabled_userids(self))
