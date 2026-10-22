---
name: read-db
description: Run read-only SELECT or SHOW queries on an existing beta staging MySQL connection in DBUI. Use when investigating staging data, counting rows, or checking staging table schemas without asking the user to relay DBUI results.
---

# Read a staging database

Use the existing DBUI connection. Do not add a connection or copy credentials into chat. This skill accepts only beta staging MySQL connections through a beta bastion. Do not use it for production; current team rules prohibit production database access.

1. Find the exact staging connection name in `~/.local/share/nvim/dadbod_ui/connections.json`. Check its host and bastion before querying. Do not print its URL or password.
2. Install the driver once with `python3 -m pip install --user PyMySQL` if missing.
3. Send a single `SELECT` or `SHOW` query on standard input to `python3 ~/.agents/skills/read-db/query.py <connection-name>`. Example:

   ```sh
   printf 'SELECT 1 AS ok\n' | python3 ~/.agents/skills/read-db/query.py service-set-beta
   ```

The runner starts its own SSH tunnel, executes one query inside a read-only transaction, requests a 30-second server limit for `SELECT`, prints at most 100 rows, then closes the connection and tunnel. The driver does not enable multiple SQL statements. Keep reads narrow: use `LIMIT` for row samples. If the bastion cannot connect, ask the user to check VPN. If a table is not granted, name the schema and table and ask for access. Never run SQL that writes, including `SELECT ... INTO OUTFILE` or calls to functions with side effects, even if the login has write grants.
