from json import JSONEncoder
from .models import NestedField, ListField, DateField, BaseField

__author__ = 'Victor'


class BaseEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NestedField):
            return dict([(k if v.name is None else v.name, self.default(v)) for k, v in obj.items()])
        elif isinstance(obj, ListField):
            return [self.default(v) for v in obj.value]
        elif isinstance(obj, DateField):
            return obj.json_encode()
        elif isinstance(obj, BaseField):
            return obj.value
        else:
            return JSONEncoder.default(self, obj) # super(MyEncoder, self).default(obj)