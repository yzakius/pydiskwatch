#!/usr/bin/env python3

import os
import subprocess

from dotenv import load_dotenv as env

env()


hosts = os.getenv("HOSTS", "").split(",")


def process_output(output: list) -> None:
    """Process the output of the df -h command and return the disk usage of the root partition."""
    for line in output:
        splited_line = line.split()
        if "/" in splited_line:
            return splited_line[4]


def get_disk_space_from_host_list(hosts):
    for host in hosts:
        """Get disk usage from a list of hosts by running df -h on each host."""
        output = subprocess.check_output(
            ["ssh", host, "df -h"],
            text=True
        ).strip().split("\n")
        disk_space = process_output(output)
        print(host, disk_space)

if __name__ == "__main__":
    get_disk_space_from_host_list(hosts)
