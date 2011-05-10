"""

Groking::

  >>> from dolmen.menu.testing import grok
  >>> grok(__name__)

A root of publication to compute url::

  >>> from zope.location.location import Location
  >>> from zope.interface import directlyProvides
  >>> from cromlech.io.interfaces import IPublicationRoot

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'

  >>> from cromlech.io.testing import TestRequest
  >>> request = TestRequest()

A basic view ::

  >>> someview = SomeView(context, request)
  >>> someview
  <dolmen.menu.tests.test_multidecorators.SomeView object at ...>

testing menu ::

  >>> mymenu = MyMenu(context, request, someview)
  >>> anothermenu = AnotherMenu(context, request, someview)

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<menu.menuentry `entrywithdetails` for menu `MyMenu`>]

  >>> anothermenu.update()
  >>> anothermenu.viewlets
  [<menu.menuentry `entrywithdetails` for menu `AnotherMenu`>]

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

"""

from dolmen import menu
from zope.interface import Interface

menu.context(Interface)  # everywhere !


class MyMenu(menu.Menu):
    menu.title('My nice menu')


class AnotherMenu(menu.Menu):
    menu.title('My other menu')


class SomeView(object):
    __component_name__ = 'someview'

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

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
