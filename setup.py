import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-multiviewniverse",
    version = "0.0.1",
    author = "Jonas Hagstedt",
    author_email = "hagstedt@gmail.com",
    description = ("multiple models and forms in one view for Django"),
    license = "BSD",
    keywords = "multiple models forms django",
    url = "https://github.com/jonashagstedt/multiviewniverse",
    packages=['multiviewniverse', ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
