from distutils.core import setup
import setuptools

setup(
    name="starlette_context",
    version="0.1.3",
    license="MIT",
    description="Middleware for Starlette that allows you to store and "
    "access the context data of a request. Can be used with "
    "logging so logs automatically use request headers such "
    "as x-request-id or x-correlation-id..",
    packages=setuptools.find_packages(
        exclude=["tests", "*example*"]
    ),
    author="Tomasz Wojcik",
    url="https://github.com/tomwojcik",
    download_url="https://github.com/tomwojcik/starlette-context/"
    "archive/0.1.3.tar.gz",
    keywords=["starlette", "fastapi"],
    install_requires=["starlette",],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
