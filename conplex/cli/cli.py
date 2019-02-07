# -*- coding: utf-8 -*-

import PrintTags as pt
from argparse import ArgumentParser
from conplex.core.project_manager import ProjectManager


class Arguments:

    init: str = 'init'
    list: str = 'list'
    active: str = 'active'
    update: str = 'update'
    delete: str = 'delete'


class CLI(object):

    def __init__(self):

        self.__manager = ProjectManager()
        self.__parser = ArgumentParser()
        self.__add_arguments()
        self.__args = self.__parser.parse_args()

    def __call__(self):
        self.__dispatch()

    def __add_arguments(self):
        self.__parser.add_argument('selector')

    def __dispatch(self):

        args = self.__args

        if args.selector == Arguments.init:
            self.__initialize()
        elif args.selector == Arguments.list:
            self.__list()
        elif args.selector == Arguments.active:
            self.__active()
        elif args.selector == Arguments.delete:
            self.__delete()

    def __initialize(self):

        # TODO: Finish print

        from .initialize_project import ProjectConstructor
        ProjectConstructor(self.__manager)
        pt.success('')

    def __list(self):

        modules = self.__manager.modules
        if not len(modules):
            pt.info('There are no ConPlex configurations in this project')
            return
        print('\n')
        for i, module in enumerate(modules, 1):
            pt.green('{}. {} | {}'.format(i, module['module_name'], module['yaml_path']))
        print('\n')

    def __active(self):

        active_module = self.__manager.active_module
        if active_module is None:
            pt.info('There no active ConPlex configurations in this project')
            return
        pt.green('\n"{}" is currently the active module\n'.format(active_module['module_name']))

    def __delete(self):
        from .delete_project import DeleteProject
        DeleteProject(self.__manager)
        pt.success('')
