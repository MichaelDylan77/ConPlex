# -*- coding: utf-8 -*-

from sys import stdout


def query_yes_no(question, default=None):

    """
    Queries the user for a yes/no answer to a given question

    args:
        question: The question the user is answering
        default: The default answer if none is provided
    """

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            stdout.write("Please respond with 'yes', 'no', 'y', or 'n'\n")


def validate_module_name(module_name):

    """
    Checks if the given name is acceptable as a module name

    args:
        module_name: A string containing the name to be updated
    """

    for char in module_name:
        if char == '_':
            continue
        elif not char.isalpha() or char == ' ':
            return False
    return True
