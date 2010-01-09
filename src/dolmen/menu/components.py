# -*- coding: utf-8 -*-

import grokcore.view
import grokcore.viewlet

from grokcore.component import baseclass

from zope.location.interfaces import ILocation
from dolmen.menu.interfaces import IMenu, IMenuEntry, IMenuEntryViewlet
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.interface import implements, Interface
from zope.component import getAdapters
from zope.schema.fieldproperty import FieldProperty
from zope.viewlet.interfaces import IViewlet
from zope.security import checkPermission


class Menu(grokcore.viewlet.ViewletManager):
    """
    """
    baseclass()
    implements(IMenu)

    template = grokcore.view.PageTemplateFile("templates/genericmenu.pt")

    entries = FieldProperty(IMenu['entries'])
    menu_class = FieldProperty(IMenu['menu_class'])
    entry_class = FieldProperty(IMenu['entry_class'])
    context_url = FieldProperty(IMenu['context_url'])

    def filter(self, viewlets):
        return [(name, viewlet) for name, viewlet in viewlets
                if checkPermission(viewlet.permission, self.context)]

    def get_entries(self, viewlets):
        return [viewlet.render() for viewlet in viewlets]
    
    def update(self):
        self.__updated = True
        self.title = grokcore.view.title.bind().get(self) or self.__name__
        self.context_url = absoluteURL(self.context, self.request)
        # Find all content providers for the region
        viewlets = getAdapters(
            (self.context, self.request, self.__parent__, self),
            IMenuEntry)

        viewlets = self.filter(viewlets)
        viewlets = self.sort(viewlets)

        # Just use the viewlets from now on
        self.viewlets = []
        for name, viewlet in viewlets:
            if ILocation.providedBy(viewlet):
                viewlet.__name__ = name
            self.viewlets.append(viewlet)

        self._updateViewlets()
        self.entries = self.get_entries(self.viewlets)


class BoundEntry(object):
    """Viewlet
    """
    implements(IMenuEntryViewlet)

    __name__ = FieldProperty(IMenuEntryViewlet['__name__'])
    description = FieldProperty(IMenuEntryViewlet['description'])
    manager = FieldProperty(IMenuEntryViewlet['manager'])
    permission = FieldProperty(IMenuEntryViewlet['permission'])
    url = FieldProperty(IMenuEntryViewlet['url'])

    def __init__(self, context, request, view, manager):
        self.view = self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager

    def __repr__(self):
        return  "<BoundEntry `%s` for menu `%s`>" % (
            self.__name__, self.manager.__name__)

    def update(self):
        self.url = str("%s/%s" % (self.manager.context_url, self.__name__))

    def render(self):
        return dict(
            id=self.__name__,
            url=self.url,
            title=self.title,
            description=self.description or self.title or None,
            selected = self.__name__ == self.view.__name__)


class Entry(BoundEntry):
    """A manually registered entry.
    """
    baseclass()
    grokcore.viewlet.context(Interface)

    def update(self):
        pass

    def __repr__(self):
        return  "<Entry `%s` for menu `%s`>" % (
            self.__view_name__, self.manager.__name__)
