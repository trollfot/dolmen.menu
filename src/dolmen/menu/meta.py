# -*- coding: utf-8 -*-

import martian
import dolmen.menu
import grokcore.viewlet
from grokcore import component, view, viewlet
from grokcore.view.meta.views import default_view_name
from zope import component, interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


def generate_entry(id, bdict):
    bdict['__view_name__'] = bdict['__name__'] = bdict['name']
    return type(id, (dolmen.menu.Entry,), bdict)


def register_entry(factory, menu, infos, config=None):
    # We get the values from the directives
    values = dolmen.menu.get_entry_values(factory, **infos)
            
    # We generate the entry
    entry_name = factory.__name__.lower()
    context = values.pop('context')
    view = values.pop('view')
    layer = values.pop('layer')
    entry = generate_entry(entry_name, values)
    
    # We enqueue our component in the registry config.
    config.action(
        discriminator=('menuentry', context, layer, view, menu, entry_name),
        callable=component.provideAdapter,
        args=(entry, (context, layer, view, menu),
              dolmen.menu.IMenuEntry, entry_name))


class MenuEntryDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        entries = module_info.getAnnotation('grok.menuentries', [])
        for factory, menu, infos in entries:
            register_entry(factory, menu, infos, config)
        return True


class GlobalMenuEntryGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        entries = dolmen.menu.global_menuentry.bind().get(module)
        for factory, menu, infos in entries:
            register_entry(factory, menu, infos, config)
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
