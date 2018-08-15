import io, os, sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

class Commands(Command):