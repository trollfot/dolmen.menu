# -*- coding: utf-8 -*-

import martian
import dolmen.menu
import grokcore.view 
from grokcore import component, view, viewlet
from grokcore.view.meta.views import default_view_name
from zope import component, interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


def generate_entry(id, name, title, description, permission):
    return type(id, (dolmen.menu.Entry, ),
                {'__name__': name, 'description': description,
                 'title': title, 'permission': permission})


class MenuEntryDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        
        entries = module_info.getAnnotation('grok.menuentries', [])
        
        for entry, args in entries:
            name = grokcore.view.name.bind().get(entry) or default_view_name(entry)
            title = grokcore.view.title.bind().get(entry) or name
            description = grokcore.view.description.bind().get(entry)
            permission = grokcore.view.require.bind().get(entry) or 'zope.View'
            
            # We generate the entry
            entry_name = entry.__name__.lower()
            entry = generate_entry(
                entry_name, name, title, description, permission)

            # We set the grok prerequisites
            entry.__view_name__ = entry_name
            entry.module_info = module_info

            # We enqueue our component in the registry config.
            context, layer, view, menu = args
            config.action(
                discriminator=(
                    'menu-entry', context, layer, view, menu, entry_name),
                callable=component.provideAdapter,
                args=(entry, args, dolmen.menu.IMenuEntry, entry_name))
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
