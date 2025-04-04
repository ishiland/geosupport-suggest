API Reference
============

GeosupportSuggest
---------------

.. autoclass:: suggest.GeosupportSuggest
   :members:
   :special-members: __init__, __enter__, __exit__

ThreadSafeMemoryCache
-------------------

.. autoclass:: suggest.ThreadSafeMemoryCache
   :members:

AddressFormatter
--------------

.. autoclass:: suggest.AddressFormatter
   :members:

Constants
--------

.. data:: suggest.VALID_BOROUGH_CODES
   :type: Set[int]
   
   Valid borough codes (1-5)

Type Definitions
--------------

.. code-block:: python

   # Type definitions for common structures
   AddressResult = Dict[str, Any]
   AddressList = List[AddressResult]
   GeoJSON = Dict[str, Any]
   NormalizedAddress = Dict[str, Any]
   CoordinatePair = Tuple[float, float] 