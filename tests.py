import unittest
import json
from json2py.models import TextField
from json2py.models import IntegerField
from json2py.models import FloatField
from json2py.models import NestedField
from json2py.models import ListField
from json2py.models import ParseException
__author__ = 'Victor'


class NestedObjTest(NestedField):
    id = IntegerField()
    key = IntegerField(name = 'clave')
    value = TextField()


class ListObjTest(ListField):
    __model__ = NestedObjTest


class TextTest(unittest.TestCase):
    def test_init(self):
        self.assertEqual(TextField('''"aBc"''').value, '''"aBc"''')
        self.assertEqual(TextField("5").value, "5")

        with self.assertRaises(ParseException):
            TextField(5)

    def test_encode(self):
        self.assertEqual(TextField("aBc").json_encode(), '"aBc"')
        self.assertEqual(TextField("5").json_encode(), '"5"')


class IntegerTest(unittest.TestCase):
    def test_init(self):
        self.assertEqual(IntegerField(10).value, 10)
        self.assertEqual(IntegerField(10L).value, 10)

        with self.assertRaises(ParseException):
            IntegerField('5')

        with self.assertRaises(ParseException):
            IntegerField(10.0)

    def test_encode(self):
        self.assertEqual(IntegerField(10).json_encode(), '10')
        self.assertEqual(IntegerField(10L).json_encode(), '10')


class FloatTest(unittest.TestCase):
    def test_init(self):
        self.assertEqual(FloatField(10).value, float(10))
        self.assertEqual(FloatField(10.0).value, float(10))
        self.assertEqual(FloatField(10L).value, float(10))
        self.assertEqual(FloatField(10.5).value, 10.5)

        with self.assertRaises(ParseException):
            FloatField('10')

    def test_encode(self):
        self.assertEqual(FloatField(10.5).json_encode(), '10.5')
        self.assertEqual(FloatField(10L).json_encode(), '10')


class NestedTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(NestedTest, self).__init__(*args, **kwargs)
        self.testObj = NestedObjTest({'id': 1234, 'clave': 1, 'value': 'aValue'})

    def test_init(self):
        self.assertEqual(self.testObj.id.value, 1234)
        self.assertEqual(self.testObj.key.value, 1)    # clave field
        self.assertEqual(self.testObj.value.value, 'aValue')

        with self.assertRaises(ParseException):
            NestedField(10)

        with self.assertRaises(ParseException):
            NestedField(10.5)

        with self.assertRaises(ParseException):
            NestedField("aString")

        with self.assertRaises(ParseException):
            NestedField([])

        with self.assertRaises(AttributeError):
            self.testObj.unknownAttr

        with self.assertRaises(AttributeError):
            NestedField({}).unknownAttr

    def test_encode(self):
        self.assertEqual(NestedField({}).json_encode(), '{}')
        self.assertEqual(json.loads(self.testObj.json_encode()), json.loads('{"id": 1234, "key": 1, "value": "aValue"}'))

class ListTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ListTest, self).__init__(*args, **kwargs)
        self.testObj = ListObjTest([
            {'id': 1234, 'clave': 1, 'value': 'aValue'},
            {'id': 4321, 'clave': 2, 'value': 'anotherValue'}
        ])

    def test_init(self):
        self.assertEqual(self.testObj[0].id.value, 1234)
        self.assertEqual(self.testObj[1].id.value, 4321)
        self.assertEqual(self.testObj[0].key.value, 1)    # clave field
        self.assertEqual(self.testObj[1].key.value, 2)    # clave field
        self.assertEqual(self.testObj[0].value.value, 'aValue')
        self.assertEqual(self.testObj[1].value.value, 'anotherValue')

        with self.assertRaises(ParseException):
            ListObjTest(10)

        with self.assertRaises(ParseException):
            ListObjTest(10.5)

        with self.assertRaises(ParseException):
            ListObjTest("aString")

        with self.assertRaises(ParseException):
            ListObjTest({})

        with self.assertRaises(IndexError):
            self.testObj[2]

        with self.assertRaises(IndexError):
            ListObjTest([])[0]

    def test_slice(self):
        self.assertEqual(len(self.testObj), 2)
        self.assertEqual(len(self.testObj[:1]), 1)
        self.assertEqual(len(self.testObj[1:]), 1)
        self.assertEqual(self.testObj[-1].id.value, 4321)
        self.assertEqual(self.testObj[-1].key.value, 2)    # clave field
        self.assertEqual(self.testObj[-1].value.value, 'anotherValue')

    def test_encode(self):
        self.assertEqual(ListObjTest([]).json_encode(), '[]')
        self.assertEqual(json.loads(self.testObj.json_encode()), json.loads('[{"id": 1234, "key": 1, "value": "aValue"},{"id": 4321, "key": 2, "value": "anotherValue"}]'))

if __name__ == '__main__':
    unittest.main()