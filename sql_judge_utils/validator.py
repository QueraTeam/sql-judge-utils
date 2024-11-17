import re


def check_hostname(hostname):
    if not isinstance(hostname, str):
        return False
    if not 0 < len(hostname) <= 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def check_space_not_allowed(value):
    return bool(re.compile("^[A-Za-z0-9]{1,64}$").match(value))


VALIDATORS = {
    "host": check_hostname,
    "port": lambda port: isinstance(port, int) or (isinstance(port, str) and port.isdigit()),
    "username": lambda username: bool(re.compile("^[A-Za-z0-9]{1,64}$").match(username)),
    "password": lambda password: password is None or check_space_not_allowed(password),
    "db_name": check_space_not_allowed,
}


def validate_db_argument(arg_name, arg_value):
    validator = VALIDATORS.get(arg_name)
    if not validator:
        return arg_value
    if not validator(arg_value):
        raise Exception(f"Invalid {arg_name}")
    return arg_value
