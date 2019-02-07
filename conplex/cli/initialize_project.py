# -*- coding: utf-8 -*-

import PrintTags as pt
from os import getcwd, path
from conplex.core.project_manager import ProjectManager
from .utils import query_yes_no, validate_module_name


class ProjectConstructor(object):

    # TODO: Finish documenting

    def __init__(self, manager: ProjectManager):

        if self.__query_confirmation():

            yaml_path = self.__query_yaml_path()  # Prompt the user for the YAML configuration file path
            yaml_name = yaml_path.split('/')[-1]
            module_name = yaml_name.split('.')[0].replace(' ', '')  # Get the name of the YAML file as a module name
            if validate_module_name(module_name):  # Check if the YAML name is acceptable as a module name
                if not self.__query_use_default_module_name(module_name):  # If the YAML name is acceptable, ask if they want to use it
                    module_name = self.__query_module_name()  # If they don't, ask them for a name
            else:
                module_name = self.__query_module_name()  # If the YAML name is not acceptable, ask for a name
            case_correction = self.__query_use_case_correction()
            set_active = self.__query_set_as_active(module_name)

            module_options = {
                'module_name': module_name,
                'yaml_name': yaml_name,
                'yaml_path': yaml_path,
                'case_correction': case_correction
            }

            manager.create_module(module_options, set_active=set_active)
            manager.update_project_file()

    @staticmethod
    def __query_confirmation():
        working_dir = getcwd()
        question = 'Initialize a new ConPlex module in {}?'.format(working_dir)
        return query_yes_no(question, default=None)

    @staticmethod
    def __query_yaml_path():

        while True:
            yaml_path = input('Please provide the path to your YAML configuration file: ')
            if path.isfile(yaml_path) and yaml_path.endswith('yaml'):
                return yaml_path
            else:
                pt.notice('It seems the path you proved is not a valid YAML file')

    @staticmethod
    def __query_use_default_module_name(default):
        question = 'Do you want to use the name from your YAML file ({}) for this module? '.format(default)
        return query_yes_no(question, default='yes')

    @staticmethod
    def __query_module_name():
        while True:
            module_name = input('Please provide a module name: ')
            if module_name and validate_module_name(module_name):
                return module_name
            else:
                pt.notice('The module name provided is invalid. Please remove any spaces or special characters other than "_" and try again.')

    @staticmethod
    def __query_use_case_correction():
        question = 'Do you want to use automatic case correction for this module?'
        return query_yes_no(question, default='no')

    @staticmethod
    def __query_set_as_active(module_name):
        question = 'Do you want to set "{}" as the active ConPlex configuration?'.format(module_name)
        return query_yes_no(question, default='yes')
