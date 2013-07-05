#!/usr/bin/env python

from setuptools import setup

setup(
    name='django_w3c_validator',
    version='1.0',
    author='Rachel Bell',
    author_email='rachel.twu@gmail.com',
    description='Crawls for internal urls at a domain, then validates them using W3C validator.',
    install_requires=['Django>=1.3'],
    url='https://github.com/racheltwu/django_w3c_validator',
    packages=['django_w3c_validator'],
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)