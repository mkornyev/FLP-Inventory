#!/usr/bin/env python
import time
import os

SECONDS_PER_WEEK = 604800
while True:
    os.system("python manage.py db_backup 'center@fosterloveproject.org'")
    time.sleep(SECONDS_PER_WEEK)