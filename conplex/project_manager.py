# -*- coding: utf-8 -*-

from os import path, listdir, mkdir
import PrintTags as pt
import json

from .generator import Generator


def singleton(cls):
    obj = cls()
    # Always return the same object
    cls.__new__ = staticmethod(lambda cls: obj)
    # Disable __init__
    try:
        del cls.__init__
    except AttributeError:
        pass
    return cls


class ProjectNotFoundError(Exception):
    pass


@singleton
class ProjectManager(object):

    """
    Manages and creates ConPlex projects and their .conplex file
    """

    # TODO: Setup locking on project file

    __project_path = './.conplex'

    def __init__(self):

        self.project_data = None

        if path.isfile(self.__project_path):
            self.__load_project_data()
        else:
            self.__create_project_data()

    def __create_project_data(self):

        """
        Creates a new .conplex file in the current working directory
        """

        project_data = {
            'active': None,
            'modules': []
        }
        try:
            with open(self.__project_path, 'w+') as project_file:
                json_data = json.dumps(project_data, indent=4, sort_keys=True)
                project_file.write(json_data)
        except IOError as e:
            pt.error(e)
        finally:
            self.project_data = project_data

    def __load_project_data(self):

        """
        Loads in the project data form the .conplex file in the current
        working directory
        """

        try:
            with open(self.__project_path, 'r') as project_file:
                self.project_data = json.load(project_file)
        except IOError as e:
            pt.error(e)

    def set_active_module(self, module_name):

        """
        Sets the current active module. This method does not update
        the .conplex file, so update_project() should be invoked after
        setting the active module

        args:
            module_name: The name of the module that should be activated
        """

        for module in self.project_data['modules']:
            if module['name'] == module_name:
                self.project_data['active'] = module_name
                return
        raise ModuleNotFoundError('No module named {} found'.format(module_name))

    def update_project(self):

        """
        Writes the contents of the project_data attribute of this class
        to the .conplex file
        """

        try:
            with open(self.__project_path, 'w') as project_file:
                json_data = json.dumps(self.project_data, indent=4, sort_keys=True)
                project_file.write(json_data)
        except OSError as e:
            pt.error(e)

    def create_module(self, options, set_active=False):

        """
        Creates a new module and adds it to the project_data attribute
        of this class. This method does not update the .conplex
        file, so update_project() should be invoked after creating a new
        module

        args:
            options: A dict containing the options for the new module
            set_active: Whether or not this should be set as the active module
        """

        yaml_path = options['yaml_path']
        generator = Generator(options['yaml_path'],
                              module_name=options['name'],
                              case_correction=options['case_correction'],
                              silent=True)
        num_classes, num_variables = generator()
        options['num_classes'] = num_classes
        options['num_variables'] = num_variables
        self.project_data['modules'].append(options)
        if set_active:
            try:
                self.set_active_module(options['name'])
            except ModuleNotFoundError as e:
                pt.error(e)

    def list_modules(self):

        """
        Returns a list of all modules present in this project
        """

        return self.project_data['modules']

    def get_module_by_name(self, name):
        for module in self.project_data['modules']:
            if module['name'] == name:
                return module
        return None

    def active_module(self):

        """
        Returns the active module for this project
        """

        name = self.project_data['active']
        if name is not None:
            return self.get_module_by_name(name)

