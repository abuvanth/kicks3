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
    name="kicks3",
    version="1.0.2",
    author="Syed Abuthahir",
    author_email="developerabu@gmail.com",
    description="Recon tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abuvanth/kicks3",
    packages=setuptools.find_packages(),
    package_dir={'kicks3': 'kicks3'},
    package_data={'kicks3': ['poc.txt']},
    install_requires=install_requires,
    scripts=['kicks3/kicks3.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
