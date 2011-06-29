from setuptools import setup, find_packages


setup(
    name = "mailout",
    version = "1.0a1.dev2",
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "templated mail campaigns based on customizable queries",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/mailout",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
