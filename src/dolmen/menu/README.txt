===========
dolmen.menu
===========

  >>> from zope.location.location import Location
  >>> from grokcore import view
  >>> from grokcore import component
  >>> from dolmen.menu import menu, Menu
  >>> from zope.interface import Interface
  >>> from zope.publisher.browser import TestRequest
  >>> from zope.component import getMultiAdapter

  >>> root = getRootFolder()

  >>> context = root['test'] = Location()
  >>> request = TestRequest()

  >>> class MyMenu(Menu):
  ...   view.context(Interface)

  >>> grok_component('mymenu', MyMenu)
  True

  >>> class SomeView(view.View):
  ...   view.context(Interface)

  >>> grok_component('view', SomeView)
  True

  >>> someview = SomeView(context, request)
  >>> someview
  <dolmen.menu.tests.SomeView object at ...>

  >>> mymenu = MyMenu(context, request, someview)

  >>> class TestEntry(view.View):
  ...   view.context(Interface)
  ...   menu(MyMenu)
 
  >>> grok_component('test', TestEntry)
  True

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<dolmen.menu.tests.TestEntry object at ...>]

  >>> mymenu.entries
  [{'url': u'http://127.0.0.1/test/testentry',
    'selected': False, 'css': u'entry', 'title': u'testentry'}]

  >>> print mymenu.render()
  <dl id="mymenu" class="menu">
    <dt>mymenu</dt>
    <dd>
      <ul class="menu">
        <li class="entry">
    	  <a href="http://127.0.0.1/test/testentry"
    	     title="testentry">testentry</a>
    	</li>
      </ul>
    </dd>
  </dl>

  >>> selected = TestEntry(context, request)
  >>> mymenu = MyMenu(context, request, selected)
  >>> mymenu.update()
  >>> mymenu.entries
  [{'url': u'http://127.0.0.1/test/testentry',
    'selected': True, 'css': u'entry selected', 'title': u'testentry'}]


  >>> from grokcore.view import title
  >>> title.set(TestEntry, u'A Simple Title')
  >>> mymenu.update()
  >>> mymenu.entries
  [{'url': u'http://127.0.0.1/test/testentry',
    'selected': True, 'css': u'entry selected', 'title': u'A Simple Title'}]
