#!/bin/bash

# python3 scripts/download_transactions.py
# if [ $? -ne 0 ]; then
#   echo "Error: download_transactions.py failed to execute."
#   exit 1
# fi

python3 scripts/clean.py
if [ $? -ne 0 ]; then
  echo "Error: clean.py failed to execute."
  exit 1
fi

echo "Both scripts executed successfully."