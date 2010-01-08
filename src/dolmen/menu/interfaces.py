from zope import schema
from zope.viewlet.interfaces import IViewletManager, IViewlet


class IMenu(IViewletManager):
    """A menu component.
    """
    entries = schema.List(
        default=[],
        title=u"The menu entries")

    menu_class = schema.TextLine(
        default=u"menu",
        title=u"Menu CSS class")

    entry_class = schema.TextLine(
        default=u"entry",
        title=u"Menu entries CSS class")


class IMenuEntry(IViewlet):
    pass
