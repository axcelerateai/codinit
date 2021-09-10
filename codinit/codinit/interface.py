import sys
import random

import codinit.name as name
import codinit.config_utils as config_utils
import codinit.wandb_utils as wandb_utils
import codinit.logger as logger
import codinit.utils as utils

try:
    import wandb
except:
    wandb = None


def set_seeds(seed):
    random.seed(seed)

    try:
        import numpy as np
        np.random.seed(seed)
    except:
        pass

    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except:
        pass

    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    except:
        pass


def initialize(
        parser,
        set_seed=True,
        append_seed=True,
        append_sid=False,
        ignore_keys=None,
        path_keys=None,
        wandb_kwargs=None,
        configure_logger=True
    ):
    """Do the following:
        1. Merge configs
        2. Get name
        3. Setup W&B

    Reserved keywords:
        - name: default name to use
        - project: W&B project
        - group: W&B group
        - seed: seed to set
    """
    if wandb_kwargs is None:
        wandb_kwargs = {}

    # Configs
    args = vars(parser.parse_args())
    default_config = config_utils.load_config(args.get('config_file', None))
    config = config_utils.merge_configs(default_config, parser, sys.argv[1:])

    # Choose seed
    if set_seed:
        if config.get('seed', None) is None:
            config['seed'] = random.randint(0,100)
        set_seeds(config['seed'])

    # Get name by concatenating arguments with non-default values.
    config['name'] = name.get_name(
            parser,
            default_config,
            config,
            append_seed=append_seed,
            append_sid=append_sid,
            ignore_keys=ignore_keys,
            path_keys=path_keys
    )

    if wandb is None:
        # Forget setting up W&B - just return
        if configure_logger:
            logger.configure(None, format_strings=['stdout'])
        return config, logger

    # Setup W&B
    wandb.init(
            project=config.get('project', None),
            name=config.get('name', None),
            group=config.get('group', None),
            config=config,
            **wandb_kwargs
    )
    wandb.config.save_dir = wandb.run.dir
    config = wandb.config

    # Print
    print(logger.colorize('Configured folder %s for saving' % config.save_dir,
          color='green', bold=True))
    print(logger.colorize('Name: %s' % config.name, color='green', bold=True))

    # Save config
    utils.save_dict_as_json(config.as_dict(), config.save_dir, 'config')

    # Setup logger
    if configure_logger:
        logger.configure(config.save_dir, format_strings=['stdout','wandb'])

    return config, logger
