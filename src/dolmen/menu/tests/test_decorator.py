"""
  >>> root = getSite()

  >>> context = root['test'] = Location()
  >>> request = TestRequest()

  >>> someview = SomeView(context, request)
  >>> someview
  <dolmen.menu.tests.test_decorator.SomeView object at ...>

  >>> mymenu = MyMenu(context, request, someview)

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction

  >>> participation = Participation(Principal('zope.anybody'))
  >>> newInteraction(participation)

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<MenuEntry `testentry` for menu `mymenu`>]

  >>> print mymenu.render()
  <dl id="mymenu" class="menu">
    <dt>My nice menu</dt>
    <dd>
      <ul class="menu">
        <li class="entry">
    	  <a href="http://127.0.0.1/test/testentry"
    	     title="testentry">testentry</a>
    	</li>
      </ul>
    </dd>
  </dl>

Using a user with the appropriate rights, we now have both the items::

  >>> endInteraction()
  >>> participation = Participation(Principal('zope.user'))
  >>> newInteraction(participation)

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<MenuEntry `protectedentry` for menu `mymenu`>,
   <MenuEntry `testentry` for menu `mymenu`>]

"""

from zope.location.location import Location
from grokcore import view, security
from dolmen.menu import menu, Menu, Entry, IMenuEntry
from zope.interface import Interface
from zope.site.hooks import getSite
from zope.publisher.browser import TestRequest
from dolmen.menu.decorator import menuentry
 

view.context(Interface)


class MyMenu(Menu):
    view.title('My nice menu')
 

class SomeView(view.View):
    def render(self):
        return u"I'm a simple view"


class MyPerm(security.Permission):
    security.name('menu.Display')


@menuentry(MyMenu)
class TestEntry(view.View):
    def render(self):
        return u"A simple entry"


@menuentry(MyMenu)
class ProtectedEntry(view.View):
    view.require('zope.ManageContent')

    def render(self):
        return "I'm a restricted view"


def test_suite():
    import unittest
    from dolmen.menu import tests
    from zope.testing import doctest
    
    suite = unittest.TestSuite()
    decorators = doctest.DocTestSuite(
        setUp=tests.siteSetUp, tearDown=tests.siteTearDown,
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    decorators.layer = tests.DolmenMenuLayer(tests.test_decorator)
    suite.addTest(decorators)
    return suite
