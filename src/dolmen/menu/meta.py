# -*- coding: utf-8 -*-

import martian
from grokcore import component, view, viewlet
from grokcore.view.meta.views import default_view_name
from zope import component, interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from dolmen.menu import menu, IMenuEntry


def altered_init(self, context, request, view=None, viewletmanager=None):
    self.view = view
    self.viewletmanager = viewletmanager
    return self.__view_init__(context, request)


class MenuItemGrokker(martian.ClassGrokker):
    martian.component(view.View)
    martian.directive(view.context)
    martian.directive(viewlet.view, default=interface.Interface)
    martian.directive(viewlet.layer, default=IDefaultBrowserLayer)
    martian.directive(viewlet.name, get_default=default_view_name)
    martian.directive(menu, default=None)

    def execute(self, factory, config, context, view, layer, name, menu, **kw):

        if menu is None:
            return True

        factory.__view_init__ = factory.__init__
        factory.__init__ = altered_init

        config.action(
            discriminator = ('viewlet', context, layer,
                             view, menu, name),
            callable = component.provideAdapter,
            args = (factory, (context, layer, view, menu),
                    IMenuEntry, name)
            )
        return True
