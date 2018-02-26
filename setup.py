from os.path import join as path_join, dirname
from setuptools import setup, find_packages

README_FILE_NAME = path_join(dirname(__file__), 'README.md')

setup(
    name='sensor-simulation',
    version='0.1',
    description=("Simulates data travel times in a railway network."),
    long_description=open(README_FILE_NAME).read(),
    packages=find_packages(),
    install_requires=[
        'pygtfs',
        'coverage',
    ]
)
