#!/usr/bin/env python3
"""
 geolocate

 Programmed by: Dante Signal31

 email: dante.signal31@gmail.com

This scripts scan given text to find urls and IP addresses. The output is the
same text but every url and IP address is going to have its geolocation
appended.

Geolocate is possible thanks to `Maxmind GeoIP database <http://www.maxmind.com>`_
and their API.
"""
import argparse
import sys
from classes import geowrapper
from classes import parser
from classes import config

_must_pass_in_user_arguments = {"show_enabled_locators": False,
                                "set_locators_preference": True,
                                "show_disabled_locators": False,
                                "reset_locators_preference": False,
                                "set_user": True,
                                "set_password": True}


def parse_arguments():
    verbosity_choices = parser.GeolocateInputParser.VERBOSITY_LEVELS
    arg_parser = argparse.ArgumentParser(description="Locate IP adresses "
                                                     "in given text.\n",
                                         epilog="This program is possible "
                                                "thanks to Maxmind GeoIP "
                                                "database "
                                                "<http://www.maxmind.com> and "
                                                "their API.")
    data_input_arguments = arg_parser.add_mutually_exclusive_group()
    data_input_arguments.add_argument(dest="text_to_parse",
                                      metavar="\"text to parse\"",
                                      nargs="?", type=str, default=None,
                                      help="Text to analyze surrounded by "
                                           "double quotes.")
    data_input_arguments.add_argument("-s", "--stream",
                                      dest="stream_mode",
                                      action="store_true", default=False,
                                      help="Program will analyze piped output "
                                           "from another program.")
    arg_parser.add_argument("-v", "--verbosity", dest="verbosity",
                            choices=verbosity_choices, type=int, default=0,
                            help="0-3 The higher the more geodata.")
    arg_parser.add_argument("-l", "--show_enabled",
                            dest="show_enabled_locators",
                            action="store_true", default=False,
                            help="Show enabled locators ordered by preference.")
    arg_parser.add_argument("-p", "--set_preference",
                            dest="set_locators_preference",
                            nargs="*", default=None,
                            help="Set preferred locator order.",
                            metavar="locator")
    arg_parser.add_argument("-d", "--show_disabled",
                            dest="show_disabled_locators", action="store_true",
                            default=False, help="Show disabled locators.")
    arg_parser.add_argument("-r", "--reset", dest="reset_locators_preference",
                            action="store_true", default=False,
                            help="Restore default locator order.")
    arg_parser.add_argument("-u", "--set_user",
                            dest="set_user",
                            type=str, default=None,
                            help="Set user for webservice database access.",
                            metavar="account_id")
    arg_parser.add_argument("-w", "--set_password",
                            dest="set_password",
                            type=str, default=None,
                            help="Set password for webservice database access.",
                            metavar="account_password")
    return arg_parser.parse_args()


def show_enabled_locators():
    """ Print in console enabled locators ordered by preference.

    :return: None
    """
    enabled_locators = _get_enabled_locators_list()
    _print_locators_list("Enabled locators:", enabled_locators)


def set_locators_preference(arguments):
    """ Change locators list with new list given in arguments.

    :param arguments:  Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: None
    """
    with config.OpenConfigurationToUpdate() as f:
        f.configuration.locators_preference = arguments.set_locators_preference



def show_disabled_locators():
    """ Print in console enabled locators ordered by preference.

    :return: None
    """
    enabled_locators_set = set(_get_enabled_locators_list())
    complete_locators_set = set(config.DEFAULT_LOCATORS_PREFERENCE)
    disabled_locators_set = complete_locators_set - enabled_locators_set
    _print_locators_list("Disabled locators:", disabled_locators_set)


def reset_locators_preference():
    """ Sets back locators list to it's default value.

    :return: None
    """
    with config.OpenConfigurationToUpdate() as f:
        f.configuration.reset_locators_preference()


def _get_enabled_locators_list():
    """
    :return: Configuration locators preference.
    :rtype: list
    """
    configuration = config.load_configuration()
    enabled_locators = configuration.locators_preference
    return enabled_locators


def set_user(arguments):
    """ Set user for webservice database access.

    :param arguments:  Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: None
    """
    # TODO: Implement.
    pass


def set_password(arguments):
    """ Set password for webservice database access.

    :param arguments:  Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: None
    """
    # TODO: Implement.
    pass


def print_lines_parsed(parser):
    for line in parser:
        print(line, end="")


def _print_locators_list(header, locators_list):
    """ Print on console a formatted list of locators.

    :param header: Title of list.
    :type header: str
    :param locators_list: Locators list.
    :type locators_list: list or set
    :return: None
    """
    components = list(locators_list)
    components.insert(0, header)
    message = "\n".join(components)
    print(message)


def process_optional_parameters(arguments):
    """ Take all optional arguments given by user and run one by one all
    functions assigned to each of them.

    :param arguments: Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: None
    """
    functions_to_execute = _get_functions_to_execute(arguments)
    for functions in functions_to_execute:
        try:
            _execute_function(functions, arguments)
        except (NoFunctionAssignedToArgument, config.UnknownLocators) as e:
            sys.exit(". ".join([e.message, "Exiting"]))


def _get_functions_to_execute(arguments):
    """
    :param arguments: Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: Function names set to execute.
    :rtype: set
    """
    valid_arguments = _get_user_arguments(arguments)
    functions_names_set = {argument for argument in valid_arguments
                           if getattr(arguments, argument)}
    return functions_names_set


def _get_user_arguments(arguments):
    """ Get public user attributes of arguments object.

    Arguments set by user are defined public in object returned by
    ArgumentParser.parse_args(). Built-in attributes in that object are defined
    "private" with "_" o "__" prefix.

    :param arguments: Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: Public attribute list of arguments object.
    :rtype: set
    """
    attribute_list = dir(arguments)
    public_attributes_set = {argument for argument in attribute_list
                             if not argument.startswith("_")}
    public_attributes_set = _remove_non_user_attributes(public_attributes_set)
    return public_attributes_set


def _remove_non_user_attributes(attributes_set):
    """ Takes out from attribute set public attributes not defined by user.

    :param attributes_set: Public attribute list of arguments object.
    :type attributes_set: set
    :return: Public attribute list of arguments object without non user attributes.
    :rtype: set
    """
    # Arguments object returned by ArgumentParser.parse_args() include by
    # default "index" and "count" public attributes. We don't need them so we
    # strip them off. Arguments "verbosity", "text_to_parse" and "stream_mode"
    # is not an optional parameter and shouldn't be processed as one.
    non_user_attributes = {"index", "count", "verbosity", "text_to_parse",
                           "stream_mode"}
    return attributes_set.difference(non_user_attributes)


def _execute_function(argument, arguments):
    """ Execute function assigned to given argument.

    :param argument: Argument to search a function assigned for.
    :param arguments: Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: None
    :raise: NoFunctionAssignedToArgument
    """
    try:
        if _must_pass_in_user_arguments[argument]:
            # Arguments names are equal to names of function to call.
            _call_function(argument, arguments)
        else:
            _call_function(argument)
    except KeyError:
        raise NoFunctionAssignedToArgument(argument)


def _call_function(function_name, arguments=None):
    """ Call given function and pass it in arguments if they are given.

    :param function_name: Function to call.
    :type function_name: str
    :param arguments:  Arguments object returned by ArgumentParser.parse_args()
    :type arguments: Namespace
    :return: None
    """
    function = globals().get(function_name)
    if arguments is None:
        function()
    else:
        function(arguments)


class NoFunctionAssignedToArgument(Exception):
    """ User has given and argument that has no function assigned yet."""

    def __init__(self, argument):
        self.argument = argument
        self.message = "Sorry, I don't know what to do " \
                       "with argument: {0}".format(self.argument)
        Exception.__init__(self, self.message)

if __name__ == "__main__":
    arguments = parse_arguments()
    process_optional_parameters(arguments)
    configuration = config.load_configuration()
    geoip_database = geowrapper.load_geoip_database(configuration)
    if arguments.text_to_parse or arguments.stream_mode:
        input_parser = parser.GeolocateInputParser(arguments.verbosity,
                                           geoip_database,
                                           arguments.text_to_parse)
        print_lines_parsed(input_parser)
    print()