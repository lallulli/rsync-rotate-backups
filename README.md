# rsync-rotate-backups
Combine rsync, cp -al and rotate-backups in a single script

This script, installed on a backup server, will connect to clients using rsync, incrementally backup clients, and maintain latest backups according to a custom policy, managed by rotate-backups.

Versioned backups will share unmodified files thanks to hard links

## How to setup (notes... to be expanded!)

On backup server:

1. Download script
2. Install requirements
3. Generate an ssh key: `ssh-keygen`
4. Send the public ssh key to each client: `ssh-copy-id <user>@<client_name>`
5. Setup `config.json`
6. Test: `python3 rsync_rotate_backups.py`
7. Add to crontab e.g. a daily backup job: `20 3 * * * cd /my_user/rsync-rotate-backups && /usr/bin/python3 rsync_rotate_backups.py`
