try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to "
        "https://pypi.python.org/pypi/setuptools and follow the instructions "
        "for installing setuptools"
    )

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='geosupport-suggest',
    version='0.0.1',
    url='https://github.com/ishiland/geosupport-suggest',
    description='Retrieve address suggestions from Geosupport',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ian Shiland',
    author_email='ishiland@gmail.com',
    packages=['suggest'],
    include_package_data=True,
    license='MIT',
    keywords=['NYC', 'geocoder', 'python-geosupport', 'geosupport', 'geosupport-suggest'],
    classifiers=[
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=requirements,
    test_suite="tests"
)
