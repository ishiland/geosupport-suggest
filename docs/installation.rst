Installation
============

Requirements
-----------

geosupport-suggest requires:

* Python 3.8+
* `python-geosupport <https://github.com/ishiland/python-geosupport>`_ library
* `nyc-parser <https://github.com/ishiland/nyc-parser>`_ library
* NYC Planning's Geosupport Desktop Edition

From PyPI
---------

You can install the latest release from PyPI:

.. code-block:: bash

    pip install geosupport-suggest

From Source
----------

Or install from source for the latest development version:

.. code-block:: bash

    git clone https://github.com/ishiland/geosupport-suggest.git
    cd geosupport-suggest
    pip install .

Geosupport Setup
--------------

To use this package, you need to have Geosupport Desktop Edition installed and configured for use with 
the python-geosupport library. Please refer to the `python-geosupport documentation <https://github.com/ishiland/python-geosupport>`_
for setup instructions.

Verifying Installation
---------------------

You can verify your installation by running:

.. code-block:: python

    from geosupport import Geosupport
    from suggest import GeosupportSuggest

    # Create and initialize objects
    g = Geosupport()
    s = GeosupportSuggest(g)

    # Test a simple address lookup
    results = s.suggestions('100 Gold St')
    
    # If successful, you should see address results
    print(len(results))
    print(s.format_address(results[0])) 