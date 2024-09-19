from setuptools import find_packages, setup

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='microSecFixer',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires
)