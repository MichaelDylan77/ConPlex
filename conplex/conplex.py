# -*- coding: utf-8 -*-

"""
This document acts as the entry point to the ConPlex application.
When executed from the command line, main() will be invoked. When
imported into a python file, run() is used.
"""

from sys import argv
from argparse import ArgumentParser
from .generator import Generator
from .cli import CLI


def run(yaml_path, output_dir=None, module_name=None, case_correction=False, verbose=False, silent=False):
    Generator(yaml_path, output_dir=output_dir, module_name=module_name, case_correction=case_correction, verbose=verbose, silent=silent)()


def main():

    CLI()()

    #if len(argv) == 2:
    #    if 'init' in argv:
    #        from conplex.cli.initialize_project import InitializeProject
    #        args = InitializeProject()



    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml_path', help='The path to the YAML configuration file to be mirrored')
    parser.add_argument('--output_dir', help='The directory the newly generated Python module should be placed in', default=None)
    parser.add_argument('--module_name', help='The name of the newly generated Python module. This will default to the YAML file name', default=None)
    parser.add_argument('-C', '--case_correction', help='(experimental) Whether or not variable, attribute, and class names should be altered to fit standard Python conventions', action='store_true', default=False)
    parser.add_argument('-V', '--verbose', help='Whether or not to print additional information, including error descriptions', action='store_true', default=False)
    parser.add_argument('-S', '--silent', help='Silences all prints and outputs. This is useful when running ConPlex from inside a script or application to update the config at runtime', action='store_true', default=False)
    args = parser.parse_args()

    if args.yaml_path is None:
        from sys import exit
        if not args.silent:
            import PrintTags as pt
            pt.notice('Please specify the path to a YAML configuration file with the --yaml_file argument')
        exit()

    Generator(args.yaml_path, output_dir=args.output_dir, module_name=args.module_name, case_correction=args.case_correction, verbose=args.verbose, silent=args.silent)()

    """
