# -*- coding: utf-8 -*-

import PrintTags as pt
from argparse import ArgumentParser
from ..project_manager import ProjectManager


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
        if args.selector == Arguments.list:
            self.__list()
        if args.selector == Arguments.active:
            self.__active()

    def __initialize(self):

        # TODO: Finish print

        from conplex.cli.initialize_project import InitializeProject
        InitializeProject(self.__manager)
        pt.success('')

    def __list(self):

        modules = self.__manager.list_modules()
        print('\n')
        for i, module in enumerate(modules, 1):
            pt.green('{}. {} | {}'.format(i, module['name'], module['yaml_path']))
        print('\n')

    def __active(self):

        active = self.__manager.active_module()
        pt.green('\n{} is currently the active module\n'.format(active['name']))

    