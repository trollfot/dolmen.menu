#
import dolmen.menu
import os.path
from zope.app.testing import functional

ftesting_zcml = os.path.join(os.path.dirname(dolmen.menu.__file__), 'ftesting.zcml')
FunctionalLayer = functional.ZCMLLayer(
    ftesting_zcml, __name__, 'FunctionalLayer', allow_teardown=True
    )
