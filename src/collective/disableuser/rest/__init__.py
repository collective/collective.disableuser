# -*- coding: utf-8 -*-
from collective.disableuser import PAS_ID
from persistent.list import PersistentList
from plone import api
from plone.restapi.services import Service
from zope.interface import alsoProvides

import json
import plone


def get_disabled_userids(self):
    membership = api.portal.get_tool('portal_membership')
    disabled_member_ids = [
        member.getId() for member in membership.listMembers()
        if member.getProperty("disabled", False)
    ]
    return disabled_member_ids


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
            user.setMemberProperties(
                mapping={'disabled': disabled, }
            )

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

        membership = api.portal.get_tool('portal_membership')
        for member in membership.listMembers():
            member.setMemberProperties(
                mapping={'disabled': member.getId() in disabled_userids}
            )

        return json.dumps(get_disabled_userids(self))


class Delete(Service):
    """ Clears the list of disabled users
    """

    def reply(self):
        membership = api.portal.get_tool('portal_membership')
        for member in membership.listMembers():
            if not member.getProperty('disabled', False):
                continue
            member.setMemberProperties(
                mapping={'disabled', False}
            )

        return json.dumps(get_disabled_userids(self))
