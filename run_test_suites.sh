#!/bin/bash

cd "$(dirname $0)"

export PYTHONPATH=$PYTHONPATH:$(pwd)/mozilla

python -m unittest discover mozilla/test
