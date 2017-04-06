# -*- coding: utf-8 -*-
from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService.PluggableAuthService import \
    registerMultiPlugin
from zope.i18nmessageid import MessageFactory

from .pas import plugin

PAS_ID = 'disableuser'
PAS_TITLE = 'Disable User Plugin'


_ = MessageFactory('collective.disableuser')


def initialize(context):
    registerMultiPlugin(plugin.DisableUserPlugin.meta_type)
    context.registerClass(
        plugin.DisableUserPlugin,
        permission=add_user_folders,
        constructors=(plugin.manage_addDisableUserPlugin,
                      plugin.addDisableUserPlugin),
        visibility=None,
    )
