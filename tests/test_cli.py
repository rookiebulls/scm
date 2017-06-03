# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pip
import pexpect
from compat import unittest


class CliTest(unittest.TestCase):

    def test_run_cli(self):
        self.cli = None
        self.check_scm_installed()
        self.login()
        self.login_success()
        self.exit()

    def check_scm_installed(self):
        dists = set([di.key for di in pip.get_installed_distributions()])
        assert 'scm' in dists

    def login(self):
        """Run the process using pexpect.
        """
        self.cli = pexpect.spawnu('scm login')

    def login_success(self):
        """Expect to see prompt.
        """
        self.cli.expect('Enter username: ')
        self.cli.sendline('admin')
        self.cli.expect('Enter password: ')
        self.cli.sendline('admin')
        self.cli.expect('scm')

    def exit(self):
        """Send Ctrl + D to exit.
        """
        self.cli.sendcontrol('d')
        self.cli.expect(pexpect.EOF)
