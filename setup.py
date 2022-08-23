#!/usr/bin/env python

from distutils.core import setup

setup(name='simplemailer',
    version='1.0.4',
    description='Simple wrapper for Python (SMTP) mail using Jinja2 templates',
    author='Chris',
    install_requires=[
        'jinja2'
    ],
    extras_require={
        "test": [
            "pytest",
            "smtpdfix",
        ],
    },
    entry_points={
        'console_scripts': [
            'simplemailer = simplemailer'
        ]
    },
    url='https://github.com/chris-ca/simplemailer',
    py_modules=['simplemailer']
)
