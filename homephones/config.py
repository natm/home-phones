import yaml


def load_config():
    with open("/etc/phones.yaml", 'r') as stream:
        cfg = yaml.load(stream)
    return cfg


def lookup_number(number):
    cfg = load_config()
    # we store lookups without the leading plus
    number = str(number)
    if number.startswith("+"):
        number = number[1:]
    for entry, name in cfg["lookup"].iteritems():
        if str(entry) == number:
            return name
    return None
