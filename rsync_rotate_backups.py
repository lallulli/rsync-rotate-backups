from datetime import datetime
import subprocess
import rotate_backups
import json
import sys
import os


def create_dir_if_not_existing(path, recurse=False):
	path = os.path.abspath(path)
	if not os.path.exists(path):
		parent, sub = os.path.split(path)
		if recurse and not os.path.exists(parent):
			create_dir_if_not_existing(parent, recurse)
		os.mkdir(path)


def backup(src, dst, rotation_scheme=None, exclude=None):
	"""
	Backup and rotate from a source to a destination directory

	In the destination directory dst the following subdirectories will be created:
	- latest: it contains the latest backup
	- YYYY-MM-DD HH:MM:SS: versioned backups

	Versioned backups will be automatically rotated using rotate-backups

	:param src: Source directory, possibly on remote server, using rsync format
	:param dst: Destination directory
	"""
	dst_latest = os.path.join(dst, "latest")
	dst_ts = os.path.join(dst, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	create_dir_if_not_existing(dst, True)
	rsync_cmd = [
		"rsync",
		"--del",
		"-avzhe",
		"ssh",
	]
	if exclude is not None:
		for e in exclude:
			rsync_cmd += [
				"--exclude",
				e,
			]
	rsync_cmd += [
		src,
		dst_latest,
	]
	subprocess.call(rsync_cmd)

	cp_cmd = [
		"cp",
		"-al",
		dst_latest,
		dst_ts,
	]
	subprocess.call(cp_cmd)

	if rotation_scheme is None:
		rotation_scheme = {
			'daily': 2,
			'weekly': 2,
			'monthly': 2,
		}
	rb = rotate_backups.RotateBackups(rotation_scheme)
	# rb.dry_run = True
	rb.rotate_concurrent(dst)


def backup_all(config_file):
	with open(config_file) as f:
		config = json.load(f)
	rs = config.get("rotation_scheme")
	for c in config['backups']:
		exclude = c.get('exclude')
		backup(c['src'], c['dst'], rs, exclude)


if __name__ == '__main__':
	if len(sys.argv) == 2:
		backup_all(sys.argv[1])
	else:
		backup_all("config.json")

