# -*- coding: utf-8 -*-

import martian
import dolmen.menu

from grokcore import component, view, viewlet
from grokcore.view.meta.views import default_view_name
from zope import component, interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


def generate_entry(id, name, title, description, permission):
    return type(id, (dolmen.menu.Entry, ),
                {'__name__': name, 'description': description,
                 'title': title, 'permission': permission})

class ViewMenuEntriesGrokker(martian.ClassGrokker):
    martian.component(view.View)

    martian.directive(view.title, default=None)
    martian.directive(view.context)
    martian.directive(view.description, default=u"")
    martian.directive(view.name, get_default=default_view_name)
    martian.directive(view.layer, default=IDefaultBrowserLayer)
    martian.directive(view.require, name='permission', default='zope.View')
    
    martian.directive(viewlet.view, default=interface.Interface)
    martian.directive(dolmen.menu.menu, default=None)
    

    def execute(self, factory, config, context, view, layer,
                name, title, description, permission, menu, **kw):

        if menu is None:
            return True

        # We set the title to name, if none is provided.
        if title is None:
            title = name

        # We generate the netry
        entry_name = factory.__name__.lower()
        entry = generate_entry(
            entry_name, name, title, description, permission)

        # We set the grok prerequisites
        entry.__view_name__ = entry_name
        entry.module_info = factory.module_info

        # We enqueue our component in the registry config.
        config.action(
            discriminator=(
                'menu-entry', context, layer, view, menu, entry_name),
            callable=component.provideAdapter,
            args=(entry, (context, layer, view, menu),
                    dolmen.menu.IMenuEntry, entry_name))

        return True


class ViewletMenuEntriesGrokker(martian.ClassGrokker):
    martian.component(dolmen.menu.Entry)

    martian.directive(viewlet.context)
    martian.directive(viewlet.view, default=interface.Interface)
    martian.directive(viewlet.layer, default=IDefaultBrowserLayer)
    martian.directive(viewlet.name, get_default=default_view_name)
    martian.directive(dolmen.menu.menu, default=None)
    
    def execute(self, factory, config, context, menu, view, layer, name, **kw):

        if not context:
            raise ValueError, "No Context"

        if not menu:
            raise ValueError, "No menu"

        if interface.interfaces.IInterface.providedBy(menu):
            if not menu.isOrExtends(dolmen.menu.IMenu):
                raise ValueError, "Invalid menu type"
        else:
            if not dolmen.menu.IMenu.implementedBy(menu):
                raise ValueError, "Invalid menu type"

        factory.__view_name__ = name
        interface.verify.verifyClass(dolmen.menu.IMenuEntry, factory)

        # We enqueue our component in the registry config.
        config.action(
            discriminator = ('menu-entry', context, layer,
                             view, menu, name),
            callable = component.provideAdapter,
            args = (factory, (context, layer, view, menu),
                    dolmen.menu.IMenuEntry, name)
            )

        return True
