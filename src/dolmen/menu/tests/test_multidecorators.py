"""

Groking::

  >>> grok(__name__)

A root of publication to compute url::

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'
  >>> request = TestRequest()

A basic view ::

  >>> someview = SomeView(context, request)
  >>> someview
  <dolmen.menu.tests.test_multidecorators.SomeView object at ...>

testing menu ::

  >>> mymenu = MyMenu(context, request, someview)
  >>> anothermenu = AnotherMenu(context, request, someview)

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction

  >>> participation = Participation(Principal('zope.anybody'))
  >>> newInteraction(participation)

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<menu.menuentry `entrywithdetails` for menu `mymenu`>]

  >>> anothermenu.update()
  >>> anothermenu.viewlets
  [<menu.menuentry `entrywithdetails` for menu `anothermenu`>]

  >>> print mymenu.render()
  <dl id="mymenu" class="menu">
    <dt>My nice menu</dt>
    <dd>
      <ul>
        <li class="entry">
          <a alt="" href="http://localhost/test/entrywithdetails"
             title="An entry with some details">An entry with some details</a>
        </li>
      </ul>
    </dd>
  </dl>

  >>> print anothermenu.render()
  <dl id="anothermenu" class="menu">
    <dt>My other menu</dt>
    <dd>
      <ul>
        <li class="entry">
          <a alt="" href="http://localhost/test/entrywithdetails"
             title="Alternate title">Alternate title</a>
        </li>
      </ul>
    </dd>
  </dl>

  >>> endInteraction()
"""
from dolmen.menu.testing import grok
from zope.interface import directlyProvides, implements
from cromlech.browser import IView
from cromlech.io.interfaces import IPublicationRoot
from zope.location.location import Location
from grokcore import security
from dolmen import menu
from zope.interface import Interface
from cromlech.io.testing import TestRequest

menu.context(Interface)  # everywhere !


class MyMenu(menu.Menu):
    menu.title('My nice menu')


class AnotherMenu(menu.Menu):
    menu.title('My other menu')


class SomeView(object):
    implements(IView)
    __name__ = 'someview'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        return u"I'm a simple view"


@menu.menuentry(MyMenu, permission='zope.Public')
@menu.menuentry(AnotherMenu, title="Alternate title", permission='zope.Public')
class EntryWithDetails(SomeView):
    menu.title("An entry with some details")

    def render(self):
        return u"A simple entry"


def test_suite():
    import unittest
    import doctest
    from dolmen.menu import tests

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
