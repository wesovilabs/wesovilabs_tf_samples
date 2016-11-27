#!/bin/bash

cd $(pwd)/$(dirname $0)
cd ..
python setup.py install
exit;