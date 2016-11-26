import pandas as pd
import tensorflow as tf
import tempfile
from six.moves import urllib

COLUMNS = ["age", "city", "state","country", "zip", "years_of_driving_license"]


flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string( "model_dir",   "",   "Base directory for output models.")
flags.DEFINE_string( "model_type",  "",  "Valid model types: {'wide', 'deep', 'wide_n_deep'}.")
flags.DEFINE_string( "train_data",  "",  "Path to the training data.")
flags.DEFINE_string( "test_data",   "",   "Path to the test data.")

def _prepare_date():
    return "/Users/Ivan/Sandbox/WesoviLabs/wesovilabs_tensorflow_samples/data/car_insurance.csv", "/Users/Ivan/Sandbox/WesoviLabs/wesovilabs_tensorflow_samples/data/car_insurance.csv"


def _download_resource(url):
    file = tempfile.NamedTemporaryFile(delete=False)
    urllib.request.urlretrieve(
        url,
        file.name
    )
    filename = file.name
    file.close()
    return filename


def _download_data():
    if FLAGS.train_data:
        train_file_name = FLAGS.train_data
    else:
        train_file_name = _download_resource("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data")
        print("Training data is downloaded to %s" % train_file_name)

    if FLAGS.test_data:
        test_file_name = FLAGS.test_data
    else:
        test_file_name = _download_resource(
            "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test")
        print("Testing data is downloaded to %s" % test_file_name)
    return train_file_name, test_file_name


def main(_):
    train_file_name, test_file_name = _download_data()
    df_train = pd.read_csv(
        tf.gfile.Open(train_file_name),
        names=COLUMNS,
        skipinitialspace=True,
        sep = ',',
        header = 0,
        engine="python")

    print(df_train.get_values())

    df_train = df_train.dropna(how='any', axis=0)

    print(df_train.get_values())

if __name__ == "__main__":

  tf.app.run()