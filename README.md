alfred-alarmcom
====================

Alfred Workflow for Alarm.com

This project uses selenium (not included), keychain.py, phantomjs and pyalarmdotcom - those files that are included and are governed by their respective licenses. The pyalarmdotcom was modified slightly to accomodate python2. phantomjs is used as is. keychain.py was modified slightly to add to error reporting.

README for Alarm.com

To use:

Step 1:
Install the Alarm.com Alfred workflow

Step 2:
open Alfred and 

```bash
alrm_update <username> <password>
```

To arm in stay mode:

```bash
arm stay
```

To arm in away mode:

```bash
arm away
```

To disarm:

```bash
arm off
```
