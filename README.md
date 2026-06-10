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
```shell
cp contrib-env .env
```

And 

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

## Data Storage

The tool automatically saves disk usage history to a **`history_disc_usage.json`** file in the project root. This file accumulates data over time, allowing you to track disk usage trends across your servers.

**File structure example:**
```json
{
  "server1": [
    {
      "datetime": "2026-06-10",
      "usage": "49%"
    },
    {
      "datetime": "2026-06-11",
      "usage": "49%"
    }
  ],
  "server2": [
    {
      "datetime": "2026-06-10",
      "usage": "52%"
    },
    {
      "datetime": "2026-06-11",
      "usage": "52%"
    }
  ]
}
```
