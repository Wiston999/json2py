import json

__author__ = 'Victor'


class ParseException(Exception): pass


class BaseField(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)

    def json_encode(self, **kwargs):
        kwargs.pop('cls', None)
        return json.dumps(self, cls = BaseEncoder, **kwargs)

    def json_decode(self, data, **kwargs):
        kwargs.pop('object_hook', None)
        json.loads(data, object_hook = self._dictToObj, **kwargs)

    def _dictToObj(self, d):
        self.__init__(d)

    @staticmethod
    def parse(data, cls):
        obj = cls(data)
        return obj

class TextField(BaseField):
    def __init__(self, *args, **kwargs):
        super(TextField, self).__init__(**kwargs)
        self.value = args[0] if len(args) > 0 else kwargs.get('value')

        if not isinstance(self.value, (str, unicode)) and self.value is not None:
            raise ParseException('TextField cannot parse non string')

class NumberField(BaseField):
    def __init__(self, *args, **kwargs):
        super(NumberField, self).__init__(**kwargs)

class IntegerField(NumberField):
    def __init__(self, *args, **kwargs):
        super(NumberField, self).__init__(**kwargs)
        self.value = args[0] if len(args) > 0 else kwargs.get('value')

        if not isinstance(self.value, (int, long)) and self.value is not None:
            raise ParseException('IntegerField cannot parse non integer')

class FloatField(NumberField):
    def __init__(self, *args, **kwargs):
        super(NumberField, self).__init__(**kwargs)
        self.value = args[0] if len(args) > 0 else kwargs.get('value')

        if not isinstance(self.value, (float, int, long)) and self.value is not None:
            raise ParseException('FloatField cannot parse non float')

class NestedField(BaseField):
    def __init__(self, *args, **kwargs):
        super(NestedField, self).__setattr__('value', {})
        super(NestedField, self).__setattr__('name', kwargs.get('name', None))
        super(NestedField, self).__init__(**kwargs)

        data = args[0] if len(args) > 0 else kwargs.get('value')
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
                if key not in data:
                    raise LookupError('%s was not found on data dict' % key)
                field = field.__class__(data[key], field.__class__)
                self.value[reverseLookUp[key]] = field
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

    @staticmethod
    def parse(data, cls):
        obj = cls(data)
        return obj

    def items(self):
        return super(NestedField, self).__getattribute__('value').items()

class ListField(BaseField):
    def __init__(self, value = None, *args, **kwargs):
        super(ListField, self).__init__(**kwargs)

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

    def _dictToObj(self, d):
        self.value.append(self.__model__(d))
        return self.value[-1]

    @staticmethod
    def parse(data, cls):
        obj = cls(data)
        return obj

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

from .encoder import BaseEncoder