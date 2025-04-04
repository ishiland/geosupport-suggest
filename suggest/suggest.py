from geosupport import GeosupportError
from nycparser import Parser
from typing import List, Dict, Any, Optional, Union, Tuple, TypeVar
import concurrent.futures
import logging
import time
import hashlib
from collections import OrderedDict
import threading

# Configure logging
logger = logging.getLogger(__name__)

# Initialize parser
parser = Parser()

# Valid borough codes
VALID_BOROUGH_CODES = {1, 2, 3, 4, 5}

# Type variables for better generic typing
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# Type definitions for common structures
AddressResult = Dict[str, Any]
AddressList = List[AddressResult]
GeoJSON = Dict[str, Any]
NormalizedAddress = Dict[str, Any]
CoordinatePair = Tuple[float, float]


class ThreadSafeMemoryCache:
    """Thread-safe in-memory LRU cache with TTL."""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.cache: Dict[str, Tuple[Any, float]] = OrderedDict()
        self._lock = threading.RLock()  # Reentrant lock for thread safety

    def _get_key(self, *args, **kwargs) -> str:
        """Generate a unique key for the function arguments."""
        key_parts = [str(args), str(sorted(kwargs.items()))]
        key_str = "".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Thread-safe get from cache."""
        with self._lock:
            if key not in self.cache:
                return None

            value, expiry = self.cache[key]

            if time.time() > expiry:
                del self.cache[key]
                return None

            self.cache.move_to_end(key)
            return value

    def set(self, key: str, value: Any) -> None:
        """Thread-safe add to cache."""
        with self._lock:
            expiry = time.time() + self.ttl

            if key in self.cache:
                self.cache[key] = (value, expiry)
                self.cache.move_to_end(key)
                return

            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)

            self.cache[key] = (value, expiry)

    def clear(self) -> None:
        """Thread-safe clear cache."""
        with self._lock:
            self.cache.clear()

    def remove_expired(self) -> int:
        """Thread-safe removal of expired items."""
        with self._lock:
            now = time.time()
            expired_keys = [k for k, (_, exp) in self.cache.items() if exp < now]
            for k in expired_keys:
                del self.cache[k]
            return len(expired_keys)


# Function decorator for caching
def cached_method(cache_instance):
    """Decorator to cache method results."""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Only use cache if it's enabled
            if not hasattr(self, "use_cache") or not self.use_cache:
                return func(self, *args, **kwargs)

            cache = getattr(self, cache_instance)
            if cache is None:
                return func(self, *args, **kwargs)

            # Generate cache key
            key = cache._get_key(*args, **kwargs)

            # Try to get from cache
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result

            # If not in cache, call the function
            result = func(self, *args, **kwargs)

            # Cache the result
            cache.set(key, result)
            return result

        return wrapper

    return decorator


class AddressFormatter:
    """Consistent formatting for address components."""

    @staticmethod
    def format_borough(borough_name: Optional[str]) -> str:
        """Format borough name consistently."""
        if not borough_name:
            return ""
        return borough_name.upper()

    @staticmethod
    def format_bbl(bbl_data: Optional[Union[Dict[str, Any], str]]) -> Optional[str]:
        """Extract BBL consistently from different formats."""
        if not bbl_data:
            return None

        if isinstance(bbl_data, dict):
            return bbl_data.get("BOROUGH BLOCK LOT (BBL)")
        return str(bbl_data)

    @staticmethod
    def format_coordinates(
        lat: Optional[Union[str, float]], lon: Optional[Union[str, float]]
    ) -> Optional[Dict[str, float]]:
        """Format coordinates consistently."""
        if lat is None or lon is None:
            return None

        try:
            return {"latitude": float(lat), "longitude": float(lon)}
        except (ValueError, TypeError):
            return None


class GeosupportSuggest:
    """Provides address suggestions from NYC Geosupport."""

    def __init__(
        self,
        geosupport=None,
        func="AP",
        max_workers=3,
        rate_limit=0,
        parser_options=None,
        use_cache=False,
        cache_size=1000,
        cache_ttl=3600,
    ):
        """
        Initialize GeosupportSuggest.

        Args:
            geosupport: Geosupport object
            func: Function to use ('AP' or '1B')
            max_workers: Max parallel workers
            rate_limit: Seconds between API calls (0 for no limit)
            parser_options: Dictionary of options to pass to nyc-parser
            use_cache: Enable caching of results
            cache_size: Maximum number of items in memory cache
            cache_ttl: Time-to-live in seconds for cached items
        """
        self._g = geosupport
        self.geofunction = func
        self.results = []
        self.similar_names = []
        self.max_workers = max_workers
        self.rate_limit = rate_limit
        self.last_call_time = 0

        # Initialize parser with custom options if provided
        if parser_options:
            self.parser = Parser(**parser_options)
        else:
            self.parser = parser

        # Initialize cache
        self.use_cache = use_cache
        if use_cache:
            self.cache = ThreadSafeMemoryCache(
                max_size=cache_size, ttl_seconds=cache_ttl
            )
        else:
            self.cache = None

        if self._g is None:
            raise ValueError(
                "You must initialize GeosupportSuggest with a Geosupport object."
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def clear(self):
        """Clear all results and similar names."""
        self.results = []
        self.similar_names = []

    def _respect_rate_limit(self):
        """Implement rate limiting if enabled."""
        if self.rate_limit > 0:
            elapsed = time.time() - self.last_call_time
            if elapsed < self.rate_limit:
                time.sleep(self.rate_limit - elapsed)
            self.last_call_time = time.time()

    def _geocode(self, phn, street, borough_code=None, zip=None):
        """Geocode or attempt to geocode an address."""
        self._respect_rate_limit()
        logger.debug(f"Geocoding: {phn} {street} (Borough: {borough_code}, ZIP: {zip})")

        # Validate borough code
        if borough_code and borough_code not in VALID_BOROUGH_CODES:
            logger.warning(f"Invalid borough code: {borough_code}")
            return

        try:
            r = self._g[self.geofunction](
                house_number=phn, street=street, borough_code=borough_code, zip=zip
            )
            self.results.append(r)
            logger.debug(
                f"Found result: {r.get('First Borough Name', 'Unknown')} - "
                f"{r.get('First Street Name Normalized', 'Unknown')}"
            )
        except GeosupportError as ge:
            if "SIMILAR NAMES" in ge.result.get("Message", ""):
                list_of_street_names = ge.result.get("List of Street Names", [])
                r = [
                    {"street": s, "borough_code": borough_code}
                    for s in list_of_street_names
                ]
                self.similar_names.extend(r)
                logger.debug(f"Found {len(list_of_street_names)} similar names")
            else:
                logger.warning(f"Geocoding error: {ge}")

    def _geocode_parallel(self, items):
        """Geocode multiple items in parallel."""
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            futures = []
            for item in items:
                futures.append(
                    executor.submit(
                        self._geocode,
                        item.get("phn"),
                        item.get("street"),
                        item.get("borough_code"),
                        item.get("zip"),
                    )
                )
            concurrent.futures.wait(futures)

    @cached_method("cache")
    def suggestions(
        self,
        input_address: str,
        borough_code: Optional[int] = None,
        parallel: bool = False,
    ) -> AddressList:
        """
        Get valid address suggestions from Geosupport.

        Args:
            input_address: Address string
            borough_code: Borough Code (1-5)
            parallel: Whether to use parallel processing

        Returns:
            List of valid addresses

        Raises:
            ValueError: If borough_code is invalid
        """
        parsed = self.parser.address(input_address)
        if borough_code:
            if borough_code not in VALID_BOROUGH_CODES:
                raise ValueError(
                    f"Invalid borough code: {borough_code}. Must be one of {VALID_BOROUGH_CODES}"
                )
            parsed["BOROUGH_CODE"] = borough_code

        self.similar_names = []
        self.results = []

        if not parsed.get("PHN") or not parsed.get("STREET"):
            logger.warning("No house number or street found in input")
            return self.results

        self._process_address_with_location_info(parsed, parallel)
        self._process_similar_names(parsed, parallel)

        # Filter None values and sort results
        self.results = [r for r in self.results if r is not None]
        self.results.sort(key=lambda x: x.get("First Borough Name", ""))
        return self.results

    def _process_address_with_location_info(self, parsed, parallel):
        """Process address based on available location information."""
        if not parsed.get("BOROUGH_CODE") and not parsed.get("ZIP"):
            self._process_all_boroughs(parsed, parallel)
        elif parsed.get("BOROUGH_CODE"):
            self._geocode(
                phn=parsed["PHN"],
                street=parsed["STREET"],
                borough_code=parsed["BOROUGH_CODE"],
            )
        elif parsed.get("ZIP"):
            self._geocode(phn=parsed["PHN"], street=parsed["STREET"], zip=parsed["ZIP"])

    def _process_all_boroughs(self, parsed, parallel):
        """Try the address in all five boroughs."""
        if parallel:
            items = [
                {
                    "phn": parsed["PHN"],
                    "street": parsed["STREET"],
                    "borough_code": x,
                }
                for x in range(1, 6)
            ]
            self._geocode_parallel(items)
        else:
            for x in range(1, 6):
                self._geocode(
                    phn=parsed["PHN"], street=parsed["STREET"], borough_code=x
                )

    def _process_similar_names(self, parsed, parallel):
        """Process any similar street names returned from Geosupport."""
        if not self.similar_names:
            return

        if parallel:
            items = [
                {
                    "phn": parsed["PHN"],
                    "street": name["street"],
                    "borough_code": name["borough_code"],
                }
                for name in self.similar_names
            ]
            self._geocode_parallel(items)
        else:
            for name in self.similar_names:
                self._geocode(
                    phn=parsed["PHN"],
                    street=name["street"],
                    borough_code=name["borough_code"],
                )

    def suggestions_batch(self, addresses, parallel=False):
        """Process multiple addresses in batch."""
        all_results = []
        for address in addresses:
            if isinstance(address, dict):
                addr_str = address.get("address", "")
                boro = address.get("borough_code")
            else:
                addr_str = address
                boro = None

            results = self.suggestions(addr_str, borough_code=boro, parallel=parallel)
            all_results.append(results)
        return all_results

    def format_address(self, result):
        """Format a result as a standard address string."""
        if not result:
            return ""

        borough = result.get("First Borough Name", "")
        house_num = result.get("House Number - Display Format", "")
        street = result.get("First Street Name Normalized", "")

        return f"{house_num} {street}, {borough}, NY"

    def to_geojson(self, results: AddressList) -> GeoJSON:
        """
        Convert results to GeoJSON format.

        Args:
            results: Address results to convert

        Returns:
            GeoJSON feature collection
        """
        features = []
        for r in results:
            # Skip results without coordinates
            if not all(k in r for k in ["Latitude", "Longitude"]):
                continue

            try:
                lon = float(r.get("Longitude", 0))
                lat = float(r.get("Latitude", 0))

                feature = {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "properties": {
                        "address": self.format_address(r),
                        "borough": r.get("First Borough Name", ""),
                        "block": r.get("BOROUGH BLOCK LOT (BBL)", {}).get(
                            "Tax Block", ""
                        ),
                        "lot": r.get("BOROUGH BLOCK LOT (BBL)", {}).get("Tax Lot", ""),
                    },
                }
                features.append(feature)
            except (ValueError, TypeError):
                continue

        return {"type": "FeatureCollection", "features": features}

    def normalize_results(self, results: AddressList) -> List[NormalizedAddress]:
        """
        Normalize results to a consistent format.

        Handles potential missing fields and standardizes structure.
        """
        normalized = []
        for r in results:
            if not r:
                continue

            norm = {
                "house_number": r.get("House Number - Display Format", ""),
                "street": r.get("First Street Name Normalized", ""),
                "borough": AddressFormatter.format_borough(r.get("First Borough Name")),
                "zip": r.get("ZIP Code", ""),
                "coordinates": AddressFormatter.format_coordinates(
                    r.get("Latitude"), r.get("Longitude")
                ),
                "bbl": AddressFormatter.format_bbl(r.get("BOROUGH BLOCK LOT (BBL)")),
            }

            normalized.append(norm)

        return normalized
