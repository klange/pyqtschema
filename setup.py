from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

def find_version(*file_paths):
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="qtjsonschema",
    version=find_version('qtjsonschema', '__init__.py'),
    description="Tool to generate Qt forms from JSON schemas.",
    long_description="""Parses a JSON-Schema and generates a Qt form based on it, which can then be saved to JSON.""",

    url='https://github.com/klange/pyqtschema',

    author='Kevin Lange',
    author_email='klange@dakko.us',

    license='University of Illinois/NCSA Open Source License',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: University of Illinois/NCSA Open Source License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='qt json jsons-chema',

    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires = [],
)


