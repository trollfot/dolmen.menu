"""
Groking ::

  >>> grok(__name__)

A root of publication to compute url ::

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'
  >>> request = TestRequest()

  >>> someview = GenericView(context, request)
  >>> rootmenu = RootMenu(context, request, someview)

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction

  >>> participation = Participation(Principal('zope.anybody'))
  >>> newInteraction(participation)

  >>> rootmenu.update()
  >>> rootmenu.viewlets
  [<menu.menuentry `somerootentry` for menu `rootmenu`>]

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

  >>> endInteraction()

"""

from dolmen.menu.testing import grok
from zope.location.location import Location
from cromlech.browser import IView
from cromlech.io.interfaces import IPublicationRoot
from dolmen import menu
from zope.interface import Interface, directlyProvides, implements
from grokcore.security import require
from cromlech.io.testing import TestRequest


class GenericView(object):
    implements(IView)
    __name__ = 'generic_view'

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
    from dolmen.menu import tests

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
