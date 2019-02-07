# -*- coding: utf-8 -*-

import PrintTags as pt
from conplex.core.project_manager import ProjectManager


class DeleteProject(object):

    # TODO: Finish documenting
    # TODO: Don't need a class for this. Should be a function

    def __init__(self, manager: ProjectManager):

        # Get a list of the existing modules
        modules = manager.modules
        # Display a numbered list of modules in the console
        self.__print_modules(modules)
        while True:
            # Prompt the user to provide the number of the module they want to remove
            module_num = input('Please enter the number of the module you would like to delete: ')
            # Convert response into an integer
            try:
                module_num = int(module_num)
            except ValueError:
                pt.notice(f'"{module_num}" is not a valid module number')
            else:

                if module_num and module_num <= len(modules):
                    module = modules[module_num - 1]
                    manager.delete_module(module)
                    break
                else:
                    pt.notice(f'"{module_num}" is not a valid module number')

    @staticmethod
    def __print_modules(modules):
        print('\n')
        for i, module in enumerate(modules, 1):
            pt.green('{}. {} | {}'.format(i, module['module_name'], module['yaml_path']))
        print('\n')



