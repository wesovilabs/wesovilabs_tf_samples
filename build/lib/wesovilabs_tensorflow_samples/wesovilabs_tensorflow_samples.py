"""Wesovilabs Tensorflow Samples.

Usage:
  wesovilabs_tf_samples [JOB] [options]
  wesovilabs_tf_samples ( -h | --help )
  wesovilabs_tf_samples ( -v | --version )
  wesovilabs_tf_samples ( --list )

Arguments:
    JOB     job name

Options:
    --train_data=V                     Path to the training data.
    --test_data=V                     Path to the test data.
"""
from docopt import docopt
from sys import argv
from .claims import main as claims_main

def main():
    arguments = docopt(__doc__, version='Wesovilabs Tensorflow Samples 0.0.1')
    print(arguments)
    if arguments['--list']:
        print('\n Available samples\n -----------------\n')
        print(' - carinsurance_claimnsnumber: This job will allow us to know if a new client wil claim or not in the first year')
        print('     Usage: \'wesovilabs_tf_samples claims <options>\'')
        print('\n\n')
    elif arguments['JOB']=='claims':
        claims_main(arguments)
    else:
        print(arguments)



if __name__ == "__main__":
    arguments = docopt(__doc__, version='Wesovilabs Tensorflow Samples 0.0.1')
    print(argv)
    main(arguments)
