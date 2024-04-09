# Solax Solar Inverter Data Interpretation Tool and Simulator

This tool provides functionalities for interpreting data recorded from Solax solar 
inverters and simulating data via an HTTP server. It allows for comparing data sets
obtained through curl commands or exported datasets from the Solax cloud, including
manual copying of HTML tables to Excel. The tool works optimally when comparing data
recorded for a whole 24-hour day (from 0:00 to 0:00 or longer).

## Installation

### Setting Up Python Virtual Environment

For Ubuntu:

```bash

# Install Python3 and virtualenv
sudo apt update
sudo apt install python3 python3-venv

# Navigate to your project directory
cd /path/to/your/project

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

For Arch Linux:

```bash

# Install Python3 and virtualenv
sudo pacman -Sy python python-pip
sudo pip install virtualenv

# Navigate to your project directory
cd /path/to/your/project

# Create a virtual environment
python -m venv env

# Activate the virtual environment
source env/bin/activate
```

### Installing Requirements

Once inside your virtual environment, install the required dependencies using pip:

```bash

pip install -r requirements.txt
```

## Usage

### Data Interpretation Module

The main.py file contains the interpreter module. You can customize the comparison 
by modifying this file directly. The interpreter can compare results by interpolating
the data to the timestamps and calculate correlation coefficients. Additionally, it
can plot the data using Matplotlib for visual comparison.

### Data Simulator via HTTP Server

The server.py file starts an HTTP server using Klein to playback simulated data based
on recorded timestamps. This allows for development even when the inverter is out of
reach or during other times. You can edit the now variable to select the desired data
time. The server starts on port 8080, and any customizations must be done in the code.
Contributing

Contributions to this project are welcome. Feel free to open issues or pull requests
to suggest improvements or report bugs.

## License

This project is licensed under the MIT License.
