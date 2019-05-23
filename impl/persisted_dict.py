import os
import pickle

from impl import get_module_logger


class PersistedDict(dict):
    __persist_dir = None
    __keys = set()
    __log = None

    def __init__(self, persist_dir: str, **kwargs):
        super().__init__(**kwargs)
        self.__persist_dir = persist_dir

        self.__log = get_module_logger('persisted_dict')
        # create dir
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)
            self.__log.debug("Directory {} created".format(self.__persist_dir))
        else:
            self.__log.warn("Directory {} already exists".format(self.__persist_dir))

    def __getitem__(self, key):
        if key not in self.__keys and not self.__persisted_object_exists(key):
            raise KeyError(key)
        return self.__read(self.__to_path(key))

    def __setitem__(self, key, value):
        self.__validate_key(key)
        if key in self.__keys and self.__persisted_object_exists(key):
            self.__log.warn("Key {} already exists. Rewriting.".format(key))
        self.__keys.add(key)
        self.__write(self.__to_path(key), value)

    def __delitem__(self, key):
        if key in self.__keys and self.__persisted_object_exists(key):
            self.__log.debug("Deleting key {}.".format(key))
            self.__keys.remove(key)
            self.__log.debug("Value for key {} successfully deleted.".format(key))
            try:
                os.remove(self.__to_path(key))
            except FileNotFoundError:
                self.__log.error("Element with key {} didn't exist in storage".format(key))
        else:
            self.__log.error("Key {} not exists".format(key))
            raise KeyError("Key {} not exists".format(key))

    def keys(self):
        return self.__keys

    def clear(self):
        for key in self.keys():
            try:
                os.remove(self.__to_path(key))
            except FileNotFoundError:
                self.__log.error("Element with key {} didn't exist in storage".format(key))
        self.__keys.clear()
        # По идее нужно грохать папку если она не пуста

    def __persisted_object_exists(self, key):
        return True if os.path.isfile(self.__to_path(str(key))) else False

    @staticmethod
    def __write(key, value):
        with open(key, 'wb') as target:
            pickle.dump(value, target)

    @staticmethod
    def __read(key):
        with open(key, 'rb') as saved_data:
            return pickle.load(saved_data)

    def __to_path(self, key):
        return os.path.join(self.__persist_dir, str(key))

    def __validate_key(self, key):
        if not isinstance(key, (int, float, str)):
            raise KeyError("Key must be string or number.")
        if type(key) is str:
            if len(key.strip()) is 0:
                raise KeyError("String key must be not empty")
