import martian
from dolmen.menu.interfaces import IMenu


def validateMenu(directive, value):
    if not IMenu.implementedBy(value):
        raise ValueError(
            "You can only register a menu item on a IMenu components.")


class menu(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = validateMenu
