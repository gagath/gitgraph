from distutils.core import setup


setup(
    name='gitgraph',
    version='0.1',

    url='http://microjoe.eu/',

    author='Romain Porte',
    author_email='microjoe@mailoo.org',

    packages=['gitgraph'],

    scripts=['bin/gitgraph'],

    requires=[
        'pygit2',
    ]
)
