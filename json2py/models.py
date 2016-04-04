from past.builtins import basestring
from builtins import int
import json
from dateutil.parser import parse
from datetime import datetime
import calendar

__author__ = 'Victor'


class ParseException(Exception):
    """
    Exception raised when an error occur trying to parse data on any
    of :class:`.BaseField` subclasses.
    """
    pass


class InvalidAttribute(Exception):
    """
    Exception raised when invalid attribute is set on :class:`.NestedField`
    """
    pass


class BaseField(object):
    """
    Base Class holding and defining common features for all the other subclasses.

    :arg value: Value to be stored
    :arg name: Name of the field in source data.
    :arg required: Whether raise LookupError when key is missing or not.
    :note: This class must be treated as abstract class and should not be reimplemented.
    """
    def __init__(self, value = None, name = None, required = True):
        """
        :class:`.BaseField` constructor
        :param name: Name of the field in source data.
        """
        self.name = name
        self.required = required

    def json_encode(self, **kwargs):
        """
        Converts an object of class :class:`.BaseField` into JSON representation (string)
        using :class:`.BaseEncoder` JSONEncoder.

        :param kwargs: Parameters passed to :py:func:`json.dumps`
        :return: JSON-string representation of this object.
        """
        kwargs.pop('cls', None)
        return json.dumps(self, cls = BaseEncoder, **kwargs)

    def json_decode(self, data, **kwargs):
        """
        Parses a JSON-string into this object. This method is intended to build
        the JSON to Object map, so it doesn't return any value, instead, the object
        is built into itself.

        :param data: JSON-string passed to :py:func:`json.loads`
        :param kwargs: Parameters passed to :py:func:`json.loads`
        """
        kwargs.pop('object_hook', None)
        json.loads(data, object_hook = self._dict_to_obj, **kwargs)

    def _dict_to_obj(self, d):
        self.__init__(d)


class BooleanField(BaseField):
    """
    Class representing boolean field in JSON.

    :arg value: It is the raw data that is this object will represent once parsed.
    :arg name: It has the same meaning as in :class:`.BaseField`
    :arg required: It has the same meaning as in :class:`.BaseField`
    :raise `ParseException`: If ``value`` is not boolean nor None
    """
    def __init__(self, value = None, name = None, required = True):
        super(BooleanField, self).__init__(value, name, required)
        self.value = value

        if not isinstance(self.value, bool) and self.value is not None:
            raise ParseException('BooleanField cannot parse non bool')

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class TextField(BaseField):
    """
    Class representing a string field in JSON.

    :arg value: It is the raw data that is this object will represent once parsed.
    :arg name: It has the same meaning as in :class:`.BaseField`
    :arg required: It has the same meaning as in :class:`.BaseField`
    :raise ParseException: If ``value`` is not a string nor None
    """
    def __init__(self, value = None, name = None, required = True):
        super(TextField, self).__init__(value, name, required)
        self.value = value

        if not isinstance(self.value, basestring) and self.value is not None:
            raise ParseException('TextField cannot parse non string')

    def __str__(self):
        return str(self.value)  ## Use str() to avoid None's

    def __repr__(self):
        return self.__str__()


class NumberField(BaseField):
    """
    Abstract class for representing JSON numbers.
    It really does nothing
    """
    def __init__(self, value = None, name = None, required = True):
        super(NumberField, self).__init__(value, name, required)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class IntegerField(NumberField):
    """
    Class representing an integer field in JSON.

    :arg value: It is the raw data that is this object will represent once parsed.
    :arg name: It has the same meaning as in :class:`.BaseField`
    :arg required: It has the same meaning as in :class:`.BaseField`
    :raise ParseException: If ``value`` is not a integer nor None
    """
    def __init__(self, value = None, name = None, required = True):
        super(NumberField, self).__init__(value, name, required)
        self.value = value

        if not isinstance(self.value, int) and self.value is not None:
            raise ParseException('IntegerField cannot parse non integer')


class FloatField(NumberField):
    """
    Class representing a float field in JSON.

    :arg value: It is the raw data that is this object will represent once parsed.
    :arg name: It has the same meaning as in :class:`.BaseField`
    :arg required: It has the same meaning as in :class:`.BaseField`
    :raise ParseException: If ``value`` is not a float nor None
    """
    def __init__(self, value = None, name = None, required = True):
        super(NumberField, self).__init__(value, name, required)
        self.value = value

        if not isinstance(self.value, (float, int)) and self.value is not None:
            raise ParseException('FloatField cannot parse non float')


class NestedField(BaseField):
    """
    Class representing a document field in JSON.

    :arg value: It is the raw data that is this object will represent once parsed.
    :arg name: It has the same meaning as in :class:`.BaseField`
    :arg required: It has the same meaning as in :class:`.BaseField`
    :raise `ParseException`: If ``value`` is not a dict nor None
    :raise `InvalidAttribute`: If a reserved keyword is used as attribute

    :note: Reserved keywords are: ``name``, ``value`` and ``required``
    :note: For use cases and examples refer to :doc:`examples`
    """
    __forbiddenAttrs = ['name', 'value', 'required']

    def __new__(cls, *args, **kwargs):
        forbidden_intersection = set(dir(cls)).intersection(NestedField.__forbiddenAttrs)
        if len(forbidden_intersection) > 0:
            raise InvalidAttribute('%s cannot be used as attribute names, use name keyword for bypassing this limitation' %(', '.join(forbidden_intersection)))
        return super(NestedField, cls).__new__(cls)

    def __init__(self, value = None, name = None, required = True):
        super(NestedField, self).__setattr__('value', {})
        super(NestedField, self).__setattr__('name', name)
        super(NestedField, self).__setattr__('required', required)
        super(NestedField, self).__init__(value, name, required)

        data = value
        if not isinstance(data, dict) and data is not None:
            raise ParseException('NestedField cannot parse non dict')

        if data is not None:
            specificFields = set(dir(self.__class__)) - set(dir(NestedField))
            lookUpKeys = {}
            reverseLookUp = {}
            for fieldName in specificFields:
                field = getattr(self.__class__, fieldName)
                if field.name is not None:
                    lookUpKeys[field.name] = field
                    reverseLookUp[field.name] = fieldName
                else:
                    lookUpKeys[fieldName] = field
                    reverseLookUp[fieldName] = fieldName

            for key, field in lookUpKeys.items():
                if key not in data and field.required:
                    raise LookupError('%s was not found on data dict' % key)
                elif key in data:
                    field = field.__class__(value = data[key], name = field.name, required = field.required)
                else:
                    field = field.__class__(value = None, name = field.name, required = field.required)

                super(NestedField, self).__getattribute__('value')[reverseLookUp[key]] = field
                # setattr(self, reverseLookUp[key], field)

    def __setattr__(self, key, value):
        if key in self.__dict__ and key != 'value':
            super(NestedField, self).__setattr__(key, value)
        else:
            self.value[key] = value

    def __getattr__(self, key):
        try:
            return super(NestedField, self).__getattribute__('value')[key]
        except KeyError:
            raise AttributeError(key)

    def __getattribute__(self, item):
        if item not in super(NestedField, self).__getattribute__('value'):
            return super(NestedField, self).__getattribute__(item)
        else:
            raise AttributeError(item)

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    @staticmethod
    def parse(data, cls):
        obj = cls(data)
        return obj

    def items(self):
        return super(NestedField, self).__getattribute__('value').items()


class ListField(BaseField):
    """
    Class representing a list field in JSON. This class implements :mod:`list` interface so you
    can slicing, appending, popping, etc.

    :arg name: It has the same meaning as in :class:`.BaseField`
    :arg value: It is the raw data that is this object will represent once parsed.
    :arg required: It has the same meaning as in :class:`.BaseField`
    :raise ParseException: If ``value`` is not a list nor None

    :note: Hinting the structure of values of the list should be done using the meta variable :attr:`__model__`
     inside class reimplementation.

    :note: JSON lists' values can be of any type even in the same list, but
     in real world apps, every JSON lists' values should be of the same type, this
     behaviour also simplifies this module, so this class expects that all values in
     lists must have the same structure.

    """
    def __init__(self, value = None, name = None, required = True):
        super(ListField, self).__init__(value, name, required)

        try:
            elementClass = self.__model__
        except Exception as e:
            raise ValueError('__model__ class variable must be defined')

        if elementClass is None:
            raise ValueError('__model__ cannot be None')

        if not issubclass(elementClass, BaseField):
            raise ValueError('__model__ must be a BaseField subclass')

        if not isinstance(value, list) and value is not None:
            raise ParseException('ListField cannot parse non list')

        self.value = [elementClass(d) for d in value] if value is not None else []

    def _dict_to_obj(self, d):
        self.value.append(self.__model__(d))
        return self.value[-1]

    def append(self, x):
        return self.value.append(x)

    def extend(self, L):
        return self.value.extend(L)

    def insert(self, x):
        return self.value.insert(x)

    def remove(self, x):
        return self.value.remove(x)

    def pop(self, i = None):
        return self.value.pop(i)

    def index(self, x):
        return self.value.index(x)

    def count(self, x):
        return self.value.count(x)

    def sort(self, cmp = None, key = None, reverse = False):
        return self.value.sort(cmp, key, reverse)

    def reverse(self):
        return self.value.reverse()

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        del self.value[key]

    def __iter__(self):
        return iter(self.value)

    def __reversed__(self):
        return reversed(self.value)

class DateField(BaseField):
    """
    Class used to parse and represent dates. It makes use of :mod:`datetime` and :mod:`dateutil`.

    :arg name: It has the same meaning as in :class:`.BaseField`
    :arg value: It is the raw data that is this object will represent once parsed.
    :arg required: It has the same meaning as in :class:`.BaseField`
    :arg formatting: Format used to represent date.
    :raise ParseException: If ``value`` is not valid nor None

    :note: Several format's can be in ``formatting``: **auto**: use :meth:`dateutil.parser.parse`,
        **timestamp**: provide UNIX timestamp and use :meth:`datetime.datetime.utcfromtimestamp` and
        **custom string**: use any format in compliance with :meth:`datetime.datetime.strptime` valid
        formats.

    """
    def __init__(self, value = None, name = None, required = True, formatting = "%Y-%m-%dT%H:%M:%SZ"):
        super(DateField, self).__init__(value, name, required)
        self.value = None
        self.formatting = formatting

        field_type = 'str'
        if formatting == 'timestamp':
            field_type = 'int'

        if field_type == 'str':
            if not isinstance(value, basestring) and value is not None:
                raise ParseException("DateField cannot parse non string with formatting specified '%s'" % self.formatting)
        elif field_type == 'int':
            if not isinstance(value, int) and value is not None:
                raise ParseException("DateField cannot parse non integer with formatting specified '%s'" % self.formatting)

        if value is not None:
            if self.formatting == 'timestamp':
                self.value = datetime.utcfromtimestamp(value)
            elif self.formatting == 'auto':
                self.value = parse(value)
            else:
                self.value = datetime.strptime(value, self.formatting)

    def json_encode(self, **kwargs):
        if self.value is None:
            return json.dumps(self.value, **kwargs)
        else:
            if self.formatting == 'timestamp':
                return json.dumps(calendar.timegm(self.value.timetuple()), **kwargs)
            else:
                formatting = self.formatting
                if self.formatting == 'auto':
                    formatting = "%Y-%m-%dT%H:%M:%SZ"

                return json.dumps(self.value.strftime(formatting), **kwargs)

from .encoder import BaseEncoder
