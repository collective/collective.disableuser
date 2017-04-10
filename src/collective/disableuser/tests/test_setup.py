# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.disableuser.testing import COLLECTIVE_disableuser_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.disableuser is properly installed."""

    layer = COLLECTIVE_disableuser_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.disableuser is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.disableuser'))

    def test_browserlayer(self):
        """Test that ICollectivedisableuserLayer is registered."""
        from collective.disableuser.interfaces import (
            ICollectivedisableuserLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectivedisableuserLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_disableuser_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.disableuser'])

    def test_product_uninstalled(self):
        """Test if collective.disableuser is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.disableuser'))

    def test_browserlayer_removed(self):
        """Test that ICollectivedisableuserLayer is removed."""
        from collective.disableuser.interfaces import \
            ICollectivedisableuserLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectivedisableuserLayer,
            utils.registered_layers()
        )
