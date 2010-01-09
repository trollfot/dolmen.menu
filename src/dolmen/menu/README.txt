===========
dolmen.menu
===========

  >>> from zope.location.location import Location
  >>> from grokcore import component, viewlet, view, security
  >>> from dolmen.menu import menu, Menu, Entry
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

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction

  >>> participation = Participation(Principal('zope.anybody'))
  >>> newInteraction(participation)

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<BoundEntry `testentry` for menu `mymenu`>]

  >>> mymenu.entries
  [{'url': 'http://127.0.0.1/test/testentry', 'title': 'testentry', 'selected': False, 'id': 'testentry', 'description': 'testentry'}]

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
  [{...'selected': True...}]

  >>> class ProtectedEntry(view.View):
  ...   view.context(Interface)	
  ...	view.require('zope.ManageContent')
  ...   menu(MyMenu)
 
  >>> grok_component('prot', ProtectedEntry)
  True

Anonymous rights doesn't grant us the access to the viewlet::

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<BoundEntry `testentry` for menu `mymenu`>]

  
Using a user with the appropriate rights, we now have both the items::

  >>> endInteraction()
  >>> participation = Participation(Principal('zope.user'))
  >>> newInteraction(participation)

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<BoundEntry `protectedentry` for menu `mymenu`>,
   <BoundEntry `testentry` for menu `mymenu`>]

Security also works with grok Permissions::

  >>> class MyPerm(security.Permission):
  ...   security.name('menu.Display')

  >>> grok_component('perm', MyPerm)
  True

  >>> class OtherProtectedEntry(view.View):
  ...   view.context(Interface)	
  ...	view.require(MyPerm)
  ...   menu(MyMenu)

  >>> grok_component('ope', OtherProtectedEntry)
  True


Manual registration
===================

  >>> class SomeEntry(Entry):
  ...   menu(MyMenu)
  ...
  ...   title = u"Grok website"
  ...   url = "http://grok.zope.org"
  ...   description = u"The homepage of the Grok project"

  >>> grok_component('entry', SomeEntry)
  True

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<BoundEntry `protectedentry` for menu `mymenu`>,
   <BoundEntry `testentry` for menu `mymenu`>,
   <Entry `someentry` for menu `mymenu`>]

  >>> endInteraction()
