import pandas as pd
import numpy as np
import time
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

# need refractor here
method_dict = {
        "LG": LogisticRegression(),
        "KN": KNeighborsClassifier(),
        "SV": SVC(),
        "GB": GradientBoostingClassifier(n_estimators=1000),
        "DT": tree.DecisionTreeClassifier(),
        "RF": RandomForestClassifier(n_estimators=1000),
        "MP": MLPClassifier(alpha = 1),
        "NB": GaussianNB(),
    }


def do_classification(df_droped_label, X_train, Y_train, X_test, Y_test, classifier_name):
    t_start = time.process_time()
    classifier = method_dict[classifier_name]
    classifier.fit(X_train, Y_train)
    t_end = time.process_time()
    t_diff = t_end - t_start;
    train_score = classifier.score(X_train, Y_train)
    test_score = classifier.score(X_test, Y_test)

    result = {'model': classifier, 'train_score': train_score, 'test_score': test_score,
                                        'train_time': t_diff}
    predict_label = classifier.predict(df_droped_label)
    return predict_label, result

"""
    This function fetches the training data set 
    and the origin dataset
"""
def get_train_test_data(df, label_name, x_name, ratio):
    mask = np.random.choice([True, False], size=len(df), p=[ratio, 1-ratio])

    df_train = df[mask]
    df_test = df[~mask]

    label_train = df_train[label_name].values
    label_test = df_test[label_name].values
    x_train = df_train[x_name].values
    x_test = df_test[x_name].values

    return df_train, df_test, x_train, label_train, x_test, label_test

def MyClassification(df, label_name, classifier_name, train_ratio):
    train_ratio = float(train_ratio)
    x_name = list(df.columns.values)
    x_name.remove(label_name)
    df_train, df_test, X_train, Y_train, X_test, Y_test = get_train_test_data(df, label_name, x_name,
                                                                         train_ratio)

    predict_label, train_result = do_classification(df.drop([label_name], axis=1),X_train, Y_train, X_test, Y_test, classifier_name)
    new_df = df.copy(deep=True)
    new_df = new_df.rename(columns = {label_name: "Label"})
    new_df["prediction_result"] = predict_label
    return new_df, train_result