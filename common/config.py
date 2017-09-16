import collections
import copy

import os

_config = {}

_local = {
    'HOME': 'D:/srkim/python/project/dw',
    'mongo': {
        'host': 'localhost',
        'port': 27017
    },
    'log': ''
}

_stage = {
    'HOME': '/dw',
    'db': {}
}

_product = {
    'HOME': '/dw',
    'db': {}
}


def _deep_update(s, d):
    for key, value in d.items():
        if isinstance(value, collections.Mapping):
            tmp = _deep_update(s.get(key, {}), value)
            s[key] = tmp
        else:
            s[key] = value
    return s


def get_config(environment='local', key=None):
    global _config

    if 'DW_ENV' not in os.environ:
        environment = environment or 'local'
    else:
        environment = os.environ['DW_ENV']
    if 'local' not in _config:
        _config['local'] = _local

    if 'stage' not in _config:
        _config['stage'] = copy.deepcopy(_config['local'])
        _deep_update(_config['stage'], _stage)

    if 'product' not in _config:
        _config['product'] = copy.deepcopy(_config['local'])
        _deep_update(_config['product'], _product)

    if key is None:
        return _config[environment]

    return _config[environment][key]

