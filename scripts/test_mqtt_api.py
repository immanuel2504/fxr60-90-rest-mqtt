#!/usr/bin/env python3
"""Moved to test script/test_mqtt_api.py. This file keeps old commands working."""
import os
import subprocess
import sys

_TARGET = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "test script", "test_mqtt_api.py",
))
raise SystemExit(subprocess.call([sys.executable, _TARGET, *sys.argv[1:]]))
