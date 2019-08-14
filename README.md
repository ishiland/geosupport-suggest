# geosupport-suggest
Retrieve address suggestions from Geosupport using [python-geosupport](https://github.com/ishiland/python-geosupport) and a single input address.

Note that not all returned suggestions will be valid addresses, they are only valid street names in the returned boro. When paired with the input house number, some of these addresses may be out of range.  
 
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

# create a GeosupportSuggest object using the Geosupport object
s = GeosupportSuggest(g)
```

### Get Suggestions
```python
# get suggestions - requires at least phn and first street name character. Any `matches` return full geosupport results.
>> s.get_suggestions('100 Gol')

# ~40 suggestions returned:
{'matches': [],
'suggestions': [
         {'phn': '100', 'street': 'GOETHALS HALL', 'boro_code': 1, 'boro_name': 'MANHATTAN', 'display': '100 GOETHALS HALL, MANHATTAN'},
         {'phn': '100', 'street': 'GOLD ST EXTENSION', 'boro_code': 1, 'boro_name': 'MANHATTAN', 'display': '100 GOLD ST EXTENSION, MANHATTAN'},
         {'phn': '100', 'street': 'GOLD STREET', 'boro_code': 1, 'boro_name': 'MANHATTAN', 'display': '100 GOLD STREET, MANHATTAN'},
         ...   
         {'phn': '100', 'street': 'GOBLE PG', 'boro_code': 2, 'boro_name': 'BRONX', 'display': '100 GOBLE PG, BRONX'},
         {'phn': '100', 'street': 'GOBLE PLACE', 'boro_code': 2, 'boro_name': 'BRONX', 'display': '100 GOBLE PLACE, BRONX'},
         {'phn': '100', 'street': 'GODWIN TERRACE', 'boro_code': 2, 'boro_name': 'BRONX', 'display': '100 GODWIN TERRACE, BRONX'},
         ...   
         {'phn': '100', 'street': 'GOFF II', 'boro_code': 4, 'boro_name': 'QUEENS', 'display': '100 GOFF II, QUEENS'},
         {'phn': '100', 'street': 'GOLD COURT', 'boro_code': 4, 'boro_name': 'QUEENS', 'display': '100 GOLD COURT, QUEENS'},
         {'phn': '100', 'street': 'GOLD PLAZA', 'boro_code': 4, 'boro_name': 'QUEENS', 'display': '100 GOLD PLAZA, QUEENS'},
         ...
         {'phn': '100', 'street': 'GOETHALS AVENUE', 'boro_code': 5, 'boro_name': 'STATEN ISLAND', 'display': '100 GOETHALS AVENUE, STATEN ISLAND'},
         {'phn': '100', 'street': 'GOETHALS BR AP EASTBOUND ROADBED', 'boro_code': 5, 'boro_name': 'STATEN ISLAND', 'display': '100 GOETHALS BR AP EASTBOUND ROADBED, STATEN ISLAND'},
         {'phn': '100', 'street': 'GOETHALS BR AP WESTBOUND ROADBED', 'boro_code': 5, 'boro_name': 'STATEN ISLAND', 'display': '100 GOETHALS BR AP WESTBOUND ROADBED, STATEN ISLAND'},
         ...
    ]
}
```
### Matches
if a match is found, the full geosupport result is returned. 
```python
>> s.get_suggestions('100 Gold st, Manhattan')

{'matches': [
    {'First Borough Name': 'MANHATTAN', 
    'House Number - Display Format': '100', 
    'House Number - Sort Format': '000100000AA', 
    'B10SC - First Borough and Street Code': '12135001010', 
    'First Street Name Normalized': 'GOLD STREET', 
    ...}
    ],
'suggestions':[]
}

```

### Contribute
Issues and PRs welcome.


### License
MIT
