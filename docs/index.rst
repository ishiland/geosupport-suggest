Welcome to geosupport-suggest's documentation!
=========================================

geosupport-suggest provides a Python interface for retrieving address suggestions from NYC Geosupport. 
It works with the `python-geosupport <https://github.com/ishiland/python-geosupport>`_ library to offer
enhanced address matching, validation, and geocoding capabilities.

Features
--------

* Thread-safe memory caching for improved performance
* Parallel processing of address queries
* GeoJSON export of geocoding results 
* Address normalization
* Consistent result formatting
* Borough code validation
* Rate limiting for API protection
* Context manager support

Installation
-----------

.. code-block:: bash

    pip install geosupport-suggest

Basic Usage
----------

.. code-block:: python

    from geosupport import Geosupport
    from suggest import GeosupportSuggest

    # Create a Geosupport object
    g = Geosupport()

    # Create a GeosupportSuggest object with caching enabled
    s = GeosupportSuggest(g, use_cache=True)

    # Get address suggestions
    results = s.suggestions('100 Gold')

    # Print the formatted addresses
    for result in results:
        print(s.format_address(result))

    # Convert to GeoJSON
    geojson = s.to_geojson(results)

    # Normalize results to a consistent format
    normalized = s.normalize_results(results)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   examples
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 