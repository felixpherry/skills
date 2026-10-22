#!/usr/bin/env python3
import argparse
import csv
import json
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pymysql

parser = argparse.ArgumentParser(description='Read from a staging DBUI MySQL connection')
parser.add_argument('connection', help='exact DBUI connection name')
args = parser.parse_args()

sql = sys.stdin.read().strip()
if not re.match(r'^(SELECT|SHOW)\b', sql, re.IGNORECASE) or re.search(r'\bINTO\b', sql, re.IGNORECASE):
    parser.error('only SELECT and SHOW queries without INTO are supported')

connections = json.loads((Path.home() / '.local/share/nvim/dadbod_ui/connections.json').read_text())
matched = [entry for entry in connections if entry['name'] == args.connection]
if len(matched) != 1:
    parser.error('expected exactly one DBUI connection with that name')

url = matched[0]['url']
if not url.startswith('ssh://'):
    parser.error('only staging connections through a beta bastion are supported')
bastion, mysql_url = url[6:].split(':', 1)
mysql = urlsplit(mysql_url)
if (not bastion.endswith('-beta-bastion') or mysql.scheme != 'mysql'
        or not mysql.hostname or not mysql.hostname.split('.')[0].endswith('-beta')
        or not mysql.username or mysql.password is None):
    parser.error('connection is not a beta staging MySQL connection')

with socket.socket() as sock:
    sock.bind(('127.0.0.1', 0))
    local_port = sock.getsockname()[1]

ssh = subprocess.Popen(
    ['ssh', '-N', '-o', 'BatchMode=yes', '-o', 'ExitOnForwardFailure=yes',
     '-o', 'StrictHostKeyChecking=yes', '-L',
     f'127.0.0.1:{local_port}:{mysql.hostname}:{mysql.port or 3306}', bastion],
    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
try:
    for _ in range(100):
        if ssh.poll() is not None:
            parser.error('staging SSH tunnel failed; check bastion access or VPN')
        try:
            with socket.create_connection(('127.0.0.1', local_port), timeout=0.2):
                break
        except OSError:
            time.sleep(0.1)
    else:
        parser.error('staging SSH tunnel timed out; check bastion access or VPN')

    with pymysql.connect(
        host='127.0.0.1', port=local_port,
        user=unquote(mysql.username), password=unquote(mysql.password),
        database=unquote(mysql.path.lstrip('/')) or None,
        connect_timeout=10, read_timeout=35, write_timeout=10,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SET SESSION MAX_EXECUTION_TIME=30000')
            cursor.execute('SET SESSION TRANSACTION READ ONLY')
            cursor.execute('START TRANSACTION READ ONLY')
            cursor.execute(sql)
            writer = csv.writer(sys.stdout)
            writer.writerow([column[0] for column in cursor.description])
            for row in cursor.fetchmany(100):
                writer.writerow(row)
            if cursor.rowcount > 100:
                print('Output limited to 100 rows', file=sys.stderr)
except pymysql.MySQLError as exc:
    sys.exit(f'Query failed: {exc}')
finally:
    ssh.terminate()
    ssh.wait()
