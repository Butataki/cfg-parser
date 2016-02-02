"""
Created on 02.02.16 11:46

Configuration parser class. Parsing config files with predetermined structure and
generating default one if no config file found.

.. py:module:: __init__.py
    :synopsis: Configuration parser class. Parsing config files with predetermined structure and
               generating default one if no config file found.

.. moduleauthor:: Roman Shuvalov <rshuvalov@abtronics.ru>
"""
import os
import sys
import re
from ConfigParser import ConfigParser

ROOT = sys.path[0]
UNDERSCORER_ONE = re.compile(r'(.)([A-Z][a-z]+)')
UNDERSCORER_TWO = re.compile('([a-z0-9])([A-Z])')


def convert_camel_case_to_underscore(s):
    """Utility function for string conversion

    Example usage

    In [1]: from cfg_parser import convert_camel_case_to_underscore

    In [2]: camel = 'SomeThingLikeThis'

    In [3]: convert_camel_case_to_underscore(camel)
    Out[3]: 'some_thing_like_this'


    :param s: input string in camel case formatting
    :return: output string in underscore formatting
    :rtype: str
    """
    subbed = UNDERSCORER_ONE.sub(r'\1_\2', s)
    return UNDERSCORER_TWO.sub(r'\1_\2', subbed).lower()


class Options(object):
    """Simple class for data storage
    """

    def get(self, attr_name, default=None):
        """Dictionary like get method

        :param attr_name: attribute name for fetching
        :param default: default value for not found attribute
        :return: value assigned to attribute or default
        """
        try:
            return self.__getattribute__(attr_name)
        except AttributeError:
            return default


class Configuration(object):
    """Configuration class for config files with predetermined structure.

    Structure is as follows:
     * All sections are lowercase without whitespaces
     * All fields are camel case and leading character represent type field contains

     Available types are:
       * i - integer, i.e. iInterval=30
       * f - float, i.e. fPrice=45.67
       * b - boolean, i.e. bEnableSpoofing=1
       * s - string, i.e. sEntryPointClass=MainMethanina
       * l - list, i.e. lProxyList=127.0.0.1:3456,127.0.0.1:2333,127.0.0.1:4565
    """

    def __init__(self, path_to_config_file, path_to_config_template=None):
        """Class initialisation

        :param path_to_config_file: file to read or create
        :param path_to_config_template: template for config file creation
        :return: Configuration class exemplar
        """
        self._config_file = path_to_config_file
        self._template_file = path_to_config_template
        self._config_parser = ConfigParser()
        self._config_parser.optionxform = str  # change default behavior for parameters processing, lowercase is default
        self._config_options = Options()

    def get_configuration(self):
        """Main and only one public method. Will read or create configuration file and return :obj:`cfg_parser.Options`
        containing sections and fields.

        :return: parsed configuration wrapped in :class:`cfg_parser.Options`

        :raise: :exp:`IOError` - in case config file was not found and was created
        """
        self._create_or_parse_config_file()
        return self._config_options

    def _create_or_parse_config_file(self):
        """This method will check if config file exists and is it do will send it further for parsing and if not will
        create new one form provided template or empty.

        :return: void

        :raise: :exp:`IOError`
        """
        # make empty template or read from template file
        if self._config_file is None:
            template = ''
        else:
            with open(self._template_file, 'r') as f:
                template = f.read()
        # read or create config file
        if not os.path.exists(self._config_file):
            print('Config file not found. Creating empty from template.')
            with open(self._config_file, 'w') as c_file:
                c_file.write(template)
            raise IOError('Config file not found and was created.')
        self._config_parser.read(self._config_file)
        self._parse_config_file()

    def _parse_config_file(self):
        """Section parsing. Each section is :obj:`cfg_parser.Options`

        :return: void
        """
        for section_name in self._config_parser.sections():
            section = self._parse_section(section_name)
            self._config_options.__setattr__(section_name, section)

    def _parse_section(self, name):
        """Main parsing function. Will parse section fields and typecast them according to leading character.
        Also all names will be transformed from camel case to underscore.

        :param name: section name
        :return: section fields wrapped in :class:`cfg_parser.Options`
        """
        section_data = Options()
        for item in self._config_parser.items(name):
            try:
                parameter, value = item
                # make typecasting
                if parameter[0] == 'i':
                    value = int(value)
                elif parameter[0] == 'f':
                    value = float(value)
                elif parameter[0] == 'b':
                    value = bool(value)
                elif parameter[0] == 's':
                    value = str(value)
                elif parameter[0] == 'l':
                    value = value.split(',')
                else:
                    raise TypeError('Unsupported type {} for parameter {}'.format(parameter[0], parameter))
                section_data.__setattr__(convert_camel_case_to_underscore(parameter[1:]), value)
            except (ValueError, TypeError), e:
                print('Error while parsing config file: {}'.format(e))
                continue
        return section_data