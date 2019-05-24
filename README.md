Persisted Dictionary
====

[![PyPi Version][pypi-image]][pypi-url]


Dictionary implementation with saving values into files. 
Based on shelve lib.

Supported operations
--
- get value by key
- set value by key
    - if key exists - rewrite value
- delete value by key
- clear dictionary 

<!-- Markdown link & img dfn's -->
[pypi-image]: https://img.shields.io/badge/PyPi-0.0.1-green.svg
[pypi-url]: https://test.pypi.org/project/persistent-dictionary/

Install
--
Using pip 

    pip install -i https://test.pypi.org/simple/ persistent-dictionary
    
Using setup.py
    
    # clone repo
    # cd into repo dir
    python setup.py install
    

Examples
-- 
    from persistent_dict.persistent_dict import PersistentDict
    
    path_to_storage = 'persistent_storage'
    test_dict = PersistentDict(path_to_storage)
    # created dir with storages
    
    # set operations
    test_dict[123] = 123
    test_dict['123'] = 321
    
    # get operations
    print(test_dict[123])
    # 123
    print(test_dict['123'])
    # 321
    
    # get all keys
    print (test_dict.keys())
    # [123, '123']
    
    # delete by key
    del test_dict[123]
    
