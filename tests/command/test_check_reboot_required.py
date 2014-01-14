import unittest
import os

from freezegun import freeze_time

from plugins.command.check_reboot_required import (CheckException,
                                                   dpkg_log_lines,
                                                   grep,
                                                   parse_files)

script_directory = os.path.dirname(__file__)
dpkg_file = os.path.join(script_directory, '../fixtures/dpkg.log')
reboot_file = os.path.join(script_directory,
                           '../fixtures/reboot-required')
pkgs_file = os.path.join(script_directory,
                         '../fixtures/reboot-required.pkgs')
pkgs_unknown_file = os.path.join(script_directory,
                                 '../fixtures/reboot-required.pkgs.unknown')


class TestCheckRebootCommand(unittest.TestCase):
    def test_dpkg_log_lines_no_files(self):
        with self.assertRaisesRegexp(CheckException, 'None') as context:
            dpkg_log_lines(['/asasdfasdfasdf', '/34ggqg3q4g'])

        self.assertEqual(context.exception.severity, 3)

    def test_grep(self):
        grepped = grep('foo', ['foo', 'bar'])
        self.assertEqual(len(grepped), 1)
        self.assertEqual(grepped[0], 'foo')

    @freeze_time("2014-01-14")
    def test_parse_files_warning(self):
        with self.assertRaisesRegexp(CheckException, 'longer') as context:
            parse_files(warning_days=0,
                        critical_days=20,
                        dpkg_log_files=[dpkg_file],
                        reboot_required_file=reboot_file,
                        reboot_required_pkgs_file=pkgs_file)

        self.assertEqual(context.exception.severity, 1)

    @freeze_time("2014-01-14")
    def test_parse_files_critical(self):
        with self.assertRaisesRegexp(CheckException, 'longer') as context:
            parse_files(warning_days=0,
                        critical_days=2,
                        dpkg_log_files=[dpkg_file],
                        reboot_required_file=reboot_file,
                        reboot_required_pkgs_file=pkgs_file)

        self.assertEqual(context.exception.severity, 2)

    @freeze_time("2014-01-14")
    def test_parse_files_ok(self):
        with self.assertRaisesRegexp(CheckException, 'inside') as context:
            parse_files(warning_days=15,
                        critical_days=30,
                        dpkg_log_files=[dpkg_file],
                        reboot_required_file=reboot_file,
                        reboot_required_pkgs_file=pkgs_file)

        self.assertEqual(context.exception.severity, 0)

    @freeze_time("2014-01-14")
    def test_parse_files_no_install_date(self):
        with self.assertRaisesRegexp(CheckException, 'assumed') as context:
            parse_files(warning_days=15,
                        critical_days=30,
                        dpkg_log_files=[dpkg_file],
                        reboot_required_file=reboot_file,
                        reboot_required_pkgs_file=pkgs_unknown_file)

        self.assertEqual(context.exception.severity, 3)

    def test_parse_files_no_reboot_file(self):
        with self.assertRaisesRegexp(CheckException, 'exist') as context:
            parse_files(warning_days=15,
                        critical_days=30,
                        dpkg_log_files=[dpkg_file],
                        reboot_required_file='/lieruhgealrugh',
                        reboot_required_pkgs_file=pkgs_unknown_file)

        self.assertEqual(context.exception.severity, 0)

    def test_parse_files_no_reboot_file(self):
        with self.assertRaisesRegexp(CheckException, 'requiring') as context:
            parse_files(warning_days=15,
                        critical_days=30,
                        dpkg_log_files=[dpkg_file],
                        reboot_required_file=reboot_file,
                        reboot_required_pkgs_file='/erlgiuhaerg')

        self.assertEqual(context.exception.severity, 0)
