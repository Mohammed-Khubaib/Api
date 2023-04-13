#!/bin/bash

apt-get update

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt