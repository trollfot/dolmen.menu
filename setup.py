# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.menu'
version = '0.1'
readme = open(join('src', 'dolmen', 'menu', "README.txt")).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'setuptools',
    'grokcore.component',
    'grokcore.viewlet',
    'grokcore.view',
    'martian',
    'zope.interface',
    'zope.security'
    ]


tests_require = [
    'zope.configuration',
    'zope.app.zcmlfiles'
    ]

setup(name = name,
      version = version,
      description = 'Dolmen menu',
      long_description = readme + '\n\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = '',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
      )
