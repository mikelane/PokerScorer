try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'description': 'A python3 tool that scores poker hands',
        'author': 'Michael Lane',
        'url': 'http://github.com/mikelane/',
        'download_url': 'http://github.com/mikelane/PokerScorer',
        'author_email': 'mikelane@gmail.com',
        'version': '0.1',
        'install_requires': ['nose'],
        'packages': ['PokerScorer'],
        'scripts': [],
        'name': 'PokerScorer'
}

setup(**config)

