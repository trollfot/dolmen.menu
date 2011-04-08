# -*- coding: utf-8 -*-

import martian
from dolmen import menu

from dolmen.view.meta import default_view_name
from zope import component, interface
from cromlech.io import IRequest


def generate_entry(bdict):
    """instanciat an Entry from parameters"""
    id = bdict['__view_name__'] = bdict['__name__'] = str(bdict['name'])
    return id, type(id, (menu.Entry,), bdict)


def register_entry(factory, menu, infos, config=None):
    """Registration for class methods"""
    # We get the values from the directives
    values = menu.get_entry_values(factory, **infos)

    # We pop the values issued from directives.
    context = values.pop('context')
    view = values.pop('view')
    request = values.pop('request')
    order = values.pop('order')

    # We generate the entry.
    entry_name, entry = generate_entry(values)

    # If order was not from a directive, we set it back, for later sorting.
    if not isinstance(order, tuple):
        menu.order.set(entry, (order, 1))

    # We enqueue our component in the registry config.
    config.action(
        discriminator=('menuentry', context, request, view, menu, entry_name),
        callable=component.provideAdapter,
        args=(entry, (context, request, view, menu),
              menu.IMenuEntry, entry_name))


class PreAdapterDecoratorGrokker(martian.GlobalGrokker):
    """Call registrators that were annotateid in the module
    by the directives

    see :py:func:`declarations.function_menu_entry()`
    """
    martian.priority(1000)
    
    def grok(self, name, module, module_info, config, **kw):
        callbacks = module_info.getAnnotation('menufunctions', [])
        for register in callbacks:
            register()
        return True


class MenuEntryGrokker(martian.GlobalGrokker):
    """Call registrators that were annotateid in the module
    by the directives

    see :py:func:`declarations.global_menuentry()`
    """

    def grok(self, name, module, module_info, config, **kw):
        callbacks = module_info.getAnnotation('menuclasses', [])
        for register in callbacks:
            register(register_entry, config)
        return True


class ViewletMenuEntriesGrokker(martian.ClassGrokker):
    """Grokker for menu entries"""
    martian.component(menu.Entry)
    martian.directive(menu.context)
    martian.directive(menu.view, default=interface.Interface)
    martian.directive(menu.request, default=IRequest)
    martian.directive(menu.name, get_default=default_view_name)
    martian.directive(menu.menu, default=None)

    def execute(self, factory, config, context, menu, view, request,
                name, **kw):
        """Context and menu are mandatory. Menu directive may refer either
        to a class or interface.

        MenuEntry is a viewlet managed by its Menu, so a named adapter of
        (context, request, view, viewletmanager) to
        :py:class:`menu.IMenuEntry`
        """

        if not context:
            raise ValueError("No Context")

        if not menu:
            raise ValueError("No menu")

        if interface.interfaces.IInterface.providedBy(menu):
            if not menu.isOrExtends(menu.IMenu):
                raise ValueError("Invalid menu type")
        else:
            if not menu.IMenu.implementedBy(menu):
                raise ValueError("Invalid menu type")

        factory.__name__ = factory.__view_name__ = name
        interface.verify.verifyClass(menu.IMenuEntry, factory)

        # We enqueue our component in the registry config.
        config.action(
            discriminator=('menu-entry', context, request,
                           view, menu, name),
            callable=component.provideAdapter,
            args=(factory, (context, request, view, menu),
                  menu.IMenuEntry, name))

        return True
