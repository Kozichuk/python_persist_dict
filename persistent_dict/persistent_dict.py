import os
import shelve
import shutil

from persistent_dict import get_module_logger


class PersistentDictContainer:

    def __init__(self, storage_dir, storage_files_mask, debug):
        self.storage_dir = storage_dir
        self.storage_files_mask = storage_files_mask
        self.debug = debug

    @staticmethod
    def to_dictionary(dict_obj):
        if not isinstance(dict_obj, PersistentDictContainer):
            raise ValueError
        return PersistentDict(dict_obj.storage_dir, dict_obj.storage_files_mask, dict_obj.debug)


class SelfMarker:
    """
    Dummy marker
    Used when an instance is added to itself.
    """
    pass


class PersistentDict(dict):
    __storage_dir = None
    __keys = set()
    __log = None

    def __init__(self, storage_dir: str, storage_files_mask='storage', debug=False):
        super().__init__()
        self.__storage_dir = storage_dir
        self.__storage_files_mask = storage_files_mask
        self.__debug = debug

        if not os.path.isdir(self.__storage_dir):
            os.mkdir(self.__storage_dir)

        self.__storage = os.path.join(self.__storage_dir, self.__storage_files_mask)
        self.__log = get_module_logger('persisted_dict', self.__debug)

    def __getitem__(self, key):
        prepared_key = self.__to_shelved_key(key)

        with shelve.open(self.__storage) as storage:
            if prepared_key not in storage.keys():
                raise KeyError()
            unpickled_value = storage.get(prepared_key)
            if type(unpickled_value) is SelfMarker:
                return self
            elif type(unpickled_value) is PersistentDictContainer:
                return unpickled_value.to_dictionary(unpickled_value)
            else:
                return unpickled_value

    def __setitem__(self, key, value):
        self.__validate_key(key)
        prepared_key = self.__to_shelved_key(key)

        if isinstance(value, PersistentDict):
            value = SelfMarker() if value == self else self.to_container(value)

        with shelve.open(self.__storage) as storage:
            storage[prepared_key] = value
        self.__keys.add(key)

    def __delitem__(self, key):
        with shelve.open(self.__storage) as storage:
            if key not in storage.keys():
                raise KeyError()
            storage.pop(key)
        self.__keys.remove(key)

    def __eq__(self, other):
        if not isinstance(other, PersistentDict):
            return False
        return self.storage_dir == other.storage_dir and self.keys() == other.keys()

    def keys(self):
        with shelve.open(self.__storage) as storage:
            tmp = [self.__from_shelve_key(k) for k in list(storage.keys())]
            return tmp

    def clear(self):
        with shelve.open(self.__storage) as storage:
            storage.clear()
        shutil.rmtree(self.__storage_dir)

    # workaround key limitations of shelve
    def __to_shelved_key(self, key):
        self.__log.debug('Origin key {}'.format(key))
        if type(key) is int:
            return "int_{}".format(key)
        elif type(key) is float:
            return "float_{}".format(key)
        else:
            return key

    def __from_shelve_key(self, shelved_key: str):
        self.__log.debug('Shelving key {}'.format(shelved_key))
        if shelved_key.startswith('int_'):
            return int(shelved_key[4:])
        elif shelved_key.startswith('float_'):
            return float(shelved_key[6:])
        else:
            return shelved_key

    @property
    def storage_dir(self):
        return self.__storage_dir

    @property
    def storage_files_mask(self):
        return self.__storage_files_mask

    def get_debug(self):
        return self.__debug

    def __validate_key(self, key):
        if not isinstance(key, (int, float, str)) or isinstance(key, (bool)):
            raise KeyError("Key must be string or number.")
        if type(key) is str:
            if len(key.strip()) is 0:
                raise KeyError("String key must be not empty")

    def to_container(self, object_dict) -> PersistentDictContainer:
        if not isinstance(object_dict, PersistentDict):
            raise ValueError
        return PersistentDictContainer(object_dict.storage_dir, object_dict.storage_files_mask, object_dict.get_debug())
