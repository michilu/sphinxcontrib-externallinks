# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the externallinks Sphinx extension.

.. add description here ..
''' + open('README.rst').read()

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-externallinks',
    version='0.1',
    url='https://github.com/MiCHiLU/sphinxcontrib-externallinks',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-externallinks',
    license='BSD',
    author='ENDOH takanao',
    description='Sphinx "externallinks" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
