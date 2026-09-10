"""One maintenance command: validate data, render pages, and sync URL metadata."""
from pathlib import Path
import subprocess
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
flags = ['--check'] if '--check' in sys.argv else []
if 'GA4_MEASUREMENT_ID' in os.environ and not flags:
    subprocess.run(['node', str(ROOT / 'scripts/build-analytics.cjs')], cwd=ROOT, check=True)
for script in ('build-trust.py', 'build-article-cluster.py', 'build-home.py', 'build-locales.py', 'sync-layout.py', 'sync-routing.py'):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / script), *flags], cwd=ROOT, check=True)
