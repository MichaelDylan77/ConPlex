# -*- coding: utf-8 -*-

from re import sub, findall, compile, IGNORECASE


def sort_dict_last(x):

    """
    Sorts a dictionary, placing properties with values that are also
    dictionaries last. If a dictionary has the !dict flag, it will not
    be placed last with the other dict types
    """

    if not isinstance(x, dict):
        return x
    dicts = {}
    other = {}
    for key, value in x.items():
        if isinstance(value, dict) and '!dict' not in key:
            dicts[key] = value
        else:
            other[key] = value
    other.update(dicts)
    return other

def find_acronyms(x):
    return findall(r'\b[A-Z]*[A-Z]\b\.?', x)


def upper_camel_case(x):

    acronyms = find_acronyms(x)
    x = sub('\s+', '_', x)
    x = x.replace('_', ' ')
    x = [word[0].capitalize() + word[1:] for word in x.split(' ')]
    x = ' '.join(x)
    x = x.replace(' ', '')
    for acronym in acronyms:
        pattern = compile(acronym, IGNORECASE)
        x = pattern.sub(acronym, x)
    return x


def snake_case(x):

    """
    Converts a string to snake case
    """

    # Disclaimer: This method is annoyingly complex, and i'm sure there is a much better way to do this. 

    # The idea is to iterate through the characters
    # in the string, checking for specific cases and handling them accordingly. One note,
    # the built it isupper() and islower() methods will consider an underscore False.
    # The process looks like this:

    # First, we will check if the current character is uppercase, if its not, we simply insert
    # that character into the new string as is.

    # Second, we need to see if it's the first character of the string. if it is, we will need
    # to check if it is part of an acronym that should stay capitalized, even in snake case(e.g. XML, JSON, HTML).
    # We do this by looking at the next character and checking if it is also capitalized. If it
    # is, we will insert the character in capital form, if not, we will lowercase it and insert it.
    # If the current character is NOT the first character of the string, we still need to determine
    # if it is part of an acronym. The same process is applied except now we also look at the previous
    # character to see if it is capitalized. If it is, we can assume this is part of an acronym.
    # If the next character is uppercase, but the previous one isn't, than we assume it is part of
    # an acronym and insert it in uppercase form. now, when checking if the previous character is lowercase during our acronym check,
    # it is possible that islower() will return False because the character before it is an underscore. This means
    # We have to handle both possibilities.

    x = sub('\s+', '_', x)  # First, we go ahead and replace any consecutive spaces with underscores
    out = ''
    for i, char in enumerate(x):
        if char.isupper():
            # Get the next and previous characters for later use
            next = x[i + 1]
            previous = x[i - 1]
            if not i == 0:  # Check if we are not at the first character
                if previous.islower():
                    out += '_'
                    if next.islower() or next == '_':
                        out += char.lower()
                        continue
                elif previous == '_':
                    if next.islower() or next == '_':
                        out += char.lower()
                        continue
            elif next.isupper():
                out += char
                continue
            else:
                out += char.lower()
                continue
        elif not char == '_' and x[i - 1].isupper() and x[i - 2].isupper():  # This could be a lowercased word following an acronym without any spaces
            out += '_'  # We will insert an underscore to break this character into its own word
        elif char == '_' and x[i - 1] == '_':
            continue
        out += char

    if out.endswith('_'):
        out = out[:len(out) - 1]
    return out


if __name__ == "__main__":
    pass
