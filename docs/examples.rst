Examples
========

Basic Address Lookup
------------------

.. code-block:: python

    from geosupport import Geosupport
    from suggest import GeosupportSuggest

    # Initialize
    g = Geosupport()
    s = GeosupportSuggest(g)

    # Get address suggestions
    results = s.suggestions('100 Gold')

    # Print formatted addresses
    for result in results:
        print(s.format_address(result))

Specify Borough
-------------

.. code-block:: python

    # Search only in Manhattan (borough code 1)
    manhattan_results = s.suggestions('100 Gold', borough_code=1)

    # Print results
    for result in manhattan_results:
        print(s.format_address(result))

Create a Simple Address Lookup Web API
-----------------------------------

Using Flask:

.. code-block:: python

    from flask import Flask, request, jsonify
    from geosupport import Geosupport
    from suggest import GeosupportSuggest

    app = Flask(__name__)

    # Initialize once for the application
    g = Geosupport()
    s = GeosupportSuggest(g, use_cache=True)

    @app.route('/suggest')
    def suggest():
        # Get address from query parameter
        address = request.args.get('address', '')
        if not address:
            return jsonify({"error": "Address parameter is required"}), 400
            
        # Get optional borough code
        borough = request.args.get('borough')
        if borough:
            try:
                borough = int(borough)
            except ValueError:
                return jsonify({"error": "Borough must be a number (1-5)"}), 400
        
        # Get suggestions
        try:
            results = s.suggestions(address, borough_code=borough)
            
            # Normalize for consistent output
            normalized = s.normalize_results(results)
            
            return jsonify({
                "query": address,
                "results": normalized,
                "count": len(normalized)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if __name__ == '__main__':
        app.run(debug=True)

Create a GeoJSON Map
------------------

Using Folium:

.. code-block:: python

    import folium
    import json
    from geosupport import Geosupport
    from suggest import GeosupportSuggest

    # Initialize
    g = Geosupport()
    s = GeosupportSuggest(g)

    # Get suggestions for multiple addresses
    addresses = [
        '350 5th Ave, Manhattan',  # Empire State Building
        '20 W 34th St, Manhattan',  # Macy's
        '45 Rockefeller Plaza, New York'  # Rockefeller Center
    ]

    all_results = []
    for address in addresses:
        results = s.suggestions(address)
        all_results.extend(results)

    # Convert to GeoJSON
    geojson_data = s.to_geojson(all_results)

    # Create a map centered on NYC
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

    # Add GeoJSON to map
    folium.GeoJson(
        geojson_data,
        name='Locations',
        popup=folium.GeoJsonPopup(fields=['address', 'borough'])
    ).add_to(m)

    # Save map
    m.save('nyc_locations.html')

Batch Processing with Progress Bar
--------------------------------

.. code-block:: python

    import time
    from tqdm import tqdm
    from geosupport import Geosupport
    from suggest import GeosupportSuggest

    # Initialize
    g = Geosupport()
    s = GeosupportSuggest(g, rate_limit=0.5)  # Limit to 2 requests per second

    # List of addresses to process
    addresses = [
        '100 Gold St',
        '350 5th Ave',
        '1 Police Plaza',
        '20 W 34th St',
        # ... many more addresses
    ]

    # Process with progress bar
    results = []
    for address in tqdm(addresses, desc="Geocoding"):
        result = s.suggestions(address)
        results.append(result)
        
    # Summarize
    print(f"Processed {len(addresses)} addresses")
    print(f"Found {sum(len(r) for r in results)} total matches") 