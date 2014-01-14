nagios-plugins
==============

A collection of useful nagios plugins used in GDS infrastructure.

Installation
------------

    $ pip install gds-nagios-plugins

Requires update-notifier-common for ``check_reboot_required``

    $ apt-get install update-notifier-common

check_reboot_required
---------------------

Checks whether there are any packages that are waiting for a reboot until their installation is complete.

    check_reboot_required [critical_days] [warning_days]

    Default threshold is 0 days

