"""
Groking ::

  >>> from dolmen.menu.testing import grok
  >>> grok(__name__)

A root of publication to compute url::

  >>> from zope.location.location import Location
  >>> from cromlech.io.interfaces import IPublicationRoot
  >>> from zope.interface import directlyProvides

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'

  >>> from cromlech.io.testing import TestRequest
  >>> request = TestRequest()

Test the menu, not availbale, at first::

  >>> current_view = GlobalView(context, request)
  >>> current_view
  <dolmen.menu.tests.test_available.GlobalView object at ...>

  >>> navigation = NavigationMenu(context, request, current_view)

  >>> navigation.update()
  >>> navigation.viewlets
  []

Make it available::

  >>> setattr(context, 'gimme_menu', True)
  >>> navigation = NavigationMenu(context, request, current_view)
  >>> navigation.update()
  >>> navigation.viewlets
  [<menu.menuentry `an_entry` for menu `NavigationMenu`>]

"""
from cromlech.browser import IView
from dolmen import menu
from zope.interface import Interface, implements


menu.context(Interface)


class NavigationMenu(menu.Menu):
    menu.title('My nice menu')


class GlobalView(object):
    implements(IView)
    __component_name__ = 'globalview'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        return u"I'm a view"


class MayOrMayNotMenu(menu.Entry):
    """all set up by directives
    """
    menu.order(1)
    menu.name('an_entry')
    menu.title('My Entry')
    menu.menu(NavigationMenu)

    @property
    def available(self):
        return getattr(self.context, 'gimme_menu', False)


def test_suite():
    import unittest
    import doctest

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
