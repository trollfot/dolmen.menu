# -*- coding: utf-8 -*-

import grokcore.view
from grokcore.component import baseclass
from grokcore import view, viewlet
from zope.location.interfaces import ILocation
from dolmen.menu.interfaces import IMenu, IMenuEntry, IMenuEntryViewlet
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.interface import implements
from zope.component import getAdapters
from zope.schema.fieldproperty import FieldProperty
from zope.viewlet.interfaces import IViewlet


class Menu(viewlet.ViewletManager):
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
        pass
    
    def _get_entries(self, actions):
        if actions:
            selected = getattr(self.view, '__name__', None)
            for action in actions:
                is_selected = action['id'] == selected
                action['selected'] = action['id'] == selected
                action['css'] = (action['selected'] and
                                 self.entry_class + ' selected' or
                                 self.entry_class)
        return actions

    def update(self):
        self.__updated = True
        self.title = view.title.bind().get(self) or self.__name__
        self.context_url = absoluteURL(self.context, self.request)
        # Find all content providers for the region
        viewlets = getAdapters(
            (self.context, self.request, self.__parent__, self),
            IMenuEntry)

        viewlets = self.sort(viewlets)

        # Just use the viewlets from now on
        self.viewlets = []
        for name, viewlet in viewlets:
            if ILocation.providedBy(viewlet):
                viewlet.__name__ = name
            viewlet.update()
            self.viewlets.append(viewlet.render())

        self._updateViewlets()
        self.entries = self._get_entries(self.viewlets)


class ViewletEntry(object):
    """Viewlet
    """
    implements(IMenuEntryViewlet)

    description = FieldProperty(IMenuEntryViewlet['description'])
    manager = FieldProperty(IMenuEntryViewlet['manager'])
    __name__ = FieldProperty(IMenuEntryViewlet['__name__'])
    permission = FieldProperty(IMenuEntryViewlet['permission'])
    url = FieldProperty(IMenuEntryViewlet['url'])

    def __init__(self, context, request, view, manager):
        self.view = self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager

    def update(self):
        self.url = "%s/%s" % (self.manager.context_url, self.__name__)

    def render(self):
        return dict(
            id=self.__name__,
            url=self.url,
            title=self.title,
            description=self.description)
