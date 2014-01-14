import os
from setuptools import setup, find_packages

from plugins import __version__

repo_directory = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(repo_directory, 'README.md')).read()
except:
    long_description = None

setup(
    name='gds-nagios-plugins',
    version=__version__,
    packages=find_packages(exclude=['test*']),

    author='Tom Booth',
    author_email='tombooth@gmail.com',
    maintainer='Government Digital Service',
    url='https://github.com/alphagov/nagios-plugins',

    description='nagios-plugins: a set of useful nagios plugins',
    long_description=long_description,
    license='MIT',
    keywords='',

    setup_requires=['setuptools-pep8'],
    install_requires=[],
    tests_require=[
        "nose==1.3.0",
        "freezegun==0.1.11"
    ],

    test_suite='nose.collector',

    entry_points={
        'console_scripts': [
            'check_reboot_required=plugins.command.check_reboot_required:main'
        ]
    }
)
