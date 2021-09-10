import argparse

from codinit import initialize
import codinit.logger as logger

def test_setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arg_1', type=str)
    parser.add_argument('--arg_2', type=int, default=1)
    parser.add_argument('--arg_3', '-a3', type=float, default=0.21)
    parser.add_argument('--arg_4', '-a4', type=float, default=0.)
    parser.add_argument('--arg_5', '-a5', action='store_true')

    config, _ = initialize(parser)

    # Can't really test with pytest, so just print
    if __name__=='__main__':
        print(config)
        logger.record('ABC/abc', 10)
        logger.record('ABC/def', 20)
        logger.record('DEF/abc', 11)
        logger.record('DEF/def', 21)
        logger.dump(step=0)


if __name__=='__main__':
    test_setup()
