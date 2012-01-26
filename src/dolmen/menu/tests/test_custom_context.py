"""
Groking ::

  >>> from dolmen.menu.testing import grok
  >>> grok(__name__)

A root of publication to compute url ::

  >>> from zope.location.location import Location
  >>> from zope.interface import Interface, directlyProvides

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'

  >>> from cromlech.browser.testing import TestHTTPRequest
  >>> request = TestHTTPRequest()

  >>> someview = GenericView(context, request)
  >>> rootmenu = RootMenu(context, request, someview)

  >>> rootmenu.update()
  >>> rootmenu.viewlets
  [<menu.menuentry `somerootentry` for menu `RootMenu`>]

  >>> print rootmenu.render()
  <dl id="rootmenu" class="menu">
    <dt>My Root Menu</dt>
    <dd>
      <ul>
        <li class="entry">
          <a alt="" href="http://localhost/somerootentry"
                    title="somerootentry">somerootentry</a>
        </li>
      </ul>
    </dd>
  </dl>

"""
from dolmen import menu
from zope.interface import Interface
from grokcore.security import require
from cromlech.io.interfaces import IPublicationRoot


class GenericView(object):
    __component_name__ = 'generic_view'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        return u"I'm a simple view"


class RootMenu(menu.Menu):
    menu.title('My Root Menu')
    menu.context(Interface)

    def update(self):
        self.setMenuContext(self.context.__parent__)
        menu.Menu.update(self)


@menu.menuentry(RootMenu)
class SomeRootEntry(GenericView):
    menu.context(IPublicationRoot)
    require('zope.Public')

    def render(self):
        return u"A Root entry"


def test_suite():
    import unittest
    import doctest

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
