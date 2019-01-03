# LinuxGamePanel
Python web interface for Linux Game Server Manager 

![preview](http://cdn.aussiehostingservices.com/b07d1d05-c687-4115-9c2c-4abd22acf068.png)

# Installation
1. Download the latest source from GitHub
2. Extract ZIP file into the root level of your game server (Where you downloaded and installed LGSM)
3. Install Python 3.X (Check online for instructions for your distubution)
4. Install requirements via `pip` (`pip3` on some systems)
```BASH
pip install flask ansi2html python-pam
```

# Configuration
To configure the panel edit `lgpl.json` at the most basic level you only need to provide the lgsm script name such as `rustserver`

## Multiple Servers
If you are using multiple servers under a single user you can add them all to a single instance of the web panel like this
```JSON
"servers": [
    "csgoserver",
    "csgoserver2",
    "csgoserver3",
]
```

# Startup
Simply run `./start_web_panel.sh` this will ensure the log/web exists and then run the server using nohup allowing you to disconnect from the session
