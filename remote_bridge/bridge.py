"""GitHub mailbox -> local Codex SDK. Python 3.10+, stdlib controller."""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
REPO = 'Tangxiaoxiao1992/active-physical-measurement'

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temp, path)

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def validate(c):
    if type(c.get('seq')) is not int or c['seq'] < 1:
        raise ValueError('seq must be a positive integer')
    if c.get('action') not in ('run', 'pause', 'stop'):
        raise ValueError('unknown action')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', c.get('task_id', '')):
        raise ValueError('invalid task_id')
    expiry = dt.datetime.fromisoformat(c['expires_at'].replace('Z', '+00:00'))
    if expiry.tzinfo is None or expiry <= dt.datetime.now(dt.timezone.utc):
        raise ValueError('expired command or missing timezone')
    if c['action'] == 'run' and (not isinstance(c.get('prompt'), str) or not 1 <= len(c['prompt']) <= 30000):
        raise ValueError('missing/oversized prompt')
    return c

def eligible(c, state):
    return c['seq'] > state['last_seq'] and (c['action'] != 'run' or c['task_id'] not in state['tasks'])

class GitHub:
    def __init__(self, token, repo, branch):
        self.token, self.repo, self.branch = token, repo, branch
    def request(self, method, endpoint, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request('https://api.github.com/' + endpoint, data=data, method=method,
            headers={'Authorization': 'Bearer ' + self.token, 'Accept': 'application/vnd.github+json',
                     'User-Agent': 'apm-local-bridge', 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.load(response)
        except urllib.error.HTTPError as e:
            if e.code == 404 and method == 'GET':
                return None
            raise RuntimeError('GitHub HTTP ' + str(e.code)) from None
    def get(self, path):
        return self.request('GET', 'repos/' + self.repo + '/contents/' + path + '?ref=' + urllib.parse.quote(self.branch, safe=''))
    def command(self):
        obj = self.get('control/command.json')
        if obj is None:
            raise RuntimeError('command file missing or repository inaccessible')
        return json.loads(base64.b64decode(obj['content']).decode('utf-8'))
    def put(self, path, text):
        current = self.get(path)
        body = {'message': 'bridge: update ' + path, 'branch': self.branch,
                'content': base64.b64encode(text.encode()).decode()}
        if current:
            body['sha'] = current['sha']
        return self.request('PUT', 'repos/' + self.repo + '/contents/' + path, body)

def terminate_tree(proc):
    if proc.poll() is not None:
        return
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True, timeout=15)
    else:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
    proc.wait(timeout=15)

def worker(job_path):
    job = json.loads(Path(job_path).read_text(encoding='utf-8'))
    os.chdir(job['workspace'])
    # GitHub publication credentials must not be passed to Codex.
    for key in ('APM_GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_TOKEN'):
        os.environ.pop(key, None)
    from openai_codex import Codex, Sandbox
    options = {'sandbox': Sandbox.workspace_write if job['write_enabled'] else Sandbox.read_only}
    if job.get('model'):
        options['model'] = job['model']
    prefix = ('Follow local AGENTS.md. Complete only this bounded task. Do not change scoring truth, '
              'read held-out labels, publish files, or alter bridge controls. Do not read credential files. '
              'Do not launch detached/background processes. Preserve experiment records. '
              'Budget, permission or authentication blocks must be reported, never bypassed. '
              'Write a concise final report with actual evidence paths, failures and next steps. '
              'Final report may be published to a public GitHub repository: include no secrets or private data.\n')
    with Codex() as codex:
        thread = codex.thread_start(**options)
        result = thread.run(prefix + job['prompt'])
        save(job['result_path'], {'report': result.final_response, 'completed_at': now()})

def redact(text, token):
    text = text.replace(token, '[REDACTED]') if token else text
    text = re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]+)', '[REDACTED]', text)
    return text[:40000]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.json')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--worker')
    args = parser.parse_args()
    if args.worker:
        worker(args.worker)
        return
    cfg_path = Path(args.config).resolve()
    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
    if cfg.get('repo', REPO) != REPO:
        raise ValueError('This bridge is pinned to the project repository')
    workspace = Path(cfg['workspace']).resolve()
    if not workspace.is_dir():
        raise ValueError('workspace does not exist')
    token = os.environ.get('APM_GITHUB_TOKEN', '')
    if not token:
        raise ValueError('Set APM_GITHUB_TOKEN locally; never commit it')
    gh = GitHub(token, REPO, cfg.get('branch', 'main'))
    command = gh.command()
    if args.check:
        import importlib.util
        print(json.dumps({'github_read': True, 'workspace_exists': True,
                          'sdk_installed': importlib.util.find_spec('openai_codex') is not None,
                          'current_command_seq': command.get('seq'),
                          'execution_enabled': cfg.get('execution_enabled', False)}, indent=2))
        print('No Codex call made. GitHub write and Codex authentication still require smoke validation.')
        return
    # One bridge per machine by default. Lock is released by OS even on crash.
    lock = socket.socket()
    if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
        lock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    lock.bind(('127.0.0.1', int(cfg.get('lock_port', 47683))))
    lock.listen(1)
    local = cfg_path.parent / 'runtime'
    state_path = local / 'state.json'
    state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {'last_seq': 0, 'tasks': {}, 'active': None}
    if state.get('active'):
        old = state['active']
        state['tasks'][old] = 'interrupted_unknown'
        state['active'] = None
        save(state_path, state)
        raise RuntimeError('Previous task interrupted. Inspect/stop orphan processes, then restart. Task will not auto-repeat.')
    proc = None
    task_id = None
    log = None
    report_path = None
    started = 0
    last_publish = 0
    status = 'idle'
    detail = 'waiting'
    poll = max(10, int(cfg.get('poll_seconds', 20)))
    timeout = max(30, int(cfg.get('max_task_seconds', 1800)))
    try:
        while True:
            try:
                c = gh.command()
                if c.get('seq', 0) > state['last_seq']:
                    validate(c)
                    if c['action'] == 'stop':
                        # Targeted stop cannot accidentally kill a newer unrelated task.
                        if proc and c['task_id'] == task_id:
                            terminate_tree(proc)
                            status = 'stopped'
                        state['last_seq'] = c['seq']
                        detail = 'stop processed for ' + c['task_id']
                    elif c['action'] == 'pause':
                        state['last_seq'] = c['seq']
                        detail = 'paused: current task may finish; no new task until a newer run command'
                        if not proc:
                            status = 'paused'
                    elif not proc and eligible(c, state):
                        if not cfg.get('execution_enabled', False):
                            detail = 'execution disabled locally; command not consumed'
                        else:
                            task_id = c['task_id']
                            folder = local / task_id
                            folder.mkdir(parents=True, exist_ok=True)
                            report_path = folder / 'result.json'
                            job = {'workspace': str(workspace), 'prompt': c['prompt'],
                                   'write_enabled': bool(cfg.get('write_enabled', False)),
                                   'model': cfg.get('model'), 'result_path': str(report_path)}
                            save(folder / 'job.json', job)
                            # Durable claim before launch: at-most-once across restarts.
                            state['last_seq'] = c['seq']
                            state['active'] = task_id
                            state['tasks'][task_id] = 'claimed'
                            save(state_path, state)
                            log = (folder / 'worker.log').open('w', encoding='utf-8')
                            env = {k: v for k, v in os.environ.items() if k not in ('APM_GITHUB_TOKEN', 'GH_TOKEN', 'GITHUB_TOKEN')}
                            options = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
                            try:
                                proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--worker', str(folder / 'job.json')],
                                                        stdout=log, stderr=subprocess.STDOUT, env=env, **options)
                            except Exception:
                                log.close()
                                log = None
                                state['active'] = None
                                state['tasks'][task_id] = 'launch_failed'
                                save(state_path, state)
                                status = 'failed'
                                raise
                            started = time.monotonic()
                            status, detail = 'running', 'Codex task started'
                    elif not proc and c['action'] == 'run' and c['task_id'] in state['tasks']:
                        state['last_seq'] = c['seq']
                        detail = 'duplicate task_id ignored'
                    save(state_path, state)
            except Exception as e:
                detail = 'control read/validation failed: ' + type(e).__name__
                print(detail, flush=True)
            if proc:
                if proc.poll() is None and time.monotonic() - started > timeout:
                    terminate_tree(proc)
                    status = 'timed_out'
                if proc.poll() is not None:
                    if status not in ('stopped', 'timed_out'):
                        status = 'completed' if proc.returncode == 0 and report_path.exists() else 'failed'
                    state['tasks'][task_id] = status
                    state['active'] = None
                    save(state_path, state)
                    log.close()
                    log = None
                    proc = None
                    detail = 'result saved locally; no automatic rerun'
                    if status == 'completed' and cfg.get('publish_report', False):
                        state.setdefault('pending_reports', []).append(task_id)
                        save(state_path, state)
                    last_publish = 0
            if time.monotonic() - last_publish >= max(60, poll):
                payload = {'updated_at': now(), 'task_id': task_id, 'status': status, 'detail': detail,
                           'last_seq': state['last_seq'], 'execution_enabled': cfg.get('execution_enabled', False)}
                save(local / 'status.json', payload)
                try:
                    gh.put('progress/bridge-status.json', json.dumps(payload, ensure_ascii=False, indent=2))
                    pending = next(iter(state.get('pending_reports', [])), None)
                    if pending:
                        report = json.loads((local / pending / 'result.json').read_text(encoding='utf-8'))['report']
                        gh.put('progress/bridge-reports/' + pending + '.md', redact(report, token))
                        state['pending_reports'].remove(pending)
                        save(state_path, state)
                except Exception as e:
                    print('Publication failed: ' + type(e).__name__, flush=True)
                last_publish = time.monotonic()
            time.sleep(poll)
    finally:
        if proc:
            terminate_tree(proc)
            state['tasks'][task_id] = 'stopped_local'
            state['active'] = None
            save(state_path, state)
        if log:
            log.close()
        lock.close()

if __name__ == '__main__':
    main()
