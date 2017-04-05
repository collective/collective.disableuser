# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.disableuser


class CollectivedisableuserLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.disableuser)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.disableuser:default')


COLLECTIVE_disableuser_FIXTURE = CollectivedisableuserLayer()


COLLECTIVE_disableuser_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_disableuser_FIXTURE,),
    name='CollectivedisableuserLayer:IntegrationTesting'
)


COLLECTIVE_disableuser_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_disableuser_FIXTURE,),
    name='CollectivedisableuserLayer:FunctionalTesting'
)


COLLECTIVE_disableuser_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_disableuser_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectivedisableuserLayer:AcceptanceTesting'
)
