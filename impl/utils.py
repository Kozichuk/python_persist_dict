import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)


def get_module_logger(resource_name):
    module_logging = logging.getLogger(resource_name)
    module_logging.setLevel(logging.INFO)
    module_logging.addHandler(sh)
    return logging.getLogger(resource_name)
