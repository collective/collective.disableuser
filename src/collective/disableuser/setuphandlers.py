# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.PlonePAS.setuphandlers import activatePluginInterfaces
from zope.interface import implementer
from .interfaces import PAS_ID, PAS_TITLE, PROP_DISABLED
from .pas.plugin import DisableUserPlugin


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.disableuser:uninstall',
        ]


def installPASPlugin(portal):
    pas = api.portal.get_tool('acl_users')
    if PAS_ID not in pas:
        plugin = DisableUserPlugin(PAS_ID, PAS_TITLE)
        pas[PAS_ID] = plugin
        activatePluginInterfaces(portal, PAS_ID)

        # We need this plugin to be on top, otherwise the REST API JWT
        # will have preference and the Unauthorized won't fire.
        iface = pas.plugins._getInterfaceFromName('IAuthenticationPlugin')
        no_of_steps = len(pas.plugins.listPlugins(iface)) - 1
        for i in range(no_of_steps):
            pas.plugins.movePluginsUp(iface, [plugin.getId()])


def removePASPlugin(portal):
    pas = api.portal.get_tool('acl_users')
    if PAS_ID in pas:
        pas._delObject(PAS_ID)


def setup_memberdata(context):
    memberdata = api.portal.get_tool('portal_memberdata')
    if not memberdata.hasProperty(PROP_DISABLED):
        memberdata.manage_addProperty(
            id=PROP_DISABLED, value='', type='boolean'
        )


def remove_memberdata(context):
    memberdata = api.portal.get_tool('portal_memberdata')
    if memberdata.hasProperty(PROP_DISABLED):
        memberdata.manage_delProperty(id=PROP_DISABLED)


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    installPASPlugin(context)
    setup_memberdata(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    removePASPlugin(context)
    remove_memberdata(context)
