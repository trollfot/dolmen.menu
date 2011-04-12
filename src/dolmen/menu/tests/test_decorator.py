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
  <dolmen.menu.tests.test_decorator.SomeView object at ...>

Using the menu ::

  >>> mymenu = MyMenu(context, request, someview)

Use it ::

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction
  >>> participation = Participation(Principal('zope.anybody'))
  >>> newInteraction(participation)

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<menu.menuentry `entrywithdetails` for menu `mymenu`>,
   <menu.menuentry `testentry` for menu `mymenu`>,
   <menu.menuentry `testentrywithparams` for menu `mymenu`>,
   <FactoryGeneratedEntry `an_entry` for menu `mymenu`>]

  >>> print mymenu.render()
  <dl id="mymenu" class="menu">
    <dt>My nice menu</dt>
    <dd>
      <ul>
        <li class="entry">
          <a alt="This is a nice view."
             href="http://localhost/test/entrywithdetails"
             title="Nice view">Nice view</a>
        </li>
        <li class="entry">
          <a alt="" href="http://localhost/test/testentry"
             title="testentry">testentry</a>
        </li>
        <li class="entry">
          <a alt="" href="http://localhost/test/testentrywithparams?type=1"
             title="testentrywithparams">testentrywithparams</a>
        </li>
        <li class="entry">
          <a href="http://dolmen-project.org"
             title="Dolmen link">Dolmen link</a>
        </li>
      </ul>
    </dd>
  </dl>

  >>> endInteraction()

Using a user with the appropriate rights, we now have both the items::

  >>> participation = Participation(Principal('zope.user'))
  >>> newInteraction(participation)

  >>> mymenu.update()

FIXME : Removed for now

  xxx mymenu.viewlets
  [<menu.menuentry `entrywithdetails` for menu `mymenu`>,
   <menu.menuentry `protectedentry` for menu `mymenu`>,
   <menu.menuentry `testentry` for menu `mymenu`>,
   <menu.menuentry `testentrywithparams` for menu `mymenu`>,
   <FactoryGeneratedEntry `an_entry` for menu `mymenu`>]

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

menu.context(Interface)

Public = 'zope.Public'


class MyMenu(menu.Menu):
    menu.title('My nice menu')


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


class MyPerm(security.Permission):
    security.name('menu.Display')


@menu.menuentry(MyMenu, permission=Public)
class TestEntry(SomeView):
    def render(self):
        return u"A simple entry"


@menu.menuentry(MyMenu, params={'type': 1}, permission=Public)
class TestEntryWithParams(SomeView):
    def render(self):
        return u"A simple entry with a parameter"


@menu.menuentry(MyMenu, available=False, permission=Public)
class TestEntryWithAvailable(SomeView):
    def render(self):
        return u"A simple unavailble entry"

# FIXME temporarly disabled
#~ @menu.menuentry(MyMenu)
#~ class ProtectedEntry(SomeView):
    #~ dolmen.view.security.permission('zope.ManageContent')
#~
    #~ def render(self):
        #~ return "I'm a restricted view"


@menu.menuentry(MyMenu, title='Nice view', description='This is a nice view.',
                permission=Public)
class EntryWithDetails(SomeView):
    def render(self):
        return u"A simple entry"


class MyEntry(object):
    """A very basic entry.
    """
    def __init__(self, menu, id, title, url, desc=u"", perm=Public):
        self.__name__ = id
        self.permission = perm
        self.title = title
        self.description = desc
        self.url = url
        self.menu = menu

    def __repr__(self):
        return "<FactoryGeneratedEntry `%s` for menu `%s`>" % (
            self.__name__, self.menu.__class__.__name__)

    def render(self):
        return """<a href="%s" title="%s">%s</a>""" % (
            self.url, self.title, self.title)


@menu.menuentry(MyMenu)
def manual_entry(context, request, view, menu):
    return MyEntry(menu, 'an_entry', 'Dolmen link',
                   url="http://dolmen-project.org")


def test_suite():
    import unittest
    import doctest
    from dolmen.menu import tests

    suite = unittest.TestSuite()
    mytest = doctest.DocTestSuite(
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    suite.addTest(mytest)
    return suite
