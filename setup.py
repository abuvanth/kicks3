import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kicks3",
    version="0.0.1",
    author="Syed Abuthahir",
    author_email="developera@gmail.com",
    description="Recon tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abuvanth/kicks3",
    packages=setuptools.find_packages(),
    scripts=['script/kicks3.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
