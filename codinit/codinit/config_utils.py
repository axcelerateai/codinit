import importlib
import argparse
import json
import math
import os
import pickle
import subprocess
import types

import codinit.utils as utils


# ======================================================================
# Config
# ======================================================================

def reverse_dict(x):
    """
    Exchanges keys and values in x i.e. x[k] = v ---> x[v] = k.
    Added Because reversed(x) does not work in python 3.7.
    """
    y = {}
    for k,v in x.items():
        y[v] = k
    return y

def load_config(config_file):
    config = {}
    if config_file is not None:
        if config_file.endswith('.py'):
            mod_name = config_file.replace('/', '.').strip('.py')
            config = importlib.import_module(mod_name).config
        elif config_file.endswith('.json'):
            config = utils.load_dict_from_json(args['config_file'])
        else:
            raise ValueError('Invalid type of config file')
    return config

def merge_configs(config, parser, sys_argv):
    """
    Merge a dictionary (config) and arguments in parser.

    Order of priority (in decreasing order):
        1. value supplied through command line
        2. value specified in config
        3. default value in parser

    Args:
        config   : dictionary
        parser   : instance of argparse.ArgumentParser
        sys_argv : list of arguments supplied through command line
    """

    parser_dict = vars(parser.parse_args())
    config_keys = list(config.keys())
    parser_keys = list(parser_dict.keys())

    sl_map = utils.get_sl_map(parser)
    rev_sl_map = reverse_dict(sl_map)
    def other_name(key):
        if key in sl_map:
            return sl_map[key]
        elif key in rev_sl_map:
            return rev_sl_map[key]
        else:
            return key

    merged_config = {}
    for key in config_keys + parser_keys:
        if key in parser_keys:
            # Was argument supplied through command line?
            if key_was_specified(key, other_name(key), sys_argv):
                merged_config[key] = parser_dict[key]
            else:
                # If key is in config, then use value from there.
                if key in config:
                    merged_config[key] = config[key]
                else:
                    merged_config[key] = parser_dict[key]
        elif key in config:
            # If key was only specified in config, use value from there.
            merged_config[key] = config[key]

    return merged_config

def key_was_specified(key1, key2, sys_argv):
    for arg in sys_argv:
        if (arg[0] == '-'
            and (key1 == arg.strip('-') or key2 == arg.strip('-'))):
            return True
    return False
