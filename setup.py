# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='Friday13th',
    version='0.01',
    author='Akretion',
    author_email='contact@akretion.com',
    url='https://github.com/akretion/friday13th',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    provides=['friday13th'],
    license='LGPL',
    description='Create files outputs using json files',
    long_description=open('README.md', 'r').read(),
    download_url='https://github.com/akretion/friday13th',
    scripts=[],
    classifiers=[],
    platforms='any',
    test_suite='',
    tests_require=[],
)
