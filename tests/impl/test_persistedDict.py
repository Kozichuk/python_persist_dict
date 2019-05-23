import os
import sys
import unittest

from parameterized import parameterized

from impl.persisted_dict import PersistedDict


class TestPersistedDictInitDict(unittest.TestCase):
    def setUp(self):
        self.myDict = None

    def test_init_storage_from_accessible_folder_success(self):
        # given
        test_path = 'test_persist'
        # when
        self.myDict = PersistedDict(test_path)
        # then
        self.assertTrue(os.path.isdir(self.myDict.storage_dir))
        # tearDown

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_init_storage_from_non_accessible_folder_raised_exception(self):
        # only on windows
        # given
        non_accessible_path = 'C:/Windows/tmp'
        # when
        with self.assertRaises(PermissionError):
            self.myDict = PersistedDict(non_accessible_path)
        # then
        # catch exception

    def tearDown(self):
        pass
        # self.myDict.clear()


class DummyObject(object):
    def __init__(self):
        self.field = 5

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.field == other.field
        return False


class TestPersistedDictBasicOperations(unittest.TestCase):

    def setUp(self):
        self.persist_dir = 'persist'
        self.myDict = PersistedDict(self.persist_dir)

    """
    __setitem__
    """

    @parameterized.expand([
        ["a"],
        ["aasvasdasd"],
        [1],
        [1.0],
        [.1],
        [99999],
        [-1]
    ])
    def test_add_new_pair_with_valid_key_success(self, key):
        self.myDict[key] = 123
        self.assertTrue(key in self.myDict.keys())

    @parameterized.expand([
        [""],
        ["   "],
        [None],
        [set()],
        [{}],
        [[]],
        [True],
        [False],
        [DummyObject()],
    ])
    def test_add_new_key_raises_exception_on_invalid_key(self, key):
        with self.assertRaises(KeyError):
            self.myDict[key] = 123

    @parameterized.expand([
        [1],
        [999],
        [-999],
        [-1],
        [0.1],
        [None],
        [True],
        [False],
        [set()],
        [{1, 2, 3}],
        [{}],
        [{1: [1, 2, 3]}],
        [[1, 2, 3]]
    ])
    def test_add_new_pair_with_valid_value_success(self, value):
        # given
        key = "test_key"
        # when
        self.myDict[key] = value
        # then
        self.assertEqual(self.myDict[key], value)
        # assert equals for pickled file and value

    def test_add_new_pair_with_custom_class_as_value_success(self):
        # given
        dummy_object = DummyObject()
        key = 'test_key'
        # when
        self.myDict[key] = dummy_object
        # then
        self.assertEqual(self.myDict[key], dummy_object)

    def test_add_new_pair_with_invalid_value_raises_exception(self):
        # Можем положить любой объект, как будто ограничений нет
        self.assertTrue(True)

    """
    __getitem__ tests
    """

    def test_get_value_from_dictionary_if_key_exists(self):
        # given
        key = 'test_key'
        value = 'test_value'
        # when
        self.myDict[key] = value
        # then
        self.assertEqual(self.myDict[key], value)

    """
    __delitem__
    """

    def test_del_pair_if_pair_exists(self):
        # given
        key = 'test_key'
        value = 'test_value'
        self.myDict[key] = value
        # when
        del self.myDict[key]
        # then
        self.assertFalse(os.path.isfile(os.path.join(self.persist_dir, key)))

    def test_del_pair_if_key_non_exists(self):
        # given
        non_exist_key = 'non_exist_key'
        # then
        with self.assertRaises(KeyError):
            del self.myDict[non_exist_key]

    """
    keys()
    """

    def test_after_adding_pairs_keys_are_not_empty_and_containing_expected_keys(self):
        # given
        key_1 = 'test_key_1'
        key_2 = 'test_key_2'
        value = 'test_value'
        # when
        self.myDict[key_1] = value
        self.myDict[key_2] = value
        # then
        self.assertIn(key_1, self.myDict.keys())
        self.assertIn(key_2, self.myDict.keys())

    def tearDown(self):
        self.myDict.clear()
