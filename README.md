# geosupport-suggest
Retrieve address suggestions from Geosupport using [python-geosupport](https://github.com/ishiland/python-geosupport) and a single input address.

## Install
```sh
$ pip install geosupport-suggest
```
or clone this repo, `cd` into it and
```sh
$ pip install .
```
## Usage

```python
from geosupport import Geosupport
from suggest import GeosupportSuggest

# create a Geosupport object
g = Geosupport()

# create a GeosupportSuggest object using Geosupport
s = GeosupportSuggest(g)

```

### Get Suggestions
Requires at least a house number and the first character of a street name. Each suggestion returns the full geosupport result.
```python
>> s.suggestions('100 Gold')
[
    {'First Borough Name': 'STATEN IS', 
    'House Number - Display Format': '100', 
    'House Number - Sort Format': '000100000AA', 
    'B10SC - First Borough and Street Code': '52981501010', 
    'First Street Name Normalized': 'GOLD AVENUE', 
    ...}, 
    {'First Borough Name': 'MANHATTAN', 
    'House Number - Display Format': '100', 
    'House Number - Sort Format': '000100000AA', 
    'B10SC - First Borough and Street Code': '12135001010', 
    'First Street Name Normalized': 'GOLD STREET', 
    ...},
    {'First Borough Name': 'BROOKLYN', 
    'House Number - Display Format': '100',
    'House Number - Sort Format': '000100000AA', 
    'B10SC - First Borough and Street Code': '34453001010', 
    'First Street Name Normalized': 'GOLD STREET',
    ...}
]
```

### Contribute
Issues and PRs welcome.


### License
MIT
