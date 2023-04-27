README.md

To install:

Install Python 3

Must have python 3.9.2 or higher

```
python --version
Python 3.9.2
```

Must also have python3-dev in order for `psutils` to install.

```
sudo apt install python3 python3-dev python3-venv

```

Install audio components:

```
sudo apt install pulseaudio pulseaudio-module-zeroconf alsa-utils avahi-daemon pulsemixer
```

Clone this repo, then `cd` into the clone directory and create, then activate a virtual environment, and install dependencies.

```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

Start pulseaduio: `pulseaudio -D`

Serve the site:

`flask run`

Serve the site from a specific IP:

By default flask serves at loopback. To define a public IP, run with `--host`.

Example: `flask run --host=192.168.0.73`

Seve the site with a specific IP and port:

Example: `flask run --host=192.168.0.73 --port=8000`

