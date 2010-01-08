# -*- coding: utf-8 -*-

import martian
from grokcore import component, view, viewlet
from grokcore.view.meta.views import default_view_name
from zope import component, interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
import dolmen.menu


def generate_entry(name):
    return type(name, (viewlet.Viewlet, ), {})


from sys import modules
from grokcore.component import zcml
from zope.interface import directlyProvides


class MenuEntryGrokker(martian.ClassGrokker):
    martian.component(view.View)
    martian.directive(view.context)
    martian.directive(viewlet.view, default=interface.Interface)
    martian.directive(viewlet.layer, default=IDefaultBrowserLayer)
    martian.directive(viewlet.name, get_default=default_view_name)
    martian.directive(dolmen.menu.menu, default=None)

    def execute(self, factory, config, context, view, layer, name, menu, **kw):

        entry_name = factory.__name__.lower() + '_menu_entry'
        entry = generate_entry(entry_name)
        entry.__view_name__ = entry_name

        config.action(
            discriminator = ('viewlet', context, layer,
                             view, menu, entry_name),
            callable = component.provideAdapter,
            args = (entry, (context, layer, view, menu),
                    dolmen.menu.IMenuEntry, entry_name)
            )
        
        return True


