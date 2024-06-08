from configparser import ConfigParser
import os


def read_config(section, filename='config.ini'):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    parser = ConfigParser()
    parser.read(config_path)
    res = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            res[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, config_path))
    return res