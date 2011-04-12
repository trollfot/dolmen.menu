"""
Groking ::

  >>> grok(__name__)

A root of publication to compute url::

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'
  >>> request = TestRequest()

Test the menu::

  >>> current_view = GlobalView(context, request)
  >>> current_view
  <dolmen.menu.tests.test_directives.GlobalView object at ...>

  >>> navigation = NavigationMenu(context, request, current_view)

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction

  >>> participation = Participation(Principal('zope.anybody'))
  >>> newInteraction(participation)

  >>> navigation.update()
  >>> navigation.viewlets
  [<menu.menuentry `a_direct_entry` for menu `navigationmenu`>,
   <menu.menuentry `anotherview` for menu `navigationmenu`>]

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
            <a alt="" href="http://localhost/test/anotherview"
               title="anotherview">anotherview</a>
         </li>
      </ul>
    </dd>
  </dl>

  >>> endInteraction()
"""
from dolmen.menu.testing import grok
from zope.location.location import Location
from cromlech.io.interfaces import IPublicationRoot
from cromlech.browser import IView
from dolmen import viewlet
from dolmen import menu
from zope.interface import Interface, directlyProvides, implements
from cromlech.io.testing import TestRequest

menu.context(Interface)


class NavigationMenu(menu.Menu):
    menu.title('My nice menu')


class GlobalView(object):
    implements(IView)
    __name__ = 'globalview'

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

menu.global_menuentry(AnotherView, NavigationMenu, order=2,
                      permission='zope.Public')


def test_suite():
    import unittest
    import doctest
    from dolmen.menu import tests

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
