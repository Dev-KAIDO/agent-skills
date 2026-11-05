# Linux Fundamentals (أساسيات لينكس)

## 1. Processes & Startup

```bash
systemctl start|stop|restart|status myapp
systemctl enable myapp                 # start on boot
journalctl -u myapp -f --since today   # logs, follow
```

- **systemd units** (`/etc/systemd/system/myapp.service`): `Restart=always`, `WantedBy=multi-user.target`, run as non-root user, `EnvironmentFile=` for secrets.
- After editing a unit: `daemon-reload` then `restart`.
- `ps aux --sort=-%mem | head` / `top` — who eats CPU/RAM; `kill -TERM` first (graceful), `-KILL` only after.
- Zombies/`defunct` = parent didn't reap — find parent with `ps -ef`.

## 2. Logs

- journald: `journalctl -u svc -p err` (priority), `--since`, `-f`.
- Files: `/var/log/syslog`, `nginx/error.log` — rotate via `logrotate` (keep size/time bounded, compress).
- App logs to stdout → journald/file via unit config; **no silent logging to random paths**.

## 3. Resources

```bash
df -h /                 # disk full = app crashes (logs!)
du -sh /var/log/* | sort -h | tail
free -h                 # watch available, not "free"
vmstat 1                # si/so (swap pressure), us/sy (CPU)
iostat -x 1             # await/%util — IO bottleneck
ss -ltnp                # listening ports + owning process
```

| Symptom | First look |
|---------|------------|
| Load high but CPU idle | IO wait (`wa` in top) or more runnable tasks than cores |
| Random restarts | OOM killer: `dmesg -T \| grep -i oom` |
| App slow, resources fine | upstream (DB/network) — check trace ids |
| Disk at 100% | logs or data growth: `du` top-down |

## 4. Permissions

- `-rwxr-xr--` = owner/group/other; `chmod 750 dir` for shared-but-restricted.
- Directories: `x` = can enter/traverse. A missing `x` on a parent blocks everything below.
- Secrets: mode `600`, owned by the service user, injected via env/`EnvironmentFile` — never world-readable, never in git.
- Ownership: service runs as its own user (`www-data`, `myapp`), **not root**.

## 5. SSH

```bash
ssh-copy-id user@host            # key-based auth
# /etc/ssh/sshd_config: PasswordAuthentication no, PermitRootLogin no
```

- Keys with passphrases + agent; disable password auth (kills brute-force noise).
- Bastion/jump host or port-forward for DB access instead of exposing 5432.

## 6. Safe Operations

- Config changes: back up the file first, test with a dry-run where supported (`nginx -t`), reload (not restart) when possible.
- Reboots: check `systemctl list-unit-files --state=enabled` for what will come back; verify after boot.
- Packages: pin versions on servers; `apt update && apt upgrade` on a schedule, not mid-incident.
- Everything ad-hoc in an incident → written into a runbook afterward (or it stays tribal knowledge).
