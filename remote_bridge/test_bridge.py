import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import bridge
class BridgeTests(unittest.TestCase):
    def command(self):
        return {'seq': 1, 'action': 'run', 'task_id': 'smoke-1', 'prompt': 'read only',
                'expires_at': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)).isoformat()}
    def test_valid(self):
        self.assertEqual(bridge.validate(self.command())['task_id'], 'smoke-1')
    def test_expired(self):
        c = self.command(); c['expires_at'] = '2000-01-01T00:00:00Z'
        with self.assertRaises(ValueError): bridge.validate(c)
    def test_path_injection(self):
        c = self.command(); c['task_id'] = '../escape'
        with self.assertRaises(ValueError): bridge.validate(c)
    def test_no_repeat_after_claim(self):
        c = self.command()
        self.assertFalse(bridge.eligible(c, {'last_seq': 0, 'tasks': {'smoke-1': 'interrupted_unknown'}}))
        self.assertFalse(bridge.eligible(c, {'last_seq': 2, 'tasks': {}}))
    def test_stop_not_blocked_by_task_dedup(self):
        c = self.command(); c['action'] = 'stop'
        self.assertTrue(bridge.eligible(c, {'last_seq': 0, 'tasks': {'smoke-1': 'claimed'}}))
    def test_atomic_state(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'state.json'
            bridge.save(p, {'active': 'smoke-1'})
            bridge.save(p, {'active': None})
            self.assertIsNone(json.loads(p.read_text())['active'])
    def test_worker_sdk_contract_offline(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'openai_codex.py').write_text('''import os
class Sandbox:
    read_only = "read_only"
    workspace_write = "workspace_write"
class Codex:
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def thread_start(self, **kwargs):
        assert kwargs["sandbox"] == "read_only"
        assert "APM_GITHUB_TOKEN" not in os.environ
        return self
    def run(self, prompt):
        assert "read only test" in prompt
        class Result: final_response = "offline mock: passed"
        return Result()
''', encoding='utf-8')
            job = {'workspace': d, 'write_enabled': False, 'prompt': 'read only test', 'result_path': str(root / 'result.json')}
            bridge.save(root / 'job.json', job)
            env = dict(os.environ, PYTHONPATH=d, APM_GITHUB_TOKEN='secret-fixture')
            p = subprocess.run([sys.executable, str(Path(bridge.__file__).resolve()), '--worker', str(root / 'job.json')], env=env, capture_output=True, timeout=10)
            self.assertEqual(p.returncode, 0, p.stderr.decode())
            self.assertEqual(json.loads((root / 'result.json').read_text())['report'], 'offline mock: passed')
    def test_redaction(self):
        self.assertNotIn('secret-fixture', bridge.redact('secret-fixture sk-abc123 ghp_test', 'secret-fixture'))
        self.assertNotIn('sk-abc123', bridge.redact('sk-abc123', ''))
    @unittest.skipIf(os.name == 'nt', 'Windows tree termination requires local validation')
    def test_stop_process(self):
        p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], start_new_session=True)
        bridge.terminate_tree(p)
        self.assertIsNotNone(p.poll())
if __name__ == '__main__': unittest.main()
