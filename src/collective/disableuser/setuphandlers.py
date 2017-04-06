# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonInstallable
from Products.PlonePAS.setuphandlers import activatePluginInterfaces
from zope.interface import implementer

from . import PAS_ID, PAS_TITLE
from .pas.plugin import DisableUserPlugin


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.disableuser:uninstall',
        ]


def installPASPlugin(portal):
    pas = getToolByName(portal, 'acl_users')
    if PAS_ID not in pas:
        plugin = DisableUserPlugin(PAS_ID, PAS_TITLE)
        pas[PAS_ID] = plugin
        activatePluginInterfaces(portal, PAS_ID)

        # We need this plugin to be on top, otherwise the REST API JWT
        # will have preference and the Unauthorized won't fire.
        iface = pas.plugins._getInterfaceFromName("IAuthenticationPlugin")
        no_of_steps = len(pas.plugins.listPlugins(iface)) - 1
        for i in range(no_of_steps):
            pas.plugins.movePluginsUp(iface, [plugin.getId()])


def removePASPlugin(portal):
    pas = getToolByName(portal, 'acl_users')
    if PAS_ID in pas:
        pas._delObject(PAS_ID)


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    installPASPlugin(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    removePASPlugin(context)
