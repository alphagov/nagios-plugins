import sys


class CheckException(Exception):
    def __init__(self, message, severity):
        Exception.__init__(self, message)
        self.severity = severity


def nagios_message(message, exitcode):
    """Format a Nagios message and exit"""
    print message
    sys.exit(exitcode)


def nagios_ok(message):
    """Nagios OK message"""
    raise CheckException("OK: %s" % message, 0)


def nagios_warning(message):
    """Nagios WARNING message"""
    raise CheckException("WARNING: %s" % message, 1)


def nagios_critical(message):
    """Nagios CRITICAL message"""
    raise CheckException("CRITICAL: %s" % message, 2)


def nagios_unknown(message):
    """Nagios UNKNOWN message"""
    raise CheckException("UNKNOWN: %s" % message, 3)
