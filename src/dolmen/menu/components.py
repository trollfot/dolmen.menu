# -*- coding: utf-8 -*-

import grokcore.view
import grokcore.viewlet

from dolmen.menu.interfaces import IMenu, IMenuEntry, IMenuEntryViewlet
from grokcore.component import baseclass
from zope.component import getAdapters, getMultiAdapter, queryAdapter
from zope.interface import implements, Interface
from zope.schema.fieldproperty import FieldProperty
from zope.security import checkPermission
from zope.traversing.browser.absoluteurl import absoluteURL

from megrok.pagetemplate import IPageTemplate, PageTemplate, view


class Menu(grokcore.viewlet.ViewletManager):
    """
    """
    baseclass()
    implements(IMenu)

    viewlets = []
    entries = FieldProperty(IMenu['entries'])
    menu_class = FieldProperty(IMenu['menu_class'])
    entry_class = FieldProperty(IMenu['entry_class'])
    context_url = FieldProperty(IMenu['context_url'])

    def _updateViewlets(self):
        """Doesn't fire events, like the original ViewletManager, on purpose.
        """
        for viewlet in self.viewlets:
            if IMenuEntryViewlet.providedBy(viewlet):
                viewlet.update()

    def filter(self, viewlets):
        return [(name, viewlet) for name, viewlet in viewlets
                if checkPermission(viewlet.permission, self.context)]

    @property
    def entries(self):
        for viewlet in self.viewlets:
            yield dict(
                id=viewlet.__name__,
                url=viewlet.url,
                title=viewlet.title,
                description=viewlet.description or viewlet.title or None,
                selected = viewlet.__name__ == self.view.__name__)

    def update(self):
        self.__updated = True
        self.title = grokcore.view.title.bind().get(self) or self.__name__
        self.context_url = absoluteURL(self.context, self.request)
        # Find all content providers for the region
        viewlets = getAdapters(
            (self.context, self.request, self.__parent__, self),
            IMenuEntry)

        viewlets = self.filter(viewlets)
        self.viewlets = [viewlet for name, viewlet in self.sort(viewlets)]
        self._updateViewlets()

    def render(self):
        template = self.template
        if template is None:
            template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


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

    @property
    def selected(self):
        if self.__name__ == self.view.__name__:
            return True
        return False    

    def update(self):
        self.url = str("%s/%s" % (self.manager.context_url, self.__name__))



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
        

class MenuTemplate(PageTemplate):
    view(IMenu)
    template = grokcore.view.PageTemplateFile("templates/genericmenu.pt")

