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
  [<MenuEntry `a_direct_entry` for menu `navigationmenu`>,
   <MenuEntry `anotherview` for menu `navigationmenu`>]

  >>> print navigation.render()
  <dl id="navigationmenu" class="menu">
    <dt>My nice menu</dt>
      <dd>
        <ul>
          <li class="entry">
    	    <a href="http://127.0.0.1/test/a_direct_entry?type=1"
               title="My Entry">My Entry</a>
          </li>
          <li class="entry">
            <a alt="" href="http://127.0.0.1/test/anotherview"
               title="anotherview">anotherview</a>
         </li>
      </ul>
    </dd>
  </dl>

  >>> endInteraction()
"""
from grokcore.component.testing import grok
from zope.location.location import Location
from dolmen import view, viewlet
from dolmen import menu
from zope.interface import Interface
from zope.site.hooks import getSite
from cromlech.io.testing import TestRequest

menu.context(Interface)

class NavigationMenu(menu.Menu):
    menu.title('My nice menu')


class GlobalView(view.View):
    def render(self):
        return u"I'm a view"


class AnotherView(view.View):
    def render(self):
        return u"I'm a view and I want to be a menu entry"


class MyMenuEntry(menu.Entry):
    menu.order(1)
    menu.name('a_direct_entry')
    menu.title('My Entry')
    menu.menu(NavigationMenu)
    params = {'type': 1}


menu.global_menuentry(AnotherView, NavigationMenu, order=2)


def test_suite():
    import unittest, doctest
    from dolmen.menu import tests

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        setUp=tests.siteSetUp, tearDown=tests.siteTearDown,
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    mytest.layer = tests.DolmenMenuLayer(tests)
    suite.addTest(mytest)
    return suite
