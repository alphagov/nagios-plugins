import os
import unittest
import httpretty

from plugins.output import CheckException
from plugins.command.check_puppetdb_ssh_host_keys import check

FIXTURES = os.path.join(os.path.dirname(__file__), '..', 'fixtures')

PUPPETDB_BASE = "http://puppetdb.example.com/v2"
PUPPETDB_URL = PUPPETDB_BASE + "/facts?query=%5B%22or%22%2C+" + \
    "%5B%22%3D%22%2C+%22name%22%2C+%22sshdsakey%22%5D%2C+" + \
    "%5B%22%3D%22%2C+%22name%22%2C+%22sshecdsakey%22%5D%2C+" + \
    "%5B%22%3D%22%2C+%22name%22%2C+%22sshrsakey%22%5D%5D"

def fixture(name):
    f = open(os.path.join(FIXTURES, name))
    return f.read()

class TestCheckPuppetdbSshHostKeysCommand(unittest.TestCase):
    @httpretty.activate
    def test_uniques_ok(self):
        httpretty.register_uri(
            httpretty.GET,
            PUPPETDB_URL,
            body=fixture('puppetdb-sshkeys.uniques'),
        )

        with self.assertRaises(CheckException) as context:
            check(PUPPETDB_BASE)

        self.assertEqual(context.exception.severity, 0)
        self.assertEqual(context.exception.message,
            'OK: No duplicate SSH host keys found')


    @httpretty.activate
    def test_two_dupes_one_good_critical(self):
        httpretty.register_uri(
            httpretty.GET,
            PUPPETDB_URL,
            body=fixture('puppetdb-sshkeys.two_dupes_one_good'),
        )

        message = """CRITICAL: Found hosts with duplicate SSH host keys

67:5c:1e:29:ac:f3:ed:dc:ee:a5:d1:c1:e3:75:0e:3f
- puppetmaster-1.management.development
- rabbitmq-1.backend.development

79:24:ac:76:4e:a6:28:35:9b:83:ee:10:bf:0e:f8:ab
- puppetmaster-1.management.development
- rabbitmq-1.backend.development

d8:9d:01:44:5a:26:de:07:82:96:b9:ae:a4:75:3e:ad
- puppetmaster-1.management.development
- rabbitmq-1.backend.development"""

        with self.assertRaises(CheckException) as context:
            check(PUPPETDB_BASE)

        self.assertEqual(context.exception.severity, 2)
        self.assertEqual(context.exception.message, message)

    @httpretty.activate
    def test_empty_unknown(self):
        httpretty.register_uri(
            httpretty.GET,
            PUPPETDB_URL,
            body=fixture('puppetdb-sshkeys.empty'),
        )

        with self.assertRaises(CheckException) as context:
            check(PUPPETDB_BASE)

        self.assertEqual(context.exception.severity, 3)
        self.assertEqual(context.exception.message,
            'UNKNOWN: Need at least two nodes in PuppetDB')


    @httpretty.activate
    def test_single_unknown(self):
        httpretty.register_uri(
            httpretty.GET,
            PUPPETDB_URL,
            body=fixture('puppetdb-sshkeys.single'),
        )

        with self.assertRaises(CheckException) as context:
            check(PUPPETDB_BASE)

        self.assertEqual(context.exception.severity, 3)
        self.assertEqual(context.exception.message,
            'UNKNOWN: Need at least two nodes in PuppetDB')
