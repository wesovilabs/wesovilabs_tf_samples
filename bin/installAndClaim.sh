#!/usr/bin/env bash

cd $(pwd)/$(dirname $0)

sh install.sh
clear
sh claims.sh
