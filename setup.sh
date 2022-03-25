#!/usr/bin/env bash

python3 -m venv venv

source venv/bin/activate

apt-get install python3-tk python3-dev

pip3 install -r requirements.txt