import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = (
    'pyramid',
    'colander',
    'deform',
    'voteit.core',
    'Babel',
    'lingua',
    )

setup(name='voteit.combined_simple',
      version='0.1dev',
      description='Combined simple polls for VoteIT',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='VoteIT development team + contributors',
      author_email='info@voteit.se',
      url='http://www.voteit.se',
      keywords='web pylons pyramid voteit',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="voteit.combined_simple",
      entry_points = """\
      [fanstatic.libraries]
      combined_simple = voteit.combined_simple.fanstaticlib:cs_lib
      """,
      message_extractors = { '.': [
              ('**.py',   'lingua_python', None ),
              ('**.pt',   'lingua_xml', None ),
              ]},
      )