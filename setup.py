from distutils.core import setup

import setuptools

import os
import re


PKG_NAME = "starlette_context"

HERE = os.path.abspath(os.path.dirname(__file__))

PATTERN = r'^{target}\s*=\s*([\'"])(.+)\1$'

AUTHOR_RE = re.compile(PATTERN.format(target="__author__"), re.M)
VERSION_RE = re.compile(PATTERN.format(target="__version__"), re.M)


def parse_init():
    with open(os.path.join(HERE, PKG_NAME, "__init__.py")) as f:
        file_data = f.read()
    return [
        regex.search(file_data).group(2) for regex in (AUTHOR_RE, VERSION_RE)
    ]


def get_long_description():
    with open("README.md", "r", encoding="utf8") as f:
        return f.read()


AUTHOR, VERSION = parse_init()


setup(
    name=PKG_NAME,
    python_requires=">=3.7",
    version=VERSION,
    license="MIT",
    description="Access context in Starlette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=(PKG_NAME, f"{PKG_NAME}.*")),
    package_data={
        PKG_NAME: ["py.typed"],
    },
    platforms="any",
    author=AUTHOR,
    url="https://github.com/tomwojcik/starlette-context",
    download_url="https://github.com/tomwojcik/starlette-context/"
    f"archive/{VERSION}.tar.gz",
    keywords=["starlette", "fastapi"],
    install_requires="starlette",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
