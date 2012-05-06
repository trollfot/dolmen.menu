# -*- coding: utf-8 -*-

from grokcore.component import order, title, name, description, context
from cromlech.browser.directives import view, request
from dolmen.menu.interfaces import IMenu, IMenuEntry
from dolmen.menu.components import Menu, Entry
from dolmen.menu.declarations import menu, menuentry
from dolmen.menu.declarations import global_menuentry, get_entry_values
