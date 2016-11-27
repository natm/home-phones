import yaml
import os


def load_config():
    with open(os.environ['PHONES_CONFIG'], 'r') as stream:
        cfg = yaml.load(stream)
    return cfg


def match_number_in_section(number, section):
    cfg = load_config()
    # we store lookups without the leading plus
    number = str(number)
    if number.startswith("+"):
        number = number[1:]
    for entry, name in cfg[section].iteritems():
        if str(entry) == number:
            return name
    return None


def lookup_number(number):
    return match_number_in_section(number=number, section="lookup")


def is_rejected_number(number):
    return match_number_in_section(number=number, section="reject")
