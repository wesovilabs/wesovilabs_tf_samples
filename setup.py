import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
<<<<<<< HEAD
    name = "wesovilabs_tensorflow_samples",
=======
    name = "wesovilabs_tf_samples",
>>>>>>> master
    version = "0.0.1",
    author = "Iván Corrales Solera",
    author_email = "developer@wesovilabs.com",
    description = ("Samples of how to use tensorflow in a real environment."),
    license = "MIT",
    keywords = "tensorflow neuronal network",
<<<<<<< HEAD
    url = "http://packages.python.org/wesovilabs_tensorflow_samples",
    packages=['wesovilabs_tensorflow_samples', 'tests'],
=======
    url = "http://packages.python.org/wesovilabs_tf_samples",
    packages=['wesovilabs_tf_samples', 'tests'],
>>>>>>> master
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Tutorials",
        "License :: MIT License",
    ],
    entry_points = {
        'console_scripts': [
<<<<<<< HEAD
            'wesovilabs_tf_samples = wesovilabs_tensorflow_samples.wesovilabs_tensorflow_samples:main',
=======
            'wesovilabs_tf_samples = wesovilabs_tf_samples.wesovilabs_tf_samples:main',
>>>>>>> master
        ]
    }

)