#!/usr/bin/env python3

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
        print(host, disk_space)
        result.update({host: [
            {
                "datetime": timestamp,
                "usage": disk_space
            }
        ]})
    return result

def save_data(data):
    # TODO: salvar em um arquivo json
    # TODO: fazer com que o json seja atualizado
    # TODO: colocar na doc
    print(data)

if __name__ == "__main__":
    result = get_disk_space_from_host_list(hosts)
    save_data(data=result)
