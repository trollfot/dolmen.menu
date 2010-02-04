# -*- coding: utf-8 -*-

import grokcore.view
import grokcore.viewlet

from dolmen.menu.interfaces import IMenu, IMenuEntry, IMenuEntryViewlet
from grokcore.component import baseclass
from megrok.pagetemplate import IPageTemplate, PageTemplate, view
from zope.component import getAdapters, getMultiAdapter
from zope.interface import implements, Interface
from zope.schema.fieldproperty import FieldProperty
from zope.security import checkPermission
from zope.traversing.browser.absoluteurl import absoluteURL


def sort_on_order(a, b):
    return a.order < b.order


class Menu(grokcore.viewlet.ViewletManager):
    """Viewlet Manager working as a menu.
    """
    baseclass()
    implements(IMenu)
    viewlets = []
    entries = FieldProperty(IMenu['entries'])
    menu_class = FieldProperty(IMenu['menu_class'])
    entry_class = FieldProperty(IMenu['entry_class'])
    context_url = FieldProperty(IMenu['context_url'])

    def sort(self, viewlets):
        """Sort the menu entries.
        """
        s_viewlets = []
        for name, viewlet in viewlets:
             viewlet.__viewlet_name__ = name
             s_viewlets.append(viewlet)
        s_viewlets.sort(sort_on_order)
        return s_viewlets

    def _updateViewlets(self):
        """Doesn't fire events, like the original ViewletManager, on purpose.
        """
        for viewlet in self.viewlets:
            if IMenuEntryViewlet.providedBy(viewlet):
                viewlet.update()

    def filter(self, viewlets):
        return [(name, viewlet) for name, viewlet in viewlets
                if checkPermission(viewlet.permission, self.context)]

    def render(self):
        template = getattr(self, 'template', None)
        if template is None:
            template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()

    def update(self):
        self.__updated = True
        self.title = grokcore.view.title.bind().get(self) or self.__name__
        self.context_url = absoluteURL(self.context, self.request)
        # Find all content providers for the region
        viewlets = getAdapters(
            (self.context, self.request, self.__parent__, self),
            IMenuEntry)

        viewlets = self.filter(viewlets)
        self.viewlets = [viewlet for viewlet in self.sort(viewlets)]
        self._updateViewlets()


class Entry(object):
    """Viewlet
    """
    baseclass()
    implements(IMenuEntryViewlet)
    grokcore.viewlet.context(Interface)
    
    __name__ = FieldProperty(IMenuEntryViewlet['__name__'])
    description = FieldProperty(IMenuEntryViewlet['description'])
    manager = FieldProperty(IMenuEntryViewlet['manager'])
    permission = FieldProperty(IMenuEntryViewlet['permission'])

    def __init__(self, context, request, view, manager):
        self.view = self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager

    def default_namespace(self):
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        namespace['view'] = self.view
        namespace['entry'] = self
        namespace['menu'] = self.manager
        return namespace

    def namespace(self):
        return {}

    def update(self):
        pass

    @property
    def selected(self):
        if self.__name__ == self.view.__name__:
            return True
        return False

    def __repr__(self):
        return  "<MenuEntry `%s` for menu `%s`>" % (
            self.__view_name__, self.manager.__name__)

    @property
    def url(self):
        return str("%s/%s" % (self.manager.context_url, self.__name__))

    def render(self):
        template = getattr(self, 'template', None)
        if template is None:
            template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()

 
class MenuTemplate(PageTemplate):
    view(IMenu)
    template = grokcore.view.PageTemplateFile("templates/menu.pt")


class EntryTemplate(PageTemplate):
    view(IMenuEntry)
    template = grokcore.view.PageTemplateFile("templates/entry.pt")
