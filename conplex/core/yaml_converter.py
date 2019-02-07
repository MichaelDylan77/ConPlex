# -*- coding: utf-8 -*-

from os import path, makedirs
from .utils import upper_camel_case, snake_case, sort_dict_last
import PrintTags as pt
from sys import exit


class YAMLConverter(object):

    # TODO: Make sure the output module automatically gets placed into the same directory as the yaml file

    """
    Ingests a YAML configuration file and generates a mirrored Python module

    args:
        yaml_path: (string) The path to the YAML configuration file to be mirrored
        output_dir: (string) The directory the newly generated Python module should be placed in
        module_name: (string) The name of the newly generated Python module. This will default to the YAML file name
        case_correction (experimental): (bool) Whether or not variable, attribute, and class names should be altered to fit standard Python conventions
        verbose: (bool) Whether or not to print additional information, including error descriptions
        silent: (bool) Silences all prints and outputs. This is useful when running ConPlex from inside a script or application to update the config at runtime
    """

    def __init__(self, yaml_path, output_dir=None, module_name=None, case_correction=False, verbose=False, silent=False):

        # Check that we do in fact have a YAML file at the yaml_path location
        if not path.isfile(yaml_path) and yaml_path.endswith('yaml'):
            if verbose:
                if not silent:
                    pt.warn('YAML file not found at location: {}'.format(yaml_path))
            else:
                if not silent:
                    pt.warn('YAML file not found')
            exit()

        # Here we are going to set up our paths and output directories
        yaml_name = yaml_path.split('/')[-1]  # Get the name of the YAML configuration file
        if output_dir is None:
            output_dir = yaml_path.replace(yaml_name, '')
        if module_name is None:
            module_name = yaml_name.split('.')[0]  # Get the YAML configuration file name without extension
            module_name = module_name.replace(' ', '_')
        self.__module_name = module_name

        self.__yaml_path = yaml_path  # The path to the yaml file that will be converted
        self.__output_dir = output_dir  # The directory in which the new Python module will be placed
        self.__output_path = path.join(output_dir + module_name)  # The path leading inside the new Python module
        self.__case_correction = case_correction  # Whether or not variable, attribute, and class names should be altered to fit standard Python conventions
        self.__verbose = verbose
        self.__silent = silent

        self.__yaml = None  # This will become the parsed yaml content
        self.__class_names = []  # This will become the list of class names in the Python configuration file
        self.__variable_names = []  # This will become the list of variable names not added as class attributes
        self.__data_string = '# -*- coding: utf-8 -*-\n\n'  # This will become the content of the Python configuration file

    def __call__(self):

        if self.__case_correction:
            if not self.__silent:
                pt.notice('Using automatic case correction is experimental and may not always work correctly')

        # Create the folder for the module
        if not path.isdir(self.__output_path):
            makedirs(self.__output_path)

        if not self.__silent:
            pt.info('Generating Python configuration from {}'.format(self.__yaml_path.split('/')[-1]))

        self.__load_yaml()
        self.__construct_python_config_string()
        self.__write_python_file()
        self.__write_init_file()

        if not self.__silent:
            pt.success('Generated Python configuration module with {} classes and {} variable(s)'.format(len(self.__class_names), len(self.__variable_names)))

        return len(self.__class_names), len(self.__variable_names)

    def __load_yaml(self):

        """
        Loads and parses the YAML configuration file
        """

        import yaml

        yaml_path = self.__yaml_path
        if path.isfile(yaml_path) and yaml_path.endswith('yaml'):
            try:
                with open(self.__yaml_path, 'r') as yaml_file:
                    try:
                        self.__yaml = yaml.load(yaml_file)
                    except Exception as e_1:
                        if self.__verbose:
                            if not self.__silent:
                                pt.error(e_1)
                        if not self.__silent:
                            pt.warn('Could not parse YAML file. Please check formatting, indentation, and aliases and try again')
                        exit()
            except IOError as e_2:
                if self.__verbose:
                    if not self.__silent:
                        pt.error(e_2)
                if not self.__silent:
                    pt.warn('Could not load YAML file: {}'.format(yaml_path.split('/')[-1]))
                exit()
        else:
            if self.__verbose:
                if not self.__silent:
                    pt.warn('YAML file not found at location: {}'.format(yaml_path))
            else:
                if not self.__silent:
                    pt.warn('YAML file not found')
            exit()

    def __construct_python_config_string(self):

        """
        Constructs the Python data string that will be written to the output Python
        configuration file
        """        

        yaml = self.__yaml
        if yaml is not None and type(yaml) == dict:
            for name, attributes in sort_dict_last(yaml).items():

                # Handle the dictionary flag
                if '!dict' in name:
                    name = name.replace('!dict', '')
                    if isinstance(attributes, dict):
                        if self.__case_correction:
                            name = snake_case(name)
                        else:
                            name = name.replace(' ', '_')
                        self.__variable_names.append(name)
                        self.__data_string += self.__add_attribute(name, attributes)
                        continue
                # Handle creating a new class
                if isinstance(attributes, dict):
                    if self.__case_correction:
                        name = upper_camel_case(name)
                    else:
                        name = name.replace(' ', '_')
                    if ' ' in name:
                        name = name.replace(' ', '')  # Remove spaces just in case
                    self.__class_names.append(name)
                    self.__data_string += self.__add_class(name, attributes)
                    if self.__verbose:
                        if not self.__silent:
                            pt.info('Added Python class with {} attributes titled: {}'.format(len(attributes), name))
                # Handle adding a new variable
                else:
                    if self.__case_correction:
                        name = snake_case(name)
                    else:
                        name = name.replace(' ', '_')
                    self.__variable_names.append(name)
                    self.__data_string += self.__add_attribute(name, attributes)
                    if self.__verbose:
                        if not self.__silent:
                            pt.info('Added Python variable titled: {}'.format(name))

    def __add_attribute(self, name, value, indentation=''):

        """
        Adds a variable to the Python configuration file
        """

        return indentation + '{} = {}\n'.format(name, value)

    def __add_class(self, name, attributes, indentation_count=0):
        
        """
        Builds out a class structure and adds it to the data string

        args:
            name: The name of the new class
            attributes: A dict containing attribute name, attribute value pairs
            indentation: A string containing the number of spaces the class should be indented
        """

        # TODO: improve the spacing and formatting of the output string

        indentation = (' ' * 4) + ('    ' * indentation_count)
        case_correction = self.__case_correction
        x = 'class {}:'.format(name)  # Build the base string for the class
        x += '\n\n'  # Two newlines for formatting

        # Here we loop through the attributes and add them to x. If the attribute value is a 
        # string we will wrap it in single quotes.
        for attr_name, attr_value in sort_dict_last(attributes).items():

            # Handle the dictionary flag
            if '!dict' in attr_name:
                attr_name = attr_name.replace('!dict', '')
                if isinstance(attr_value, dict):
                    if case_correction:
                        attr_name = snake_case(attr_name)
                    else:
                        attr_name = attr_name.replace(' ', '_')
                    x += indentation + '{} = {}'.format(attr_name, attr_value)
                    x += '\n'  # Newline for formatting
                    continue

            # Handle adding the dictionary as a class recursively if it doesn't have the dict flag
            if isinstance(attr_value, dict):
                x += '\n'
                if case_correction:
                    attr_name = upper_camel_case(attr_name)
                else:
                    attr_name = attr_name.replace(' ', '_')
                attr_indentation = '' * 4  # A single indentation of 4 spaces
                x += indentation + self.__add_class(attr_name, attr_value, indentation_count=indentation_count + 1)

            # Handle all other data types
            else:
                if case_correction:
                    attr_name = snake_case(attr_name)
                else:
                    attr_name = attr_name.replace(' ', '_')
                x += indentation + '{} = '.format(attr_name)  # Build the base attribute string
                if isinstance(attr_value, str):
                    x += "'{}'".format(attr_value)
                else:
                    x += '{}'.format(attr_value)
                x += '\n'

        x += '\n'  # Newline for formatting
        return x

    def __write_init_file(self):

        """
        Writes a Python init file for the configuration module
        """

        if self.__yaml is not None:
            x = ''
            # Import classes
            for i, class_name in enumerate(self.__class_names):
                if i == 0:
                    x += class_name
                else:
                    x += ', {}'.format(class_name)

            # Import variables
            for i, variable_name in enumerate(self.__variable_names):
                x += ', {}'.format(variable_name)

            x = 'from .config import ' + x
            x += '\n'

            # Set __all__
            x += '__all__ = ' + str(self.__class_names + self.__variable_names)

            init_file_path = path.join(self.__output_path, '__init__.py')
            try:
                with open(init_file_path, 'w+') as init_file:
                    try:
                        init_file.write(x)
                    except Exception as e_1:
                        if self.__verbose:
                            if not self.__silent:
                                pt.error(e_1)
                        if not self.__silent:
                            pt.warn('An error occurred while writing to the init file for the Python configuration module')
                        exit()
            except IOError as e_2:
                if self.__verbose:
                    if not self.__silent:
                        pt.error(e_2)
                if not self.__silent:
                    pt.warn('An error occurred while creating the init file for the Python configuration module')
                exit()
                
    def __write_python_file(self):

        """
        Writes the Python data string to a file
        """

        config_file_path = path.join(self.__output_path, 'config.py')
        try:
            with open(config_file_path, 'w+') as output_file:
                try:
                    output_file.write(self.__data_string)
                except Exception as e_1:
                    if self.__verbose:
                        if not self.__silent:
                            pt.error(e_1)
                    if not self.__silent:
                        pt.warn('An error occurred while writing to the Python configuration file')
                    exit()
        except IOError as e_2:
            if self.__verbose:
                if not self.__silent:
                    pt.error(e_2)
            if not self.__silent:
                pt.warn('An error occurred while creating the Python configuration file')
            exit()


if __name__ == "__main__":
    pass
