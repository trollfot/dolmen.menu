===========
dolmen.menu
===========

``dolmen.menu`` aims to provide the most flexible and explicit way to
create and manage menus and their entries with Grok.

You have to know that...
========================

* ``dolmen.menu`` only works on Python 2.6.

* ``dolmen.menu`` does not support sub-menus, out of the box. The
  implementation is left to your discretion.


Components
==========

``dolmen.menu`` provides two components:

* Menu : the menu implementation is based on the zope "content
  provider" notion and is using the ``dolmen.viewlet`` package.
  It is a specific ViewletManager.

* Entry: a menu item is called an entry. It's a viewlet, and as such, a multi
  adapter registered for a Menu component.


Examples
--------

A menu component::

  >>> class MyMenu(dolmen.menu.Menu):
  ...     menu.title('My nice menu')

A menu entry::

  >>> class MyMenuEntry(dolmen.menu.Entry):
  ...     menu.order(1)
  ...     menu.name('a_direct_entry')
  ...     menu.title('My Entry')
  ...     menu.menu(MyMenu)


Registration
============

In order to use base Grok component as menu entries, we get two
registration ways.

class decorator
---------------

A class decorator allows you to decorate any View class, in order to
register it as a menu entry::

  >>> @menu.menuentry(MyMenu)
  ... class TestEntry(ViewClass):
  ...    def render(self):
  ...        return u"A simple entry"


Module level martian directive
------------------------------

A martian directive allows you register classes you can't decorate
(from a foreign package, for instance), explicitly::

  >>> class SomeView(ViewClass):
  ...    def render(self):
  ...        return u"I'm a view and I want to be a menu entry"

  >>> dolmen.menu.global_menuentry(SomeView, MyMenu, order=2)
