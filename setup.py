import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = [
    'django',
]

setup(
    name='django-advancedsearchfilter',
    version='0.2.1',
    description='Advanced Search Filter for Django Contrib Admin',
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Joel Kleier',
    author_email='joel@kleier.us',
    url='http://github.com/wildcardcorp/django-advancedsearchfilter',
    keywords='web django search',
    packages=find_packages(),
    license="LICENSE.txt",
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="",
    entry_points="",
)
