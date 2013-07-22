"""
Groking ::

  >>> from dolmen.menu.testing import grok
  >>> grok(__name__)

A root of publication to compute url::

  >>> from zope.location.location import Location
  >>> from cromlech.browser import IPublicationRoot
  >>> from zope.interface import directlyProvides

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'

  >>> from cromlech.browser.testing import TestRequest
  >>> request = TestRequest()

Test the menu::

  >>> current_view = GlobalView(context, request)
  >>> current_view
  <dolmen.menu.tests.test_directives.GlobalView object at ...>

  >>> navigation = NavigationMenu(context, request, current_view)

  >>> navigation.update()
  >>> navigation.viewlets
  [<menu.menuentry `a_direct_entry` for menu `NavigationMenu`>, <menu.menuentry `anotherview` for menu `NavigationMenu`>, <menu.menuentry `a_second_entry` for menu `NavigationMenu`>]

  >>> print navigation.render()
  <dl id="navigationmenu" class="menu">
    <dt>My nice menu</dt>
      <dd>
        <ul>
          <li class="entry">
            <a href="http://localhost/test/a_direct_entry?type=1"
               title="My Entry">My Entry</a>
          </li>
          <li class="entry">
            <a href="http://localhost/test/anotherview"
               title="anotherview" alt="">anotherview</a>
         </li>
         <li class="entry">
            <a href="http://localhost/test/a_second_entry?type=1"
               title="My other Entry">My other Entry</a>
         </li>
      </ul>
    </dd>
  </dl>

"""
from cromlech.browser import IView
from dolmen import menu
from dolmen.menu.interfaces import IMenu
from zope.interface import Interface, implementer


menu.context(Interface)


class ISomeMenu(IMenu):
    pass


@implementer(ISomeMenu)
class NavigationMenu(menu.Menu):
    menu.title('My nice menu')


@implementer(IView)
class GlobalView(object):
    __component_name__ = 'globalview'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        return u"I'm a view"


class AnotherView(GlobalView):
    def render(self):
        return u"I'm a view and I want to be a menu entry"


class MyMenuEntry(menu.Entry):
    """all set up by directives
    """
    menu.order(1)
    menu.name('a_direct_entry')
    menu.title('My Entry')
    menu.menu(NavigationMenu)
    params = {'type': 1}


class AnotherEntry(menu.Entry):
    """all set up by directives
    """
    menu.order(2)
    menu.name('a_second_entry')
    menu.title('My other Entry')
    menu.menu(ISomeMenu)
    params = {'type': 1}


menu.global_menuentry(AnotherView, NavigationMenu, order=2,
                      permission='zope.Public')


def test_suite():
    import unittest
    import doctest

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
