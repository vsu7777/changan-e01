"""Run Lemo's tts_zh.py with the Hatch egress proxy + CA bundle.

Why: edge-tts hardcodes its SSL context to certifi's bundle (no Hatch egress CA),
and tts_zh.py does not pass a proxy, so on this VM the Microsoft TTS endpoint
fails twice over (direct connect -> SSL wrong version; via proxy -> cert verify).
This wrapper patches certifi.where to a combined bundle (certifi + Hatch CA)
and injects the proxy from the environment into edge_tts.Communicate, then runs
tts_zh.py unchanged. Usage: .venv/bin/python voice/run_tts.py
"""
import os
import certifi

certifi.where = lambda: '/home/hatch/workspace/lemo-opuscar/films/changan-e01/voice/combined-ca.pem'

import edge_tts

_orig_init = edge_tts.Communicate.__init__


def _patched_init(self, *args, **kwargs):
    kwargs.setdefault('proxy', os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy'))
    return _orig_init(self, *args, **kwargs)


edge_tts.Communicate.__init__ = _patched_init

import runpy
import sys

sys.argv = ['tts_zh.py', 'films/changan-e01/voice/lines.json',
            'films/changan-e01/voice/out', '--voice', 'zh-CN-XiaoxiaoNeural']
runpy.run_path('core/tts/tts_zh.py', run_name='__main__')
