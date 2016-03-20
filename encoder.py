from json import JSONEncoder
from .models import NestedField, ListField, TextField, NumberField

__author__ = 'Victor'


class BaseEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NestedField):
            return dict([(k, self.default(v)) for k, v in obj.value.items()])
        elif isinstance(obj, ListField):
            return [self.default(v) for v in obj.value]
        elif isinstance(obj, (TextField, NumberField)):
            return obj.value
        else:
            return JSONEncoder.default(self, obj) # super(MyEncoder, self).default(obj)