#!/usr/bin/env bash
set -o errexit

pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
pip install --no-cache-dir -r requirements.txt
