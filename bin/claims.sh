#!/usr/bin/env bash

cd $(pwd)/$(dirname $0)
cd ../data

wesovilabs_tf_samples claims \
    --train_data=car_insurance.csv \
    --test_data=car_insurance.csv