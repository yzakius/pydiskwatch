# pydiskwatch
A Python-based CLI tool to monitor disk usage across multiple remote servers via SSH.

I created this tool for learning purposes. I know there are tools out there for monitoring disk usage, but I decided to build my own just for fun.

## Prerequisites
- Python 3.10+
- SSH key-based access (passwordless) configured for all target hosts

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Setup
Create a `.env` file in the project root:
```env
HOSTS=user@server1.com,user@server2.com,192.168.1.50
```

## Usage
```bash
python3 pydiskwatch.py
```

**Example output:**
```
user@server1.com 45%
user@server2.com 82%
192.168.1.50 12%
```
