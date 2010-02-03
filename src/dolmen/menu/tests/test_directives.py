"""
  >>> grok(__name__)
  >>> root = getSite()

  >>> context = root['test'] = Location()
  >>> request = TestRequest()

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
  [<MenuEntry `anotherview` for menu `navigationmenu`>]

  >>> print navigation.render()
  <dl id="navigationmenu" class="menu">
    <dt>My nice menu</dt>
      <dd>
        <ul class="menu">
          <li class="entry">
            <a href="http://127.0.0.1/test/anotherview"
               title="anotherview">anotherview</a>
         </li>
      </ul>
    </dd>
  </dl>
"""
from grokcore.component.testing import grok
from zope.location.location import Location
from grokcore import view, security
from dolmen.menu import global_menuentry, Menu, Entry, IMenuEntry, IMenu
from zope.interface import Interface
from zope.site.hooks import getSite
from zope.publisher.browser import TestRequest 

view.context(Interface)

class NavigationMenu(Menu):
    view.title('My nice menu')


class GlobalView(view.View):
    def render(self):
        return u"I'm a view"


class AnotherView(view.View):
    def render(self):
        return u"I'm a view and I want to be a menu entry"


global_menuentry(AnotherView, NavigationMenu)


def test_suite():
    import unittest
    from dolmen.menu import tests
    from zope.testing import doctest
    
    suite = unittest.TestSuite()
    decorators = doctest.DocTestSuite(
        setUp=tests.siteSetUp, tearDown=tests.siteTearDown,
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    decorators.layer = tests.DolmenMenuLayer(tests.test_directives)
    suite.addTest(decorators)
    return suite
