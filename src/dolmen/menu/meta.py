# -*- coding: utf-8 -*-

import martian
from grokcore import component, view, viewlet
from grokcore.view.meta.views import default_view_name
from zope import component, interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import directlyProvides
import dolmen.menu


def generate_entry(id, name, title, description, permission):
    return type(id, (dolmen.menu.ViewletEntry, ),
                {'__name__': name, 'description': description,
                 'title': title, 'permission': permission})


class MenuEntryGrokker(martian.ClassGrokker):
    martian.component(view.View)
    
    martian.directive(view.require)
    martian.directive(view.context)
    martian.directive(view.title, default=None)
    martian.directive(view.description, default=u"")
    martian.directive(view.name, get_default=default_view_name)
    
    martian.directive(viewlet.view, default=interface.Interface)
    martian.directive(viewlet.layer, default=IDefaultBrowserLayer)
    
    martian.directive(dolmen.menu.menu, default=None)
    
    def execute(self, factory, config, context, view, layer,
                name, title, description, require, menu, **kw):

        if menu is None:
            return True

        # We set the title to name, if none is provided.
        if title is None:
            title = name

        # We generate the netry
        entry_name = factory.__name__.lower()
        entry = generate_entry(entry_name, name, title, description, require)

        # We set the grok prerequisites
        entry.__view_name__ = entry_name
        entry.module_info = factory.module_info

        # We enqueue our component in the registry config.
        config.action(
            discriminator = ('viewlet', context, layer,
                             view, menu, entry_name),
            callable = component.provideAdapter,
            args = (entry, (context, layer, view, menu),
                    dolmen.menu.IMenuEntry, entry_name)
            )
        
        return True


