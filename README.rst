nagios-plugins
==============

A collection of useful nagios plugins used in GDS infrastructure.

.. image:: https://travis-ci.org/alphagov/nagios-plugins.png?branch=master
   :target: https://travis-ci.org/alphagov/nagios-plugins

Installation
------------

    $ pip install gds-nagios-plugins

Requires update-notifier-common for ``check_reboot_required`` and ``check_apt_security_updates``

    $ apt-get install update-notifier-common

check_apt_security_updates
--------------------------

Checks the number of outstanding security updates.

    check_apt_security_updates [critical_number] [warning_number]

    Default threshold is 0 days

check_reboot_required
---------------------

Checks whether there are any packages that are waiting for a reboot until their installation is complete.

    check_reboot_required [critical_days] [warning_days]

    Default threshold is 0 days


check_puppetdb_ssh_host_keys
----------------------------

Checks whether machines have duplicate SSH host keys by querying facts in PuppetDB.

    check_puppetdb_ssh_host_keys [options]

check_elasticsearch
-------------------

Checks the health of elasticsearch clusters.

    check_elasticsearch [options]

