from setuptools import setup
import re

version = re.search('^__version__\s*=\s*"(.*)"', open('conplex/__init__.py').read(), re.M).group(1)

name = 'conplex'
description = 'Simplified Python project configuration'
long_description = 'ConPlex aims to simplify your Python workflow by providing a configuration model that combines the simplicity of YAML with the functionality of a configuration file written in Python. With ConPlex, you write your config once in YAML, and the run a single command. ConPlex transpiles your YAML file into a Python module; making it importable, and fully supported by code completion.'
url='https://github.com/MichaelDylan77/ConPlex'
author = 'Michael Lockyer'
author_email = 'mdlockyer@gmail.com'
license = 'MIT License'
classifiers = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
install_requires = ['PrintTags', 'pyyaml']
entry_points = {"console_scripts": ['conplex = conplex.conplex:main']}
zip_safe = False
packages = ['conplex']
    
setup(name=name, 
      description=description, 
      long_description=long_description, 
      version=version, 
      url=url, 
      author=author, 
      author_email=author_email, 
      license=license, 
      classifiers=classifiers, 
      install_requires=install_requires,
      entry_points=entry_points,
      zip_safe=zip_safe, 
      packages=packages)