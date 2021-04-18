from distutils.core import setup

import setuptools

from starlette_context import __author__, __version__  # noqa


def get_long_description():
    with open("README.md", "r", encoding="utf8") as f:
        return f.read()


setup(
    name="starlette_context",
    python_requires=">=3.7",
    version=__version__,
    license="MIT",
    description="Access context in Starlette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        include=("starlette_context", "starlette_context.*")
    ),
    package_data={
        "starlette_context": ["py.typed"],
    },
    platforms="any",
    author=__author__,
    url="https://github.com/tomwojcik/starlette-context",
    download_url="https://github.com/tomwojcik/starlette-context/"
    f"archive/{__version__}.tar.gz",
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
