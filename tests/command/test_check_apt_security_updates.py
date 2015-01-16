import unittest

from plugins.output import CheckException
from plugins.command.check_apt_security_updates import (parse_apt_check,
                                                        parse_output)


class TestCheckAptSecurityUpdatesCommand(unittest.TestCase):
    def test_parsing(self):
        pkgs = parse_output('142;2')
        self.assertEqual(pkgs, (142, 2))

    def test_updates_ok(self):
        with self.assertRaisesRegexp(CheckException, 'All') as context:
            parse_apt_check(
                apt_check_output='142;2',
                critical=10,
                warning=5
            )

        self.assertEqual(context.exception.severity, 0)

    def test_updates_warning(self):
        with self.assertRaisesRegexp(CheckException, 'need') as context:
            parse_apt_check(
                apt_check_output='142;7',
                critical=10,
                warning=5
            )

        self.assertEqual(context.exception.severity, 1)

    def test_updates_critical(self):
        with self.assertRaisesRegexp(CheckException, 'need') as context:
            parse_apt_check(
                apt_check_output='142;12',
                critical=10,
                warning=5
            )

        self.assertEqual(context.exception.severity, 2)

    def test_packages_broken(self):
        apt_check_broken_message = 'E: Error: BrokenCount > 0'
        with self.assertRaisesRegexp(CheckException, "CRITICAL: apt-check output was not an int. Returned 'E: Error: BrokenCount > 0'") as context:
            parse_apt_check(
                apt_check_output="{}".format(apt_check_broken_message),
                critical=10,
                warning=5
            )

        self.assertEqual(context.exception.severity, 2)
