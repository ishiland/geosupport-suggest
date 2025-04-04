from setuptools import setup, find_packages
import os
import subprocess


def get_version():
    """
    Get version from git tag or file.
    If in CI/CD with a tag, use the tag as version.
    Otherwise, use 0.1.0.dev0 for development.
    """
    try:
        # Try to get version from git tag
        process = subprocess.Popen(
            ["git", "describe", "--tags", "--abbrev=0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            version = stdout.decode("ascii").strip()
            # Remove 'v' prefix if present
            if version.startswith("v"):
                version = version[1:]
            return version
    except (subprocess.SubprocessError, OSError):
        pass

    # If git is not available or no tag exists
    # Check for CI/CD environment variables (GitHub Actions)
    if "GITHUB_REF" in os.environ and os.environ["GITHUB_REF"].startswith("refs/tags/v"):
        version = os.environ["GITHUB_REF"].split("/")[-1]
        if version.startswith("v"):
            version = version[1:]
        return version

    # Default development version if no tags found
    return "0.1.0.dev0"


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="geosupport-suggest",
    version=get_version(),
    url="https://github.com/ishiland/geosupport-suggest",
    description="Retrieve address suggestions from Geosupport",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Shiland",
    author_email="ishiland@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    keywords=["NYC", "geocoder", "python-geosupport", "geosupport", "geosupport-suggest"],
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
