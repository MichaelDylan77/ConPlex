# -*- coding: utf-8 -*-

"""
This document acts as the entry point to the ConPlex application.
When executed from the command line, main() will be invoked. When
imported into a python file, run() is used.
"""

from conplex.core import YAMLConverter
from .cli import CLI


def run(yaml_path, output_dir=None, module_name=None, case_correction=False, verbose=False, silent=False):
    YAMLConverter(yaml_path, output_dir=output_dir, module_name=module_name, case_correction=case_correction, verbose=verbose, silent=silent)()


def main():

    CLI()()
