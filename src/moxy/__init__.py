
__package_name__        = u'moxy'
__description__         = u'EPICS GUI support for a set of motor positions'
__long_description__    = __description__

__version__             = u'0.7.3'
__release__             = __version__
__author__              = u'Pete R. Jemian'
__email__               = u'jemian@anl.gov'
__institution__         = u"Advanced Photon Source, Argonne National Laboratory"
__author_name__         = __author__
__author_email__        = __email__

__copyright__           = u'2009-2015, UChicago Argonne, LLC'
# __license_url__         = u''
__license__             = u'UChicago Argonne, LLC OPEN SOURCE LICENSE (see LICENSE file)'
__url__                 = u'https://github.com/prjemian/moxy/'
__download_url__        = __url__
__keywords__            = ['EPICS', 'motor', 'tool']
__requires__            = ['PyQt4>=4',      # this project developed with PyQt4 >= 4.11.3
                           'PyEpics>=3.2', 
                           'bcdaqwidgets>=2015.0413.0']

__classifiers__ = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Science/Research',
            'License :: Free To Use But Restricted',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development :: Embedded Systems',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
                     ]

# as shown in the About box ...
__credits__ = u'author: ' + __author__
__credits__ += u'\nemail: ' + __email__
__credits__ += u'\ninstitution: ' + __institution__
__credits__ += u'\nURL: ' + __url__
__credits__ += u'\n'
__credits__ += u'\nSpecial thanks to Matt Newville for authoring PyEpics'
