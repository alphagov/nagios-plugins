import string
import subprocess
import sys

from plugins.output import (CheckException,
                            nagios_ok,
                            nagios_warning,
                            nagios_critical,
                            nagios_message)


def parse_output(apt_check_output):
    packages_to_update = string.split(apt_check_output, ';')

    return (int(packages_to_update[0]),
            int(packages_to_update[1]))


def parse_apt_check(apt_check_output, critical, warning):
    (_, security_updates) = parse_output(apt_check_output)

    if security_updates >= critical:
        nagios_critical("%s security updates need to be"
                        "applied with 'apt-get dist-upgrade'"
                        % security_updates)
    elif security_updates >= warning:
        nagios_warning("%s security updates need to be"
                       "applied with 'apt-get dist-upgrade'"
                       % security_updates)
    else:
        nagios_ok("All security updates applied")


usage_message = """
Usage: check_apt_security_updates [critical] [warning]

Checks the number of outstanding security updates

When given no arguments, the default threshold is 0 updates.
One argument will raise a critical alert at that number of updates.
Two arguments will raise a warning at the first number of updates
and a critical at the second number of updates
"""


def main():
    try:
        if len(sys.argv) >= 3:
            warning = sys.argv[2]
            critical = sys.argv[1]
        elif len(sys.argv) == 2:
            if sys.argv[1] == "-h":
                print usage_message
                sys.exit(0)
            else:
                warning = sys.argv[1]
                critical = sys.argv[1]
        else:
            warning = 0
            critical = 0

        proc = subprocess.Popen(['/usr/lib/update-notifier/apt-check'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        apt_check_output = proc.stdout.read()
        parse_apt_check(apt_check_output, critical, warning)

    except CheckException as e:
        nagios_message(e.message, e.severity)
    except Exception as e:
        # Catching all other exceptions
        nagios_message("Exception: %s" % e, 3)
