#!/usr/bin/env python

import os

from setuptools import setup, find_packages


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r", encoding="UTF-8").read()


setup(
    name="MacScan",
    version="0.0.0",
    description="A simple Python library and CLI tool to scan document on macOS using ImageCaptureCore",
    license="BSD-3-Clause",
    long_description=long_description,
    keywords="macOS scan scanner ImageCaptureCore PyObjC",
    author="Wanadev <contact@wanadev.fr>",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyObjC",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
        ]
    },
    entry_points={
        "console_scripts": [
            "macscan = macscan.__main__:main",
        ]
    },
)
