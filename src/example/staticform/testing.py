# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import example.staticform


class ExampleStaticformLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=example.staticform)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'example.staticform:default')


EXAMPLE_STATICFORM_FIXTURE = ExampleStaticformLayer()


EXAMPLE_STATICFORM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_STATICFORM_FIXTURE,),
    name='ExampleStaticformLayer:IntegrationTesting',
)


EXAMPLE_STATICFORM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_STATICFORM_FIXTURE,),
    name='ExampleStaticformLayer:FunctionalTesting',
)


EXAMPLE_STATICFORM_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EXAMPLE_STATICFORM_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ExampleStaticformLayer:AcceptanceTesting',
)
