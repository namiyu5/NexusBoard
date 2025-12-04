"""Build the Vue frontend and deploy into Django staticfiles.

Usage (Windows PowerShell):
  .venv\Scripts\activate
  python scripts\deploy_frontend.py

What it does:
- runs `npm run build` inside `nexusboard_vue`
- copies `nexusboard_vue/dist/*` into `nexus_board/staticfiles/nexusboard_vue/`
- runs `python scripts/update_django_template.py` to inject hashed asset names into
  `nexus_board/templates/nexus_board/index.html`
- reminds you to run `python manage.py collectstatic --noinput` if not running automatically

Note: run this script from the repository root. Ensure `npm` is installed and available on PATH.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / 'nexusboard_vue'
DIST_DIR = FRONTEND_DIR / 'dist'
TARGET_STATIC_DIR = ROOT / 'nexus_board' / 'staticfiles' / 'nexusboard_vue'
UPDATE_SCRIPT = ROOT / 'scripts' / 'update_django_template.py'


def run(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)} (cwd={cwd})")
    res = subprocess.run(cmd, cwd=cwd, shell=False)
    if res.returncode != 0:
        print(f"Command failed with exit code {res.returncode}: {cmd}")
        sys.exit(res.returncode)


def build_frontend():
    if not FRONTEND_DIR.exists():
        print('Error: frontend folder not found at', FRONTEND_DIR)
        sys.exit(1)
    # Locate npm (allow override with NPM_CMD env var)
    npm_cmd = os.environ.get('NPM_CMD') or shutil.which('npm')
    if not npm_cmd:
        print('\nError: `npm` not found on PATH.')
        print('Please install Node.js and npm: https://nodejs.org/')
        print('Verify npm is on your PATH: `npm --version` or `where.exe npm`')
        print('Or set env var `NPM_CMD` to the full path to npm and re-run.')
        sys.exit(1)

    # Install deps (optional) and build
    print('Installing frontend dependencies (npm install)')
    run([npm_cmd, 'install'], cwd=str(FRONTEND_DIR))
    print('Building frontend (npm run build)')
    run([npm_cmd, 'run', 'build'], cwd=str(FRONTEND_DIR))


def copy_dist_to_django():
    if not DIST_DIR.exists():
        print('Error: dist folder not found at', DIST_DIR)
        sys.exit(1)
    TARGET_STATIC_DIR.mkdir(parents=True, exist_ok=True)
    print(f'Copying {DIST_DIR} -> {TARGET_STATIC_DIR}')
    # remove existing files in target to avoid stale assets
    for child in TARGET_STATIC_DIR.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    # copy all files
    for item in DIST_DIR.iterdir():
        dest = TARGET_STATIC_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)


def inject_template():
    if not UPDATE_SCRIPT.exists():
        print('Warning: update script not found at', UPDATE_SCRIPT)
        return
    print('Updating Django template with built asset names')
    run([sys.executable, str(UPDATE_SCRIPT)], cwd=str(ROOT))


if __name__ == '__main__':
    build_frontend()
    copy_dist_to_django()
    inject_template()
    print('\nFrontend build deployed to Django staticfiles.')
    print('Next: run `python manage.py collectstatic --noinput`.')
