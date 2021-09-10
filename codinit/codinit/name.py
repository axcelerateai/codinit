import argparse
import json
import math
import os
import pickle
import subprocess
import types

import codinit.utils as utils

# ======================================================================
# Name
# ======================================================================

def get_name(
        parser,
        default_config,
        actual_config,
        append_seed=True,
        append_sid=False,
        ignore_keys=None,
        path_keys=None
    ):
    """
    Return a name for the current experiment based on the parameters passed.
    The name is constructed by concatenating the names and values of the
    parameters that have a non-default value. The default value is specified
    in the default_config dictionary

    Args:
        parser          : an instance of ArgumentParser
        default_config  : the default config
        actual_config   : the actual config that is being used
    """

    if (name := actual_config.get('name', None)) is None:
        name = concat_nondefault_arguments(
                parser,
                ignore_keys=ignore_keys,
                path_keys=path_keys,
                default_config=default_config,
                actual_config=actual_config
        )

    # Append seed and system id regardless of whether the name was
    # passed in or not
    if append_seed:
        name = name + '_s_' + str(actual_config['seed'])
    if append_sid:
        name = name + '_sid_' + get_sid()

    # Delete trailing underscore
    name = name[1:] if name[0] == '_' else name

    return name

def concat_nondefault_arguments(
        parser,
        ignore_keys=None,
        path_keys=None,
        default_config=None,
        actual_config=None
    ):
    """
    Given an instance of argparse.ArgumentParser or an alternative default
    configuration dictionary , return a concatenation of the names and values
    of only those arguments that do not have the default value (i.e.
    alternative values were specified via command line).
    So if you run
        python file.py -abc 123 -def 456
    this function will return abc_123_def_456. (In case the value passed
    for 'abc' or 'def' is the same as the default value, they will be
    ignored)
    If a shorter version of the argument name is specified, it will be
    preferred over the longer version.
    Arguments are sorted alphabetically.

    Args:
        parser         : instance of argparse.ArgumentParser
        ignore_keys    : list arguments, whose values should be ignored
        path_keys      : list arguments that expect paths. The values of
                         these will be split at '/' and only the last
                         substring will be used
        default_config : a dictionary. Contains alternative default
                         values
    Return
        name: a string. The concatenation of non-default args
    """

    if ignore_keys is None:
        ignore_keys = []
    if path_keys is None:
        path_keys = []

    sl_map = utils.get_sl_map(parser)

    def get_default(key):
        if default_config is not None and key in default_config:
            return default_config[key]
        return parser.get_default(key)

    # Determine save dir based on non-default arguments if no
    # save_dir is provided.
    concat = ''
    for key, value in sorted(vars(parser.parse_args()).items()):
        if actual_config is not None:
            value = actual_config[key]

        # Skip these arguments.
        if key in ignore_keys:
            continue

        if type(value) == list:
            b = False
            if get_default(key) is None or len(value) != len(get_default(key)):
                b = True
            else:
                for v, p in zip(value, get_default(key)):
                    if v != p:
                        b = True
                        break
            if b:
                concat += '%s_' % sl_map[key]
                for v in value:
                    if type(v) not in [bool, int] and hasattr(v, '__float__'):
                        if v == 0:
                            valstr = 0
                        else:
                            valstr = round(
                                    v,
                                    4-int(math.floor(math.log10(abs(v))))-1
                            )
                    else:
                        valstr = v
                    concat += '%s_' % str(valstr)

        # Add key, value to concat.
        elif value != get_default(key):
            # For paths.
            if value is not None and key in path_keys:
                value = value.split('/')[-1]

            if type(value) not in [bool, int] and hasattr(value, '__float__'):
                if value == 0:
                    valstr = 0
                else:
                    valstr = round(
                            value,
                            4-int(math.floor(math.log10(abs(value))))-1
                    )
            else:
                valstr = value
            concat += '%s_%s_' % (sl_map[key], valstr)

    if len(concat) > 0:
        # Remove extra underscore at the end.
        concat = concat[:-1]

    return concat

def get_sid():
    sid = _get_sid('who_am_i')
    return sid

def _get_sid(cm):
    try:
        sid = subprocess.check_output(
                ['/bin/bash', '-i', '-c', cm],
                timeout=2
            ).decode('utf-8').split('\n')[-2]
        sid = sid.lower()
        if 'system' in sid:
            sid = sid.strip('system')
        else:
            sid = -1
    except:
        sid = -1
    return str(sid)


