**Usage**

```python
import argparse
import wandb

from codinit import initialize, logger

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg_1', type=str)
    parser.add_argument('--arg_2', type=int, default=1)
    parser.add_argument('--arg_3', '-a3', type=float, default=0.21)
    parser.add_argument('--arg_4', '-a4', type=float, default=0.)
    parser.add_argument('--arg_5', '-a5', action='store_true')

    initialize(parser)

    # Print config
    print(wandb.config)

    # Log
    logger.record('ABC/abc', 10)
    logger.record('ABC/def', 20)
    logger.record('DEF/abc', 11)
    logger.record('DEF/def', 21)
    logger.dump(step=0)
```

To install:
```shell
git clone https://github.com/shehryar-malik/codinit
cd codinit
pip install -e codinit
```
