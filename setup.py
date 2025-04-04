from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="geosupport-suggest",
    version="0.1.0",
    url="https://github.com/ishiland/geosupport-suggest",
    description="Retrieve address suggestions from Geosupport",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Shiland",
    author_email="ishiland@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    keywords=[
        "NYC",
        "geocoder",
        "python-geosupport",
        "geosupport",
        "geosupport-suggest",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "geosupport-suggest=suggest.cli:main",
        ],
    },
    test_suite="tests",
    extras_require={
        "docs": [
            "sphinx>=4.0.0",
            "sphinx_rtd_theme>=1.0.0",
        ],
        "test": [
            "pytest",
            "pytest-cov",
        ],
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
        ],
    },
)
