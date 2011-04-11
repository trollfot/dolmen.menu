# -*- coding: utf-8 -*-
import urllib
import os
import sys

import dolmen.viewlet
from dolmen.viewlet.components import query_components
from grokcore.component import title, description, context

from grokcore.component import baseclass, adapter, implementer
from grokcore.component.util import sort_components
import grokcore.security
from cromlech.browser import ITemplate
from cromlech.io import IRequest
from dolmen.template import TALTemplate
from dolmen.location import absolute_url
from zope.component import getAdapters, getMultiAdapter
from zope.interface import implements, Interface
from zope.schema.fieldproperty import FieldProperty
from zope.security import checkPermission
from zope.security.checker import CheckerPublic


from dolmen.menu.interfaces import IMenu, IMenuEntry, IMenuEntryViewlet

def isAvailable(viewlet):
    try:
        return viewlet.available
    except AttributeError:
        return True


class Menu(dolmen.viewlet.ViewletManager):
    """Viewlet Manager working as a menu.

    template may be provided as an attribute or will be search as an
    adapter of the menu and the request to IPageTemplate
    """
    baseclass()
    implements(IMenu)
    viewlets = []

    entries = FieldProperty(IMenu['entries'])
    menu_class = FieldProperty(IMenu['menu_class'])
    entry_class = FieldProperty(IMenu['entry_class'])
    context_url = FieldProperty(IMenu['context_url'])
    menu_context = FieldProperty(IMenu['menu_context'])

    @property
    def id(self):
        """id for eg. html id attribute"""
        return self.__name__.replace('.', '-')

    def setMenuContext(self, item):
        self.menu_context = item

    def getMenuContext(self):
        return self.menu_context or self.context

    def _updateViewlets(self):
        """Doesn't fire events, like the original ViewletManager, on purpose.
        """
        for viewlet in self.viewlets:
            if IMenuEntryViewlet.providedBy(viewlet):
                viewlet.update()

    def filter(self, viewlets):
        """Iterator which filters out menu items based on user authorizations
        """
        for name, viewlet in viewlets:
            permission = viewlet.permission
            if permission == 'zope.Public':
                # Translate public permission to CheckerPublic
                permission = CheckerPublic
            if checkPermission(permission, self.context) and \
                    isAvailable(viewlet):
                yield name, viewlet

    def render(self):
        """Template is taken from the template attribute or searching
        for an adapter to ITemplate for menu and request
        """
        template = getattr(self, 'template', None)
        if template is None:
            template = getMultiAdapter((self, self.request), ITemplate)
        return template.render(self)
        
    def get_menu_entries(self):
        # Find all content providers for the region
        import pdb;pdb.set_trace()
        viewlets = getAdapters(
            (self.getMenuContext(), self.request, self.view, self),
            IMenuEntry)
        return self.filter(viewlets)

    def update(self):
        self.__updated = True
        self.title = title.bind(default=self.__name__).get(self) # Alex : why not an interface attribute ?

        # We get the real context
        menu_context = self.getMenuContext()

        # Get the MenuContext and calculate its url
        self.context_url = absolute_url(menu_context, self.request)
        
        viewlets = self.get_menu_entries()
        self.viewlets = sort_components([entry for name, entry in viewlets])
        self._updateViewlets()


class Entry(dolmen.viewlet.Viewlet):
    """The menu entry viewlet

    template may be provided as an attribute or will be search as an
    adapter of the menu and the request to IPageTemplate
    """
    baseclass()
    implements(IMenuEntryViewlet)
    context(Interface)
    params = None

    def __init__(self, context, request, view, manager):
        self.view = self.__parent__ = view
        self.context = context
        self.request = request
        self.manager = manager
        self.__name__ = self.__view_name__

    def __repr__(self):
        return  "<menu.menuentry `%s` for menu `%s`>" % (
            self.__view_name__, self.manager.__name__)

    def default_namespace(self):
        """Objects that will be available in template"""
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
        """Does current page corresponds to this menu entry ?

        Permits to eg. highlith entry

        You may override this if you do not use default strategy of view name
        matching last part of target url
        """
        if self.__name__ == self.view.__name__:
            return True
        return False

    @property
    def url(self):
        """The url the menu entry is pointing at

        Default appends menu entry name to current page url, as it is often the
        case for an action on an object (eg. edit is /path/to/objetc/edit)

        You may override for a different strategy
        """
        url = str("%s/%s" % (self.manager.context_url, self.__name__))
        if self.params:
            url += '?' + urllib.urlencode(self.params, doseq=True)
        return url

    @property
    def title(self):
        return title.bind(default=self.__name__).get(self)

    @property
    def permission(self):
        return grokcore.security.require.bind().get(self)

    @property
    def description(self):
        return description.bind(default=None).get(self)

    def render(self):
        """Template is taken from the template attribute or searching
        for an adapter to ITemplate for entry and request
        """
        template = getattr(self, 'template', None)
        if template is None:
            template = getMultiAdapter((self, self.request), ITemplate)
        return template()

module = sys.modules[__name__]
_prefix = os.path.dirname(module.__file__)

@adapter(IMenu, Interface)
@implementer(ITemplate)
def menu_template(context, request):
    """default template for the menu"""
    return TALTemplate(filename=os.path.join(_prefix, "templates/menu.pt"))

@adapter(IMenuEntry, Interface)
@implementer(ITemplate)
def entry_template(context, request):
    """default template for a menu entry"""
    return TALTemplate(filename=os.path.join(_prefix, "templates/entry.pt"))
