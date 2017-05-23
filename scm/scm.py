# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
import json
import shlex
import subprocess
from functools import wraps

import click
import requests
from prompt_toolkit import prompt, AbortAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .errors import errors, UnauthorizedError
from .completer import SCMCompleter
from .completion import completions
from .style import DocumentStyle, get_prompt_tokens
from .utils import get_params, TextUtils


def handle_result(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except UnauthorizedError:
                url = kwargs.get('url')
                click.echo('Please login')
                subprocess.call(['python', __file__, 'login', url])
                break
            except requests.ConnectionError:
                click.secho('Can not connect to content manager!', fg='red')
                break
            except Exception as e:
                click.secho(str(e), fg='red')
    return wrapper


def process_command(session, url, text):
    words = shlex.split(text.strip())
    if not words:
        return
    elif len(words) < 2:
        cmd = words[0]
        if cmd not in ('scm', 'help'):
            click.secho('No such command `{}`'.format(cmd), fg='red')
    else:
        cmd, api_name = words[0], words[1]
        api_infos = completions.get(api_name)
        if api_infos is None:
            click.secho('No such api `{}`'.format(api_name), fg='red')
            return
        if cmd not in ('scm', 'help'):
            click.secho('No such command `{}`'.format(cmd), fg='red')
            return
        elif cmd == 'help':
            click.echo(json.dumps(api_infos, indent=2))
        else:
            path = api_infos['path']
            method = api_infos['operation']
            merged_kwargs = {}
            path_params = get_params(words[2:], '--path-param.')
            qry_params = get_params(words[2:], '--qry-param.')
            qry_body = get_params(words[2:], '--qry-body.')
            path = path.format(**dict(path_params))
            merged_kwargs['json'] = qry_body
            merged_kwargs['params'] = qry_params
            rv = session.request(method,
                                 '{url}{path}'.format(url=url, path=path),
                                 **merged_kwargs)
            status_code = rv.status_code
            if status_code < 400:
                click.secho(str(status_code), fg='green')
            else:
                click.secho(str(status_code), fg='red')
            if status_code in (401,):
                raise errors[str(status_code)]
            try:
                click.echo(json.dumps(rv.json(), indent=2))
            except json.JSONDecodeError:
                click.echo(rv.text)


def update_completions(session, url, path='/api/rest/apidoc'):
    r = session.get('{url}{path}'.format(url=url, path=path))
    doc = r.json()
    api = doc['list']
    completion = {}
    props = ['path', 'description', 'operation',
             'pathParameters', 'queryParameters', 'queryBody']
    for item in api:
        for op in item['operations']:
            name = '-'.join([word.lower() for word in op['name'].split(' ')])
            completion[name] = {prop: op.get(prop) for prop in props
                                if prop != 'queryBody'}
            body = op.get('queryBody')
            if body is not None and isinstance(body, str):
                sub_body = re.sub('[\n\s\'\"]+', '', body)
                if not sub_body.startswith('{') or not sub_body.endswith('}'):
                    completion[name]['queryBody'] = sub_body
                else:
                    words = re.findall('[^{}:\[\],]+', sub_body)
                    for idx, char in enumerate(words):
                        sub_body = sub_body.replace(char, '"%s"', 1)
                    sub_body = sub_body % tuple(words)
                    try:
                        completion[name]['queryBody'] = json.loads(sub_body)
                    except json.JSONDecodeError:
                        completion[name]['queryBody'] = sub_body
            else:
                completion[name]['queryBody'] = None

    with open('completions.json', 'w') as f:
        json.dump(completion, f, indent=2)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url', envvar='CM_URL')
@click.option('-u', '--username', prompt='Enter username')
@click.option('-p', '--password', prompt='Enter password', hide_input=True)
@click.option('--update-apidoc', is_flag=True)
@click.option('--display-meta', is_flag=True)
@handle_result
def login(url, username, password, update_apidoc, display_meta):
    s = requests.Session()
    r = s.post('{}/api/rest/auth/login'.format(url),
               json={'username': username, 'password': password})
    rest = r.json()
    if rest['status'] == 'login.failed':
        click.secho('Fail to login, wrong username or password!', fg='red')
        return
    headers = {item: rest[item]
               for item in ('token', 'apiToken', 'apiLicenseToken')}
    s.headers = headers

    if update_apidoc:
        update_completions(s, url)

    click.echo('Syntax: <command> [params] [options]')
    click.echo('Press `Ctrl+D` to exit')
    history = InMemoryHistory()
    history.append('scm apiname')
    history.append('help apiname')
    while True:
        try:
            text = prompt(get_prompt_tokens=get_prompt_tokens,
                          completer=SCMCompleter(TextUtils(display_meta)),
                          auto_suggest=AutoSuggestFromHistory(),
                          style=DocumentStyle,
                          history=history,
                          on_abort=AbortAction.RETRY)
        except EOFError:
            break
        process_command(s, url, text)
