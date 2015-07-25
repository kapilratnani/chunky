try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A python module to handle reading and writing of text files in chunks.',
    'author': 'Kapil Ratnani',
    'url': 'http://github.com/kapilratnani/chunky',
    'download_url': 'http://github.com/kapilratnani/chunky/tarball/0.5.1',
    'author_email': 'kapil.ratnani@iiitb.net',
    'version': '0.5.1',
    'install_requires': [],
    'keywords':['chunk', 'parts', 'files', 'chunks', 'split'],
    'packages': ['chunky'],
    'name': 'chunky'
}

setup(**config)
