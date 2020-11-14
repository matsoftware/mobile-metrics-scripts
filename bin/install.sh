#!/bin/bash

set -e

top=$(dirname $0)
python3 -m venv ${top}/venv

# It installs the common dependencies for the python scripts

${top}/venv/bin/python3 ${top}/venv/bin/pip3 install -r ${top}/requirements.txt

# Installs the sample app dependencies (assuming that CocoaPods is installed)
cd ./test/CarbonIntensityUKDemo/CarbonIntensityUKDemo && pod install