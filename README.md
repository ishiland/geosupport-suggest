# geosupport-suggest
Retrieve address suggestions from Geosupport using [python-geosupport](https://github.com/ishiland/python-geosupport) and a single input address.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/) [![Documentation Status](https://readthedocs.org/projects/geosupport-suggest/badge/?version=latest)](https://geosupport-suggest.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://img.shields.io/pypi/v/geosupport-suggest.svg)](https://pypi.python.org/pypi/geosupport-suggest/)

## Features

* Thread-safe memory caching for improved performance
* Parallel processing of address queries
* GeoJSON export of geocoding results 
* Address normalization with consistent formatting
* Borough code validation
* Rate limiting for API protection
* Context manager support
* Batch address processing

## Documentation

Full documentation is available at [geosupport-suggest.readthedocs.io](https://geosupport-suggest.readthedocs.io/).

## Install
```sh
$ pip install geosupport-suggest
```
or clone this repo, `cd` into it and
```sh
$ pip install .
```
## Quick Start

```python
from geosupport import Geosupport
from suggest import GeosupportSuggest

# create a Geosupport object
g = Geosupport()

# create a GeosupportSuggest object using Geosupport
s = GeosupportSuggest(g)

# Get suggestions
results = s.suggestions('100 Gold')

# Print formatted addresses
for result in results:
    print(s.format_address(result))
```

### Advanced Usage

Caching for improved performance:

```python
# Enable caching
s = GeosupportSuggest(g, use_cache=True)

# First call makes API request
results1 = s.suggestions('100 Gold St')

# Second call uses cache
results2 = s.suggestions('100 Gold St')  # Much faster
```

Convert results to GeoJSON:

```python
# Get address suggestions
results = s.suggestions('350 5th Ave')  # Empire State Building

# Convert to GeoJSON for mapping
geojson = s.to_geojson(results)
```

Process multiple addresses:

```python
addresses = [
    '100 Gold St',
    '350 5th Ave',
    {'address': '1 Police Plaza', 'borough_code': 1}  # With borough code
]

# Process all addresses (with parallel execution)
batch_results = s.suggestions_batch(addresses, parallel=True)
```

### Contribute
Issues and PRs welcome. See [Contributing](https://geosupport-suggest.readthedocs.io/en/latest/contributing.html) for details.

### License
MIT
