---
name: add-db-connection
description: Add a MySQL database to vim-dadbod-ui (DBUI) in Neovim, optionally tunneled through an SSH bastion. Use when the user says "setup this db in DBUI", pastes a mysql command or RDS host to add, or shares bastion details (IP, user, key file) for a new DB.
---

# Add a DB to DBUI

DBUI keeps its connections in `~/.local/share/nvim/dadbod_ui/connections.json`.
Tunneled entries look like `ssh://<ssh alias>:mysql://user:pass@<rds host>:<port>/`, and the vim-dadbod-ssh plugin opens the tunnel.
`add.py` (next to this file) tests the login through a tunnel, then saves. If the login fails, it saves nothing.

## Steps

1. **Collect the inputs** from the user's message, mysql command, or screenshot:
   - **Name**: what shows in DBUI. Default to the first part of the host.
   - **Host and port**: from the pasted command. Pass `--port` unless it's 3306.
   - **Credentials**: a `.env` file with `USERNAME=` and `PASSWORD=`. Look in the current directory first. If there isn't one, ask. Use the `.env` login even if the pasted command names a different user. Never print the password.
   - **Bastion**: match the bastion IP to an existing alias with `grep -B1 'HostName <ip>' ~/.ssh/config`. Its key is already set there.
   - **New bastion**: pick an alias and pass `--ssh-host <ip> --pem <path>`. Ask the user where the key file is. The script moves it into `~/.ssh` and adds the alias to `~/.ssh/config`, pointing at the moved key.
2. **Run the script:**
   ```
   python3 -I ~/.claude/skills/add-db-connection/add.py <name> <host> --port <port> --bastion <alias> --env <path/to/.env>
   ```
   Leave out `--bastion` for a DB that connects directly, without a tunnel.
3. **Tell the user to reopen DBUI**, or restart Neovim, to see the new entry. The previous list is saved as `connections.json.bak`.

## Notes

- **Leave out SSL flags** like `--ssl-mode=VERIFY_IDENTITY --ssl-ca=global-bundle.pem`. The tunnel connects to 127.0.0.1, so the certificate check can't match the host name.
- **If the login fails because the server requires SSL,** the script can't handle that yet. Add `?ssl-mode=REQUIRED` to the end of the saved URL. DBUI passes it to mysql as `--ssl-mode=REQUIRED`.
- **All bastion keys live in `~/.ssh`.** `~/.ssh/config` points there. Don't move them or the tunnels break. Never put a key in the skills folder: every agent and tool that reads skills can see it.
- **The name must be new.** The script refuses a duplicate. To replace an entry, delete it from the JSON file first.
