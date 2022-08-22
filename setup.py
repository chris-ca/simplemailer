#!/usr/bin/env python

from distutils.core import setup

setup(name='simplemailer',
    version='1.0.3',
    description='Simple wrapper for Python (SMTP) mail using Jinja2 templates',
    author='Chris',
    install_requires=[
        'jinja2'
    ],
    url='https://github.com/chris-ca/simplemailer',
    py_modules=['simplemailer']
)
