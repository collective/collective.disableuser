# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from AccessControl.SecurityInfo import ClassSecurityInfo
from persistent.list import PersistentList
from plone import api
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin  # NOQA
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer

_ = MessageFactory('collective.disableuser.pas')


manage_addDisableUserPlugin = PageTemplateFile(
    'add_plugin', globals(), __name__='manage_addDisableUserPlugin')


def addDisableUserPlugin(self, id_, title=None, REQUEST=None):
    """Add a Disabled User authentication plugin
    """
    plugin = DisableUserPlugin(id_, title)
    self._setObject(plugin.getId(), plugin)

    if REQUEST is not None:
        url = '{0}/manage_workspace' + \
              '?manage_tabs_message=DisableUser+plugin+added.'
        REQUEST['RESPONSE'].redirect(
            url.format(self.absolute_url())
        )


@implementer(IAuthenticationPlugin)
class DisableUserPlugin(BasePlugin):
    """Plone PAS plugin to block disabled users
    """
    meta_type = 'Disable User Plugin'
    security = ClassSecurityInfo()

    def __init__(self, id_, title=None):
        self._setId(id_)
        self.title = title

    # IAuthenticationPlugin implementation
    @security.private
    def authenticateCredentials(self, credentials):
        if self.is_disabled(credentials):
            msg = _('Your account is disabled.')
            api.portal.show_message(msg, request=self.REQUEST, type='error')
            raise Unauthorized(msg)

    @security.private
    def is_disabled(self, credentials):
        membership = api.portal.get_tool('portal_membership')
        for user_id in self._get_userids(credentials):
            member = membership.getMemberById(user_id)
            if member.getProperty('disabled', False):
                return True

    @security.private
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
