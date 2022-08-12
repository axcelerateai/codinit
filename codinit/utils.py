import json
import os
import pickle

# =====================================================================
# File handlers
# =====================================================================

def save_dict_as_json(dic, save_dir, name=None):
    if name is not None:
        save_dir = os.path.join(save_dir, name+'.json')
    with open(save_dir, 'w') as out:
        out.write(json.dumps(dic, separators=(',\n','\t:\t'),
                  sort_keys=True))

def load_dict_from_json(load_from, name=None):
    if name is not None:
        load_from = os.path.join(load_from, name+'.json')
    with open(load_from, 'rb') as f:
        dic = json.load(f)

    return dic

def save_dict_as_pkl(dic, save_dir, name=None):
    if name is not None:
        save_dir = os.path.join(save_dir, name+'.pkl')
    with open(save_dir, 'wb') as out:
        pickle.dump(dic, out, protocol=pickle.HIGHEST_PROTOCOL)

def load_dict_from_pkl(load_from, name=None):
    if name is not None:
        load_from = os.path.join(load_from, name+'.pkl')
    with open(load_from, 'rb') as out:
        dic = pickle.load(out)

    return dic

# ======================================================================
# Parser
# ======================================================================

def get_sl_map(parser):
    """Return a dictionary containing short-long name mapping in parser."""
    sl_map = {}

    # Add arguments with long names defined.
    for key in parser._option_string_actions.keys():
        if key[1] == '-':
            options = parser._option_string_actions[key].option_strings
            if len(options) == 1:   # No short argument.
                sl_map[key[2:]] = key[2:]
            else:
                if options[0][1] == '-':
                    sl_map[key[2:]] = options[1][1:]
                else:
                    sl_map[key[2:]] = options[0][1:]

    # We've now processed all arguments with long names. Now need to process
    # those with only short names specified.
    known_keys = list(sl_map.keys()) + list(sl_map.values())
    for key in parser._option_string_actions.keys():
        if key[1:] not in known_keys and key[2:] not in known_keys:
            sl_map[key[1:]] = key[1:]

    # Arguments left must be the compulsory ones. Now add them
    known_keys = list(sl_map.keys()) + list(sl_map.values())
    for key in vars(parser.parse_args()).keys():
        if key not in known_keys:
            sl_map[key] = key

    return sl_map
