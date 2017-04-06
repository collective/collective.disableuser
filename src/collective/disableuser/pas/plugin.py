# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from AccessControl.SecurityInfo import ClassSecurityInfo
from persistent.list import PersistentList
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import \
    IAuthenticationPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.statusmessages.interfaces import IStatusMessage
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

_ = MessageFactory('collective.disableuser.pas')


manage_addDisableUserPlugin = PageTemplateFile(
    "add_plugin", globals(), __name__="manage_addDisableUserPlugin")


def addDisableUserPlugin(self, id_, title=None, REQUEST=None):
    """Add a Disabled User authentication plugin
    """
    plugin = DisableUserPlugin(id_, title)
    self._setObject(plugin.getId(), plugin)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect(
            "%s/manage_workspace"
            "?manage_tabs_message=DisableUser+plugin+added." %
            self.absolute_url()
        )


class DisableUserPlugin(BasePlugin):
    """Plone PAS plugin to block disabled users
    """
    implements(IAuthenticationPlugin)
    meta_type = "Disable User Plugin"
    security = ClassSecurityInfo()

    def __init__(self, id_, title=None):
        self._setId(id_)
        self.title = title
        self.disabled_user_ids = PersistentList()


    security.declarePrivate('authenticateCredentials')

    # IAuthenticationPlugin implementation
    def authenticateCredentials(self, credentials):
        if self.is_disabled(credentials):
            messages = IStatusMessage(self.REQUEST)
            msg = _("Your account is disabled.")
            messages.add(msg, type="error")
            raise Unauthorized(msg)

    security.declarePrivate('is_disabled')

    def is_disabled(self, credentials):
        for user_id in self._get_userids(credentials):
            if user_id in self.disabled_user_ids:
                return True

    security.declarePrivate('_get_userids')
    def _get_userids(self, credentials):
        userids = []
        pas = self._getPAS()
        authenticators = pas.plugins.listPlugins(IAuthenticationPlugin)

        for authenticator_id, auth in authenticators:
            if auth.getId() is self.getId():
                continue
            uid_and_info = auth.authenticateCredentials(credentials)
            if uid_and_info is None:
                continue
            user_id, info = uid_and_info
            userids.append(user_id)

        return userids
