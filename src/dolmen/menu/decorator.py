import sys
import types
import zope.component
from zope.interface import Interface
from martian.util import frame_is_module
from martian.error import GrokImportError
from dolmen.menu import Menu, Entry, IMenuEntry
import grokcore.viewlet


class menuentry:
    """Annotates the class for further grokking
    """

    def __init__(self, menu, context=None, layer=None, view=None):
        self._for = context, layer, view, menu
        

    def __call__(self, entry):
        frame = sys._getframe(1)
        if not frame_is_module(frame):
            raise GrokImportError(
                "@dolmen.menu.menuitem can only be used at the module level")

        if not self._for:
            raise GrokImportError(
                "@dolmen.menu.menuitem requires at least one argument.")
    
        if type(entry) is types.FunctionType:
            adapter = zope.component.adapter(*self._for)
            implementer = zope.interface.implementer(*self._for)

            adapter(entry)
            implementer(entry)
            
            adapters = frame.f_locals.get('__grok_adapters__', None)
            if adapters is None:
                frame.f_locals['__grok_adapters__'] = adapters = []
            adapters.append(entry)

        else:
            context, layer, view, menu = self._for
            context = grokcore.viewlet.context.bind().get(entry) or context
            layer = grokcore.viewlet.layer.bind().get(entry) or layer
            view = grokcore.viewlet.view.bind().get(entry) or view

            entries = frame.f_locals.get('__grok_menuentries__', None)
            if entries is None:
                frame.f_locals['__grok_menuentries__'] = entries = []
            entries.append((entry, (context, layer, view, menu)))

        return entry
