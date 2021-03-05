import json
import requests
import time
import os
import subprocess
from utils import deObfuscate as d

with open('config.json', 'r') as f:
    config = json.load(f)

# VARIABLE                            # TYPE (DEFAULT) : <DESCRIPTION>. 
MYADDRESS    = d(config["MYADDRESS"]) # STR  (None)    : Base64 encoded Public eth/bsc address.
APIKEY       = d(config["APIKEY"])    # STR  (None)    : Base64 encoded bscScan.com API key.
