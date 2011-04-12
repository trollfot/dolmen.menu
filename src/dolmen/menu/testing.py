# -*- coding: utf-8 -*-

from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml


def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok('grokcore.component.meta', config)
    zcml.do_grok('dolmen.viewlet.meta', config)
    zcml.do_grok('dolmen.location.resolvers', config)
    zcml.do_grok('dolmen.menu.meta', config)
    zcml.do_grok('dolmen.menu.components', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()
