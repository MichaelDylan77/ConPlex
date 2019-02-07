# -*- coding: utf-8 -*-

from filelock import FileLock, Timeout
from shutil import rmtree
import PrintTags as pt
from os import path
import json

from .yaml_converter import YAMLConverter


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

    # TODO: Setup lock on project file

    __project_file_path = './.conplex'
    __lock_file_path = './.conplex.lock'

    def __init__(self):

        self.project_data = None
        self.__lock = FileLock(self.__lock_file_path, timeout=1)

        if path.isfile(self.__project_file_path):
            self.__load_project_file()
        else:
            self.__create_project_file()

    def __create_project_file(self):

        """
        Creates a new .conplex file in the current working directory
        """

        project_data = {
            'active': None,
            'modules': []
        }
        try:
            self.__lock.acquire(timeout=2)
            with open(self.__project_file_path, 'w') as project_file:
                json_data = json.dumps(self.project_data, indent=4, sort_keys=True)
                project_file.write(json_data)
        except Timeout as e:
            pt.error(e)
        except IOError as e:
            pt.error(e)
        finally:
            self.__lock.release()
            self.project_data = project_data

    def __load_project_file(self):

        """
        Loads in the project data form the .conplex file in the current
        working directory
        """

        try:
            self.__lock.acquire(timeout=2)
            with open(self.__project_file_path, 'r') as project_file:
                self.project_data = json.load(project_file)
        except Timeout as e:
            pt.error(e)
        except IOError as e:
            pt.error(e)
        finally:
            self.__lock.release()

    def update_project_file(self):

        """
        Writes the contents of the project_data attribute of this class
        to the .conplex file
        """

        try:
            self.__lock.acquire(timeout=2)
            with open(self.__project_file_path, 'w') as project_file:
                json_data = json.dumps(self.project_data, indent=4, sort_keys=True)
                project_file.write(json_data)
        except Timeout as e:
            pt.error(e)
        except IOError as e:
            pt.error(e)
        finally:
            self.__lock.release()

    def set_active_module(self, module_name):

        # TODO: Update project after setting active module

        """
        Sets the current active module. This method does not update
        the .conplex file, so update_project() should be invoked after
        setting the active module

        args:
            module_name: The name of the module that should be activated.
            If module_name is None, the active module will be set to None/null
        """
        if module_name is None:
            self.project_data['active'] = module_name
            return
        for module in self.project_data['modules']:
            if module['module_name'] == module_name:
                self.project_data['active'] = module_name
                return
        raise ModuleNotFoundError('No module named {} found'.format(module_name))

    def create_module(self, options, set_active=False):

        # TODO: Update project after setting active module

        """
        Creates a new module and adds it to the project_data attribute
        of this class. This method does not update the .conplex
        file, so update_project() should be invoked after creating a new
        module

        args:
            options: A dict containing the options for the new module
            set_active: Whether or not this should be set as the active module
        """

        generator = YAMLConverter(options['yaml_path'],
                                  module_name=options['module_name'],
                                  case_correction=options['case_correction'],
                                  silent=True)
        num_classes, num_variables = generator()
        options['num_classes'] = num_classes
        options['num_variables'] = num_variables
        self.project_data['modules'].append(options)
        if set_active:
            try:
                self.set_active_module(options['module_name'])
            except ModuleNotFoundError as e:
                pt.error(e)

    def delete_module(self, module):

        # TODO: Handle errors from rmtree

        rmtree(module['module_name'])
        self.project_data['modules'].remove(module)
        if self.project_data['active'] == module['module_name']:
            self.set_active_module(None)
        self.update_project_file()

    def get_module_by_name(self, name):
        for module in self.project_data['modules']:
            if module['module_name'] == name:
                return module
        return None

    @property
    def modules(self):

        """
        Returns a list of all modules present in this project
        """

        return self.project_data['modules']

    @property
    def active_module(self):

        """
        Returns the active module for this project
        """

        active_module = self.project_data['active']
        if active_module is not None:
            return self.get_module_by_name(active_module)

