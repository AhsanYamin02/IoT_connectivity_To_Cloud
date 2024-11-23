# IoT_connectivity_To_Cloud
Python script to handle AT command communication with IoT devices and cloud
# AT Command Handler

This Python script communicates with devices using AT commands via a serial interface. It organizes commands into blocks and automates retries for robust communication.

## Features
- Send AT commands and process responses.
- Retry mechanism for failed commands.
- Log responses to a file for debugging.
- Organize commands into blocks for modular execution.

## Usage
- Requires Python 3.x and the `pyserial` library.

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/yourusername/at_command_handler.git
cd at_command_handler
pip install pyserial
