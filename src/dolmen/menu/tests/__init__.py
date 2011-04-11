#-*- coding: utf-8 -*-

import zope.component
from zope.component.interfaces import IComponentLookup
from zope.component.testlayer import ZCMLFileLayer
from zope.interface import Interface, directlyProvides
from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager, SiteManagerAdapter

from cromlech.io.interfaces import IPublicationRoot


def siteSetUp(test):
    """Set up a site, using info of """

    zope.component.hooks.setHooks()

    # Set up site manager adapter
    zope.component.provideAdapter(
        SiteManagerAdapter, (Interface,), IComponentLookup)

    # Set up site
    site = rootFolder()
    site.setSiteManager(LocalSiteManager(site))
    directlyProvides(site, IPublicationRoot)
    zope.component.hooks.setSite(site)

    return site


def siteTearDown(test):
    zope.component.hooks.resetHooks()
    zope.component.hooks.setSite()


class DolmenMenuLayer(ZCMLFileLayer):
    pass

