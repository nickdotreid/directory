#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	if 'DJANGO_DIR' in os.environ:
		sys.path.insert(0, os.path.join(os.environ['DJANGO_DIR'],"directory"))
	else:
		sys.path.insert(0, os.path.join(os.getcwd(),"directory"))

	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
