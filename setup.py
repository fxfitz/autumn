import imp

from setuptools import find_packages, setup

VERSION = imp.load_source('autumn_init', './autumn/version.py').__version__


setup(
    name='autumn',
    version=VERSION,
    description="Internet File Harvester",
    long_description=(
        "Autumn is an file harvester that scours the internet for filetypes "
        "and downloads them!"
    ),
    author="Fran Fitzpatrick",
    author_email='francis.x.fitzpatrick@gmail.com',
    license='GPL v2',
    packages=find_packages(),
    install_requires=[
        "google>=1.9",
        "requests",
        "filemagic"
    ]
)
