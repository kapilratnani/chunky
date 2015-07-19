try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A python library to handle reading and writing of text files in chunks.',
    'author': 'Kapil Ratnani',
    'url': 'http://github.com/kapilratnani/chunky',
    'download_url': 'http://github.com/kapilratnani/chunky',
    'author_email': 'kapil.ratnani@iiitb.net',
    'version': '0.1',
    'install_requires': [],
    'packages': ['chunky'],
    'name': 'chunky'
}

setup(**config)