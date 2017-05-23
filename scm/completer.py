# -*- coding: utf-8 -*-

import json

from prompt_toolkit.completion import Completer

from .completion import custom_completion, completions


class SCMCompleter(Completer):

    def __init__(self, text_utils):
        self.text_utils = text_utils

    def get_completions(self, document, _):
        """Get completions for the current scope.
        :param document: An instance of `prompt_toolkit.Document`.
        :param _: (Unused).
        """
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        commands = []
        if len(words) == 0:
            return commands
        if len(words) == 1 and word_before_cursor:
            commands.extend(['scm', 'help'])
            self.text_utils.META_LOOKUP['scm'] = 'request api'
            self.text_utils.META_LOOKUP['help'] = 'api help message'
        elif len(words) == 2 and words[0] in ('scm', 'help') and \
                word_before_cursor != '':
            commands.extend(completions.keys())
            for key in completions.keys():
                self.text_utils.META_LOOKUP[
                    key] = completions[key]['description']
        elif len(words) > 2 and words[0] == 'scm' and \
                words[1] in completions.keys() and \
                word_before_cursor:
            api_name = words[1]
            api_infos = completions.get(api_name)
            path_params = api_infos.get('pathParameters')
            qry_params = api_infos.get('queryParameters')
            qry_body = api_infos.get('queryBody')
            if path_params is not None:
                for path_param in path_params:
                    cmd = '--path-param.{name}'.format(**path_param)
                    commands.append(cmd)
                    self.text_utils.META_LOOKUP[
                        cmd] = path_param.get('description')
            if qry_params is not None:
                for qry_param in qry_params:
                    cmd = '--qry-param.{name}'.format(**qry_param)
                    commands.append(cmd)
                    self.text_utils.META_LOOKUP[
                        cmd] = qry_param.get('description')
            if qry_body is not None:
                if custom_completion.get(api_name) is not None:
                    qry_body = custom_completion[api_name].get('queryBody')
                try:
                    for key, value in qry_body.items():
                        cmd = '--qry-body.{}'.format(key)
                        commands.append(cmd)
                        self.text_utils.META_LOOKUP[cmd] = json.dumps(value)
                except Exception:
                    pass
        completer = self.text_utils.find_matches(
            word_before_cursor, commands)
        return completer
