.. _models:


Usage
=====

.. note:: For extended and more in depth examples, refer to :ref:`examples`

The following example illustrates how this module works.

.. code-block:: python
    :linenos:

    from json2py.models import *
    class Example(NestedField):
        hello = TextField(name = 'hi')
        integer = IntegerField()
        floating = FloatField()

    class ExampleList(ListField):
        __model__ = Example

    dict_var = {'hi': 'world', 'integer': 1000, 'floating': 10.5, 'ignored': "you won't see me"}
    list_var = [dict_var] * 3

    myMappedList = ExampleList(list_var)

    myMappedList[1].integer.value = 1234

    print myMappedList.json_encode(indent = 4)

Should return something like:

.. code-block:: json
    :emphasize-lines: 8

    [
        {
            "integer": 1000,
            "floating": 10.5,
            "hello": "world"
        },
        {
            "integer": 1234,
            "floating": 10.5,
            "hello": "world"
        },
        {
            "integer": 1000,
            "floating": 10.5,
            "hello": "world"
        }
    ]

Models
______

.. note:: The classes of this modules are intended to be reimplemented in order to make use of this module.

Models represent basic JSON data types. The usage of this models is intended
to be subclassed in order to fully map the original JSON structure.

.. py:module:: json2py.models

BaseField
---------

.. autoclass:: BaseField
    :members:

TextField
---------

.. autoclass:: TextField
    :members:

IntegerField
------------

.. autoclass:: IntegerField
    :members:


FloatField
----------

.. autoclass:: FloatField
    :members:

.. todo::

    Document how to access elements in :class:`.NestedField` with same name than Python's reserved keywords.

NestedField
-----------

.. autoclass:: NestedField
    :members:

ListField
---------

.. autoclass:: ListField
    :members:
