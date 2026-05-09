#!/usr/bin/env python3

import json
import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv as env

env()

hosts = [h for h in os.getenv("HOSTS", "").split(",") if h]


def process_output(output: list) -> list | None:
    """Process the output of the df -h command and return the disk usage of the root partition."""
    for line in output:
        splited_line = line.split()
        if "/" in splited_line:
            return splited_line[4]


def get_disk_space_from_host_list(hosts):
    """Get disk usage from a list of hosts by running df -h on each host."""
    result = {}
    timestamp = datetime.now().strftime("%Y-%m-%d")
    for host in hosts:
        output = subprocess.check_output(
            ["ssh", host, "df -h"],
            text=True
        ).strip().split("\n")
        disk_space = process_output(output)
        #print(host, disk_space)
        result.update({host: [
            {
                "datetime": timestamp,
                "usage": disk_space
            }
        ]})
    return result

def save_data(data):
    filename = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists("history_disc_usage.json"):
        with open("history_disc_usage.json", "r") as f:
            history = json.load(f)
    else:
        history = {}
    for host_name, host_usage_data in data.items():
        if host_name not in history:
            history[host_name] = []
        history[host_name].extend(host_usage_data)
    with open("history_disc_usage.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # TODO: Rodar e testar se acumulou, se sim:
        # TODO: colocar na doc

if __name__ == "__main__":
    result = get_disk_space_from_host_list(hosts)
    save_data(data=result)
