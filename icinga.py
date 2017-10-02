#!/bin/env python3
import sys
import os
from subprocess import call
import requests
from pyyamlconfig import load_config


config = load_config(os.path.expanduser('~/.config/icinga_status.yaml'))

try:
    response = requests.get(
        f'{config.get("url")}/v1/status/CIB',
        auth=(
            config.get('user'),
            config.get('pass'),
        ),
        verify=False,
    )
except:
    call([config.get('traffic'), '-r'])
    sys.exit(1)

results = response.json().get('results', [])[0]
status = results.get('status', {})
hosts_acked = status.get('num_hosts_acknowledged')
hosts_down = status.get('num_hosts_down')
hosts_flapping = status.get('num_hosts_flapping')
hosts_downtime = status.get('num_hosts_in_downtime')
hosts_pending = status.get('num_hosts_pending')
hosts_unreachable = status.get('num_hosts_unreachable')
hosts_up = status.get('num_hosts_up')

hosts_handled = (hosts_acked + hosts_downtime)
hosts_bad_state = (hosts_down + hosts_unreachable)

services_acked = status.get('num_services_acknowledged')
services_crit = status.get('num_services_critical')
services_flapping = status.get('num_services_flapping')
services_downtime = status.get('num_services_in_downtime')
services_ok = status.get('num_services_ok')
services_pending = status.get('num_services_pending')
services_unknown = status.get('num_services_unknown')
services_unreachable = status.get('num_services_unreachable')
services_warn = status.get('num_services_warning')

services_handled = (services_acked + services_downtime)
services_bad_state = (services_warn + services_crit + services_unknown + services_unreachable)

if (services_bad_state > services_handled) or (hosts_bad_state > hosts_handled):
    call([config.get('traffic'), '-r'])
else:
    call([config.get('traffic')])
