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

class NoneTest(unittest.TestCase):
    def test_value(self):
        self.assertEqual(TextField(None).value, None)
        self.assertEqual(IntegerField(None).value, None)
        self.assertEqual(FloatField(None).value, None)
        self.assertEqual(NestedField(None).value, {})
        self.assertEqual(len(ListObjTest(None)), 0)

    def test_encode(self):
        self.assertEqual(TextField(None).json_encode(), "null")
        self.assertEqual(IntegerField(None).json_encode(), "null")
        self.assertEqual(FloatField(None).json_encode(), "null")
        self.assertEqual(NestedField(None).json_encode(), "{}")
        self.assertEqual(ListObjTest(None).json_encode(), "[]")

    def test_decode(self):
        t = TextField(None)
        t.json_decode("null")
        self.assertEqual(t.value, None)
        t = IntegerField(None)
        t.json_decode("null")
        self.assertEqual(t.value, None)
        t = FloatField(None)
        t.json_decode("null")
        self.assertEqual(t.value, None)
        t = NestedField(None)
        t.json_decode("null")
        self.assertEqual(t.value, {})
        t = ListObjTest(None)
        t.json_decode("null")
        self.assertEqual(t.value, [])


class TextTest(unittest.TestCase):
    def test_init(self):
        self.assertEqual(TextField('''"aBc"''').value, '''"aBc"''')
        self.assertEqual(TextField("5").value, "5")

        self.assertRaises(ParseException, TextField.__init__, TextField(), 5)
        # with self.assertRaises(ParseException):
        #     TextField(5)

    def test_encode(self):
        self.assertEqual(TextField("aBc").json_encode(), '"aBc"')
        self.assertEqual(TextField("5").json_encode(), '"5"')

        self.assertEqual(TextField(None).json_encode(), 'null')


class IntegerTest(unittest.TestCase):
    def test_init(self):
        self.assertEqual(IntegerField(10).value, 10)
        # self.assertEqual(IntegerField(10L).value, 10)

        self.assertRaises(ParseException, IntegerField.__init__, IntegerField(), '5')
        # with self.assertRaises(ParseException):
        #     IntegerField('5')

        self.assertRaises(ParseException, IntegerField.__init__, IntegerField(), 10.0)
        # with self.assertRaises(ParseException):
        #     IntegerField(10.0)

    def test_encode(self):
        self.assertEqual(IntegerField(10).json_encode(), '10')
        # self.assertEqual(IntegerField(10L).json_encode(), '10')


class FloatTest(unittest.TestCase):
    def test_init(self):
        self.assertEqual(FloatField(10).value, float(10))
        self.assertEqual(FloatField(10.0).value, float(10))
        # self.assertEqual(FloatField(10L).value, float(10))
        self.assertEqual(FloatField(10.5).value, 10.5)

        self.assertRaises(ParseException, FloatField.__init__, FloatField(), '10')
        # with self.assertRaises(ParseException):
        #     FloatField('10')

    def test_encode(self):
        self.assertEqual(FloatField(10.5).json_encode(), '10.5')
        # self.assertEqual(FloatField(10L).json_encode(), '10')


class NestedTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(NestedTest, self).__init__(*args, **kwargs)
        self.testObj = NestedObjTest({'id': 1234, 'clave': 1, 'value': 'aValue'})

    def test_init(self):
        self.assertEqual(self.testObj.id.value, 1234)
        self.assertEqual(self.testObj.key.value, 1)    # clave field
        self.assertEqual(self.testObj.value.value, 'aValue')

        self.assertRaises(ParseException, NestedField.__init__, NestedField(), 10)
        # with self.assertRaises(ParseException):
        #     NestedField(10)

        self.assertRaises(ParseException, NestedField.__init__, NestedField(), 10.5)
        # with self.assertRaises(ParseException):
        #     NestedField(10.5)

        self.assertRaises(ParseException, NestedField.__init__, NestedField(), "aString")
        # with self.assertRaises(ParseException):
        #     NestedField("aString")

        self.assertRaises(ParseException, NestedField.__init__, NestedField(), [])
        # with self.assertRaises(ParseException):
        #     NestedField([])

        self.assertRaises(AttributeError, NestedField.__getattr__, self.testObj, 'unknownAttr')
        # with self.assertRaises(AttributeError):
        #     self.testObj.unknownAttr

        self.assertRaises(AttributeError, NestedField.__getattr__, NestedField({}), 'unknownAttr')
        # with self.assertRaises(AttributeError):
        #     NestedField({}).unknownAttr

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

        self.assertRaises(ParseException, ListField.__init__, ListObjTest(), 10)
        # with self.assertRaises(ParseException):
        #     ListObjTest(10)

        self.assertRaises(ParseException, ListField.__init__, ListObjTest(), 10.5)
        # with self.assertRaises(ParseException):
        #     ListObjTest(10.5)

        self.assertRaises(ParseException, ListField.__init__, ListObjTest(), "aString")
        # with self.assertRaises(ParseException):
        #     ListObjTest("aString")

        self.assertRaises(ParseException, ListField.__init__, ListObjTest(), {})
        # with self.assertRaises(ParseException):
        #     ListObjTest({})

        self.assertRaises(IndexError, ListField.__getitem__, self.testObj, 2)
        # with self.assertRaises(IndexError):
        #     self.testObj[2]

        self.assertRaises(IndexError, ListField.__getitem__, ListObjTest([]), 0)
        # with self.assertRaises(IndexError):
        #     ListObjTest([])[0]

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