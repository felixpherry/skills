#!/usr/bin/env python3
"""Add a MySQL connection to vim-dadbod-ui. Tests the login first; saves nothing if it fails."""
import argparse, json, os, re, shutil, socket, subprocess, sys, urllib.parse
from pathlib import Path

CONN = Path.home() / '.local/share/nvim/dadbod_ui/connections.json'
SSH_CONFIG = Path.home() / '.ssh/config'
KEYS = Path.home() / '.ssh'  # bastion keys live with the other SSH keys, never in the skills folder
TUNNEL_SECONDS = 15  # the test tunnel only has to outlive one login check

p = argparse.ArgumentParser()
p.add_argument('name', help='label shown in DBUI')
p.add_argument('host', help='MySQL host, e.g. mydb.abc123xyz.ap-southeast-1.rds.amazonaws.com')
p.add_argument('--port', default='3306')
p.add_argument('--env', default='.env', help='file with USERNAME= and PASSWORD=')
p.add_argument('--bastion', help='ssh Host alias to tunnel through; omit to connect directly')
p.add_argument('--ssh-host', help='bastion IP, only when the alias is not in ~/.ssh/config yet')
p.add_argument('--ssh-user', default='ec2-user')
p.add_argument('--pem', help='bastion key file, moved into ~/.ssh; only when the alias is not in ~/.ssh/config yet')
a = p.parse_args()

env_file = Path(a.env)
if not env_file.exists():
    sys.exit(f'{env_file} not found: pass --env with a file holding USERNAME= and PASSWORD=')
env = dict(l.rstrip('\n').split('=', 1) for l in env_file.open() if '=' in l)
missing = [k for k in ('USERNAME', 'PASSWORD') if not env.get(k)]
if missing:
    sys.exit(f'{env_file} has no {" or ".join(missing)}= line')
user, pw = env['USERNAME'], env['PASSWORD']

conns = json.loads(CONN.read_text()) if CONN.exists() else []
if any(c['name'] == a.name for c in conns):
    sys.exit(f'"{a.name}" already exists in {CONN}')

ssh_config = SSH_CONFIG.read_text() if SSH_CONFIG.exists() else ''
new_bastion = a.bastion and not re.search(rf'^Host {re.escape(a.bastion)}$', ssh_config, re.M)
if new_bastion:
    if not (a.ssh_host and a.pem):
        sys.exit(f'{a.bastion} is not in {SSH_CONFIG}: pass --ssh-host and --pem')
    key = KEYS / Path(a.pem).name
    if key.exists() and key.read_bytes() != Path(a.pem).read_bytes():
        sys.exit(f'{key} already exists with different contents')
    os.chmod(a.pem, 0o600)  # ssh refuses keys others can read
    ssh_target = ['-i', a.pem, '-o', 'IdentitiesOnly=yes', f'{a.ssh_user}@{a.ssh_host}']
else:
    ssh_target = [a.bastion]

# Test the login, through a short-lived tunnel when there is a bastion.
host, port = a.host, a.port
if a.bastion:
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        host, port = '127.0.0.1', str(s.getsockname()[1])
    subprocess.run(['ssh', '-f', '-o', 'ExitOnForwardFailure=yes', '-o', 'StrictHostKeyChecking=accept-new',
                    '-L', f'{port}:{a.host}:{a.port}', *ssh_target, 'sleep', str(TUNNEL_SECONDS)], check=True)
r = subprocess.run(['mysql', '-h', host, '-P', port, '-u', user, '-e', 'select current_user()'],
                   env={**os.environ, 'MYSQL_PWD': pw}, capture_output=True, text=True)
if r.returncode:
    sys.exit(f'login failed, nothing saved:\n{r.stderr}')
print('login ok:', r.stdout.split()[-1])

if new_bastion:
    KEYS.mkdir(mode=0o700, exist_ok=True)
    if Path(a.pem).resolve() != key.resolve():
        shutil.move(a.pem, key)
    key.chmod(0o600)
    with SSH_CONFIG.open('a') as f:
        f.write(f'\nHost {a.bastion}\n  HostName {a.ssh_host}\n  User {a.ssh_user}\n'
                f'  IdentityFile {key}\n  IdentitiesOnly yes\n  ServerAliveInterval 60\n')
    print(f'added {a.bastion} to {SSH_CONFIG}')

q = lambda s: urllib.parse.quote(s, safe='')
url = f'mysql://{q(user)}:{q(pw)}@{a.host}:{a.port}/'
if a.bastion:
    url = f'ssh://{a.bastion}:{url}'
if CONN.exists():
    shutil.copy(CONN, CONN.with_suffix('.json.bak'))
conns.append({'name': a.name, 'url': url})
CONN.write_text(json.dumps(conns))
print(f'added "{a.name}" to DBUI; reopen DBUI to see it')
