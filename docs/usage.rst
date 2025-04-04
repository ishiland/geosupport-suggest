Usage
=====

Basic Usage
----------

The core functionality of geosupport-suggest is to find valid addresses from partial input:

.. code-block:: python

    from geosupport import Geosupport
    from suggest import GeosupportSuggest

    # Create a Geosupport object
    g = Geosupport()

    # Create a GeosupportSuggest object
    s = GeosupportSuggest(g)

    # Get suggestions for an address
    results = s.suggestions('100 Gold')

    # Print the results
    for result in results:
        print(f"{result['House Number - Display Format']} {result['First Street Name Normalized']}, {result['First Borough Name']}")

Advanced Features
---------------

Memory Caching
^^^^^^^^^^^^^

Enable memory caching to improve performance for repeated queries:

.. code-block:: python

    # Create with caching enabled
    s = GeosupportSuggest(g, use_cache=True, cache_size=500, cache_ttl=3600)
    
    # Repeated calls with the same input will use the cache
    results1 = s.suggestions('100 Gold St')  # Makes API call
    results2 = s.suggestions('100 Gold St')  # Uses cached result

Parallel Processing
^^^^^^^^^^^^^^^^^

For better performance when searching across multiple boroughs:

.. code-block:: python

    # Use parallel processing
    results = s.suggestions('100 Gold St', parallel=True)

Batch Processing
^^^^^^^^^^^^^^

Process multiple addresses at once:

.. code-block:: python

    addresses = [
        '100 Gold St',
        '350 5th Ave',
        {'address': '1 Police Plaza', 'borough_code': 1}
    ]
    
    # Process all addresses
    batch_results = s.suggestions_batch(addresses, parallel=True)

GeoJSON Export
^^^^^^^^^^^^

Convert results to GeoJSON format for mapping:

.. code-block:: python

    # Get suggestions
    results = s.suggestions('350 5th Ave')
    
    # Convert to GeoJSON
    geojson = s.to_geojson(results)
    
    # Write to file
    import json
    with open('addresses.geojson', 'w') as f:
        json.dump(geojson, f)

Normalized Results
^^^^^^^^^^^^^^^^

Get standardized result format:

.. code-block:: python

    # Get suggestions
    results = s.suggestions('350 5th Ave')
    
    # Normalize to consistent format
    normalized = s.normalize_results(results)
    
    # Normalized results have consistent keys
    for address in normalized:
        print(f"{address['house_number']} {address['street']}, {address['borough']}")
        if address['coordinates']:
            print(f"Coordinates: {address['coordinates']['latitude']}, {address['coordinates']['longitude']}")

Using Context Manager
^^^^^^^^^^^^^^^^^^^

Use as a context manager to automatically clean up resources:

.. code-block:: python

    with GeosupportSuggest(g) as s:
        results = s.suggestions('100 Gold St')
        # Process results
    # Resources are automatically cleared when exiting the context

Rate Limiting
^^^^^^^^^^^

Protect APIs with rate limiting:

.. code-block:: python

    # Limit to one request per second
    s = GeosupportSuggest(g, rate_limit=1.0)
    
    # Calls will be spaced at least 1 second apart
    results1 = s.suggestions('100 Gold St')
    results2 = s.suggestions('200 Broadway') 