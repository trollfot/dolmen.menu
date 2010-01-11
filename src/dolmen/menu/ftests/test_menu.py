"""
  >>> from zope.app.testing.functional import getRootFolder
  >>> root = getRootFolder()
  >>> root['doc'] = doc = Document() 
  >>> root['doc']
  <dolmen.menu.ftests.test_menu.Document object at ...>

  >>> root['event'] = doc = Event() 
  >>> root['event']
  <dolmen.menu.ftests.test_menu.Event object at ...>

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/doc/index')
  >>> print browser.contents
  <dl id="sitemenu" class="menu">
    <dt>sitemenu</dt>
    <dd>
      <ul class="menu">
        <li class="entry">
      <a href="http://www.dolmen.de" title="GlobalEntry">GlobalEntry</a>
        </li>
      </ul>
    </dd>
  </dl>

  >>> browser.open('http://localhost/event/index')
  >>> print browser.contents
  <dl id="sitemenu" class="menu">
    <dt>sitemenu</dt>
    <dd>
      <ul class="menu">
        <li class="entry">
      <a href="http://www.dolmen.de" title="GlobalEntry">GlobalEntry</a>
        </li>
        <li class="entry">
      <a href="http://localhost/event/ical" title="ical">ical</a>
        </li>
      </ul>
    </dd>
  </dl>

"""  

import grokcore.view as view 
import grokcore.component as grok

from grokcore.view import templatedir
from dolmen.menu import Menu, Entry, menu
from zope.interface import Interface

templatedir('templates')


class Document(grok.Context):
    pass


class Event(grok.Context):
    pass


class Index(view.View):
    grok.context(Interface)


class SiteMenu(Menu):
    grok.context(Interface)


class GlobalEntry(Entry):
    grok.context(Interface)
    menu(SiteMenu)
    title = "GlobalEntry"
    url="http://www.dolmen.de"

class ICal(view.View):
    grok.context(Event)
    menu(SiteMenu)

    def render(self):
        return "ICAL"

def test_suite():
    from zope.testing import doctest
    from dolmen.menu.ftests import FunctionalLayer
    suite = doctest.DocTestSuite(
         optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
    suite.layer = FunctionalLayer
    return suite
