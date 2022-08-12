from setuptools import find_packages, setup

setup(
    name='codinit',
    packages=find_packages(include=['codinit']),
    version='0.1.0',
    description='Library to take care of initiaisation etc.',
    author='shehryar',
    license='MIT',
    install_requires=['numpy','pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['wandb','pytest==4.4.1'],
    test_suite='tests',
)
