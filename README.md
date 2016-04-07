# json2py

## Description
Convert JSON/dict to python object and vice versa

## Installation
```
pip install json2py
```

## Example
Using json2py makes treating with Python dicts as simple as:
```python
    from json2py.models import *
    # Define basic object map
    class Example(NestedField):
        hello = TextField(name = 'hi')
        integer = IntegerField()
        floating = FloatField()

    # Define list map
    class ExampleList(ListField):
        __model__ = Example

    # Sample variables
    dict_var = {'hi': 'world', 'integer': 1000, 'floating': 10.5, 'ignored': "you won't see me"}
    list_var = [dict_var] * 3

    # Do the magic
    myMappedList = ExampleList(list_var)

    # Modify integer field of second list element
    myMappedList[1].integer.value = 1234

    # Show the results
    print myMappedList.json_encode(indent = 4)
```

Output:
```javascript
    [
        {
            "integer": 1000,
            "floating": 10.5,
            "hi": "world"
        },
        {
        // Notice how "integer" value has changed
            "integer": 1234,
            "floating": 10.5,
            "hi": "world"
        },
        {
            "integer": 1000,
            "floating": 10.5,
            "hi": "world"
        }
    ]
```

Please, refer to [Documentation examples](http://json2py.readthedocs.org/en/latest/examples.html) for more examples.

## Build Status
[![Build Status](https://travis-ci.org/Wiston999/json2py.svg?branch=master)](https://travis-ci.org/Wiston999/json2py)

## Documentation
[![Documentation Status](https://readthedocs.org/projects/json2py/badge/?version=latest)](http://json2py.readthedocs.org/en/latest/?badge=latest)

## Issues status
[![Stories in Ready](https://badge.waffle.io/Wiston999/json2py.png?label=ready&title=Ready)](https://waffle.io/Wiston999/json2py)

