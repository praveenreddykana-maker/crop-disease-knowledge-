#!/usr/bin/env bash
set -e

python -m pip install --no-cache-dir --upgrade pip setuptools wheel
pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
pip install --no-cache-dir -r requirements.txt
