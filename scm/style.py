# -*- coding: utf-8 -*-

from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
        Token.Host: '#00ff00',
        Token.Pound: '#00ff00',
    }
    styles.update(DefaultStyle.styles)


def get_prompt_tokens(cli):
    return [
        (Token.Host, 'scm'),
        (Token.Pound, '>>> '),
    ]
