#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kicks3",
    version="0.0.9",
    author="Syed Abuthahir",
    author_email="developerabu@gmail.com",
    description="Recon tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abuvanth/kicks3",
    packages=setuptools.find_packages(),
    scripts=['kicks3/kicks3.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
