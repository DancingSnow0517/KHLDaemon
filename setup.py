import os

from setuptools import setup, find_packages

from khldaemon.constants import core_constant

# === cheatsheet ===
# linux rm
# rm -rf build/ dist/ khldaemon.egg-info/
# powershell rm
# rm -path "build" -Recurse; rm -path "dist" -Recurse; rm -path "khldaemon.egg-info" -Recurse
# python setup.py sdist bdist_wheel
# python -m twine upload --repository testpypi dist/*
# python -m twine upload dist/*


NAME = core_constant.PACKAGE_NAME
VERSION = core_constant.VERSION_PYPI
DESCRIPTION = 'Plugin system based on khl.py'
URL = 'https://github.com/DancingSnow0517/KHLDaemon'
AUTHOR = 'HuajiMUR233'

CLASSIFIERS = [
    # https://pypi.org/classifiers/
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python'
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIRED = [line for line in f.readlines() if not len(line.strip()) == 0]

print('REQUIRED = {}'.format(REQUIRED))

with open(os.path.join(here, 'README.md'), encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=CLASSIFIERS
)
