#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools,os

with open("README.md", "r") as fh:
    long_description = fh.read()
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setuptools.setup(
    name="kick-s3",
    version="2.0.0",
    author="Syed Abuthahir",
    author_email="developerabu@gmail.com",
    description="Recon tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abuvanth/kicks3",
    packages=['kicks3'],
    package_dir={'kicks3': 'kicks3'},
    install_requires=install_requires,
    dependency_links=['https://github.com/abuvanth/Sublist3r/tarball/master'],
    scripts=['kicks3/kicks3.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
