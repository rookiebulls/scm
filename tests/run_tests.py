# -*- coding: utf-8 -*-

from compat import unittest

from test_completer import CompleterTest

try:
    from test_cli import CliTest
except Exception:
    pass

if __name__ == '__main__':
    unittest.main()
