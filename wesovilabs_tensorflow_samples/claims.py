import pandas as pd
import tensorflow as tf
import tempfile
from six.moves import urllib



flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string("model_dir", "", "Base directory for output models.")
flags.DEFINE_string("model_type", "", "Valid model types: {'wide', 'deep', 'wide_n_deep'}.")
flags.DEFINE_string("train_data", "", "Path to the training data.")
flags.DEFINE_string("test_data", "", "Path to the test data.")
flags.DEFINE_integer("train_steps", 4, "Number of training steps.")

COLUMNS = ["firstname","lastname","age", "city", "state", "country", "zip", "years_of_driving_license","claims_per_year"]
CATEGORICAL_COLUMNS = [ "country"]
CONTINUOUS_COLUMNS = [ "age", "years_of_driving_license" ]

LABEL_COLUMN = "label"

def _prepare_date():
    return "/Users/Ivan/Sandbox/WesoviLabs/wesovilabs_tensorflow_samples/data/car_insurance.data", "/Users/Ivan/Sandbox/WesoviLabs/wesovilabs_tensorflow_samples/data/car_insurance.test"


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
        train_file_name = _download_resource(
            "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data")
        print("Training data is downloaded to %s" % train_file_name)

    if FLAGS.test_data:
        test_file_name = FLAGS.test_data
    else:
        test_file_name = _download_resource(
            "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test")
        print("Testing data is downloaded to %s" % test_file_name)
    return train_file_name, test_file_name

def build_estimator(model_dir):
    """Build an estimator."""

    #Categorical base columns
    country = tf.contrib.layers.sparse_column_with_hash_bucket("car", hash_bucket_size=1000)

    #Continuous base columns
    age = tf.contrib.layers.real_valued_column("age")
    years_of_driving_license = tf.contrib.layers.real_valued_column("driving-license-experience")

    # Transformations.
    age_buckets = tf.contrib.layers.bucketized_column(age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])
    years_of_driving_license_buckets = tf.contrib.layers.bucketized_column(age, boundaries=[1, 2, 3, 5, 10, 15, 25])


    wide_columns = [
        country,
        age,
        years_of_driving_license,
        """
        tf.contrib.layers.crossed_column([age, years_of_driving_license], hash_bucket_size=int(1e4)),
        tf.contrib.layers.crossed_column([age, salary], hash_bucket_size=int(1e4)),
        tf.contrib.layers.crossed_column([gender, salary], hash_bucket_size=int(1e6)),
        """
    ]

    deep_columns = [
        country,
        age,
        years_of_driving_license
    ]

    if FLAGS.model_type == "wide":
        m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
                                              feature_columns=wide_columns)
    elif FLAGS.model_type == "deep":
        m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
                                           feature_columns=deep_columns,
                                           hidden_units=[100, 50])
    else:
        m = tf.contrib.learn.DNNLinearCombinedClassifier(
            model_dir=model_dir,
            linear_feature_columns=wide_columns,
            dnn_feature_columns=deep_columns,
            dnn_hidden_units=[100, 50])
    print(m)
    return m

def input_fn(df):
  """Input builder function."""
  # Creates a dictionary mapping from each continuous feature column name (k) to
  # the values of that column stored in a constant Tensor.
  continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
  # Creates a dictionary mapping from each categorical feature column name (k)
  # to the values of that column stored in a tf.SparseTensor.
  categorical_cols = {k: tf.SparseTensor(
      indices=[[i, 0] for i in range(df[k].size)],
      values=df[k].values,
      shape=[df[k].size, 1])
                      for k in CATEGORICAL_COLUMNS}
  # Merges the two dictionaries into one.
  feature_cols = dict(continuous_cols)
  feature_cols.update(categorical_cols)
  # Converts the label column into a constant Tensor.
  label = tf.constant(df[LABEL_COLUMN].values)
  # Returns the feature columns and the label.
  return feature_cols, label

def main(_):
    train_file_name, test_file_name = _download_data()
    df_train = pd.read_csv(
        tf.gfile.Open(train_file_name),
        names=COLUMNS,
        skipinitialspace=True,
        sep=',',
        header=1,
        engine="python")
    df_test = pd.read_csv(
        tf.gfile.Open(test_file_name),
        names=COLUMNS,
        skipinitialspace=True,
        sep=',',
        header=1,
        engine="python")

    df_train = df_train.dropna(how='any', axis=0)
    df_test = df_test.dropna(how='any', axis=0)

    df_train[LABEL_COLUMN] = (df_train["claims_per_year"].apply(lambda x: ">2" in x)).astype(int)
    df_test[LABEL_COLUMN] = (df_test["claims_per_year"].apply(lambda x: ">2" in x)).astype(int)

    model_dir = tempfile.mkdtemp() if not FLAGS.model_dir else FLAGS.model_dir
    print("model directory = %s" % model_dir)

    m = build_estimator(model_dir)
    m.fit(input_fn=lambda: input_fn(df_train, True), steps=FLAGS.train_steps)
    results = m.evaluate(input_fn=lambda: input_fn(df_test), steps=1)
    for key in sorted(results):
        print("%s: %s" % (key, results[key]))





if __name__ == "__main__":
    tf.app.run()
