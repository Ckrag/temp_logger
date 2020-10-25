#!/usr/bin/python3

import log
import time
import sys

_LOG_INTERVAL_SEC = 60
_POST_ADR = None
_AUTH = None

# Run
if len(sys.argv) > 1:
    _LOG_INTERVAL_SEC = int(sys.argv[1])

if len(sys.argv) > 2:
    _POST_ADR = sys.argv[2]

if len(sys.argv) > 4:
    _AUTH = (sys.argv[3], sys.argv[4])

log = log.Log()

print("Logging started")
print("Log interval: {}".format(_LOG_INTERVAL_SEC))

while True:
    print(str(log._get_timestamp()) + " - testing ..")
    log.log(dms=_POST_ADR, auth=_AUTH)
    time.sleep(_LOG_INTERVAL_SEC)