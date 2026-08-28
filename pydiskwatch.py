#!/usr/bin/env python3

import json
import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv as env

env()

hosts = [h for h in os.getenv("HOSTS", "").split(",") if h]
needs_atention = {}


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
        output = (
            subprocess.check_output(["ssh", host, "df -h"], text=True)
            .strip()
            .split("\n")
        )
        disk_space = process_output(output)
        result.update({host: [{"datetime": timestamp, "usage": disk_space}]})
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
        json.dump(history, f, indent=2, ensure_ascii=False)


def print_summary(data):
    """Print hosts grouped by disk usage."""
    print("\nAcima de 80%")
    for host_name, host_usage_data in data.items():
        usage = int(host_usage_data[0]["usage"].replace("%", ""))
        if usage > 80:
            print(f"{host_name} -> {usage}%")

    print("\nAcima de 50%")
    for host_name, host_usage_data in data.items():
        usage = int(host_usage_data[0]["usage"].replace("%", ""))
        if 50 < usage <= 80:
            print(f"{host_name} -> {usage}%")


if __name__ == "__main__":
    result = get_disk_space_from_host_list(hosts)
    save_data(data=result)
    print_summary(data=result)
