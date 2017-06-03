# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import mock
from tests.compat import unittest

from prompt_toolkit.document import Document

from scm.completer import SCMCompleter
from scm.utils import TextUtils


class CompleterTest(unittest.TestCase):

    def setUp(self):
        self.completer = SCMCompleter(text_utils=TextUtils())
        self.completer_event = self.create_completer_event()

    def create_completer_event(self):
        return mock.Mock()

    def _get_completions(self, command):
        """
        :rtype instance like {Completion(text='help', start_position=-1)}
        """
        position = len(command)
        result = set(self.completer.get_completions(
            Document(text=command, cursor_position=position),
            self.completer_event))
        return result

    def verify_completions(self, commands, expected):
        result = set()
        for command in commands:
            # Call autocompleter
            result.update(self._get_completions(command))
        result_texts = []
        for item in result:
            # Each result item is a Completion object,
            # we are only interested in the text portion
            result_texts.append(item.text)
        assert result_texts
        if len(expected) == 1:
            self.assertIn(expected[0], result_texts)
        else:
            for item in expected:
                self.assertIn(item, result_texts)

    def test_blank(self):
        text = ''
        expected = set([])
        result = self._get_completions(text)
        self.assertEqual(result, expected)

    def test_no_completions(self):
        text = 'foo'
        expected = set([])
        result = self._get_completions(text)
        self.assertEqual(result, expected)

    def test_command(self):
        commands = ['h', 's']
        expected = ['help', 'scm']
        self.verify_completions(commands, expected)

    def test_path_params(self):
        commands = ['scm find-player-by-id -']
        expected = ['--path-param.id']
        self.verify_completions(commands, expected)

    def test_qry_params(self):
        commands = ['scm list-players -']
        expected = [
            '--qry-param.fields',
            '--qry-param.limit',
            '--qry-param.offset',
            '--qry-param.sort',
            '--qry-param.search'
        ]
        self.verify_completions(commands, expected)

    def test_qry_body(self):
        commands = ['scm create-player -']
        expected = [
            '--qry-body.description',
            '--qry-body.name'
        ]
        self.verify_completions(commands, expected)
