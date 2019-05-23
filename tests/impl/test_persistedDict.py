import os
import sys
import unittest

from parameterized import parameterized

from impl.persisted_dict import PersistedDict


class TestPersistedDictInitDict(unittest.TestCase):
    def setUp(self):
        self.test_dict = None

    def test_init_storage_from_accessible_folder_success(self):
        # given
        test_path = 'test_persist'
        # when
        self.test_dict = PersistedDict(test_path)
        # then
        self.assertTrue(os.path.isdir(self.test_dict.storage_dir))
        # tearDown
        self.test_dict.clear()

    def test_recover_from_existing_storage(self):
        # given
        key_1 = 'key_1'
        value_1 = 'value_1'
        # and
        test_path = 'test_persist'
        self.test_dict = PersistedDict(test_path)
        # and
        self.test_dict[key_1] = value_1
        # when
        self.test_dict = PersistedDict(test_path)
        # then
        self.assertIn(key_1, self.test_dict.keys())
        # tesrDown
        self.test_dict.clear()

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_init_storage_from_non_accessible_folder_raised_exception(self):
        # only on windows
        # given
        non_accessible_path = 'C:/Windows/tmp'
        # when
        with self.assertRaises(PermissionError):
            self.test_dict = PersistedDict(non_accessible_path)
        # then
        # catch exception


class DummyObject(object):
    def __init__(self):
        self.field = 5

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.field == other.field
        return False


class TestPersistedDictBasicOperations(unittest.TestCase):

    def setUp(self):
        self.persist_dir = 'test_persist'
        self.test_dict = PersistedDict(self.persist_dir)

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
        self.test_dict[key] = 123
        self.assertTrue(key in self.test_dict.keys())

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
            self.test_dict[key] = 123

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
        self.test_dict[key] = value
        # then
        self.assertEqual(self.test_dict[key], value)
        # assert equals for pickled file and value

    def test_add_new_pair_with_custom_class_as_value_success(self):
        # given
        dummy_object = DummyObject()
        key = 'test_key'
        # when
        self.test_dict[key] = dummy_object
        # then
        self.assertEqual(self.test_dict[key], dummy_object)

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
        self.test_dict[key] = value
        # then
        self.assertEqual(self.test_dict[key], value)

    """
    __delitem__
    """

    def test_del_pair_if_pair_exists(self):
        # given
        key = 'test_key'
        value = 'test_value'
        self.test_dict[key] = value
        # when
        del self.test_dict[key]
        # then
        self.assertFalse(os.path.isfile(os.path.join(self.persist_dir, key)))

    def test_del_pair_if_key_non_exists(self):
        # given
        non_exist_key = 'non_exist_key'
        # then
        with self.assertRaises(KeyError):
            del self.test_dict[non_exist_key]

    """
    keys()
    """

    def test_after_adding_pairs_keys_are_not_empty_and_containing_expected_keys(self):
        # given
        key_1 = 'test_key_1'
        key_2 = 'test_key_2'
        value = 'test_value'
        # when
        self.test_dict[key_1] = value
        self.test_dict[key_2] = value
        # then
        self.assertIn(key_1, self.test_dict.keys())
        self.assertIn(key_2, self.test_dict.keys())

    """
    specific cases
    1. adding instance of PersistentDict to itself
    2. adding another instances of PersistentDict to current dict
    """

    def test_add_self_instance_to_dictionary_as_value(self):
        # given
        self_key = 'instance_of_self'
        key_1 = 'key_1'
        key_2 = 'key_2'
        key_3 = 'new_key'

        value_1 = 'value_1'
        value_2 = 'value_2'
        value_3 = 'value_3'

        self.test_dict[key_1] = value_1
        self.test_dict[key_2] = value_2
        # when
        self.test_dict[self_key] = self.test_dict
        # then
        unpickled_dict: PersistedDict = self.test_dict[self_key]
        self.test_dict[key_3] = value_3
        # and
        self.assertIn(key_1, unpickled_dict.keys())
        self.assertIn(key_2, unpickled_dict.keys())
        # and
        self.assertIn(key_3, unpickled_dict.keys())
        self.assertIn(key_3, self.test_dict.keys())

    def test_add_persistent_dictionary_to_dictionary_as_value_with_another_persist_dir(self):
        # given
        dict_2_key = "dict_2_key"
        dict_2_persist_dir = "persist_2"
        dict_2_persist_storages_file_mask = "storage_2"
        # and
        key_1_in_dict_2 = "key_1"
        key_2_in_dict_2 = "key_2"

        value_1_in_dict_2 = "value_1"
        value_2_in_dict_2 = "value_2"
        # and
        dict_2 = PersistedDict(dict_2_persist_dir)
        dict_2[key_1_in_dict_2] = value_1_in_dict_2
        dict_2[key_2_in_dict_2] = value_2_in_dict_2
        # when
        self.test_dict[dict_2_key] = dict_2
        unpickled_dict = self.test_dict[dict_2_key]
        # then
        self.assertIn(key_1_in_dict_2, unpickled_dict.keys())
        self.assertIn(key_2_in_dict_2, unpickled_dict.keys())
        # teardown
        unpickled_dict.clear()


    def tearDown(self):
        self.test_dict.clear()
