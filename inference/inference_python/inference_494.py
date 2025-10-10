#!/usr/bin/env python

"""
This script evaluates the performance of classifiers on the HPCG dataset.
"""

import os
import numpy as np
import pandas as pd
from sklearn import preprocessing, tree, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.neural_network import MLPClassifier

class Inference:
    def __init__(self, data_dir="data", grid_size=494, cv=5):
        self.funcs = ["cg_ref", "cg", "spv_ref", "mg_ref", "cg_timed"]
        self.data_dir = data_dir
        self.grid_size = grid_size
        self.cv = cv
        self.all = {"LR": self.lr, "DT": self.dt, "GB": self.gb, "RF": self.rf,
                    "KNN": self.knn, "SVM": self.svm, "MLP": self.mlp}
        self.scoring = {
           'accuracy': make_scorer(accuracy_score),
           'precision': make_scorer(precision_score),
           'recall': make_scorer(recall_score),
           'f1': make_scorer(f1_score)}

    def lr(self):
        return LogisticRegression(solver='lbfgs', max_iter=1000)

    def dt(self):
        return tree.DecisionTreeClassifier()

    def gb(self):
        return GradientBoostingClassifier()

    def rf(self):
        return RandomForestClassifier()

    def knn(self):
        return KNeighborsClassifier()

    def svm(self):
        return svm.SVC()

    def mlp(self):
        return MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=1000, random_state=42)

    def read_data(self, f):
        path = os.path.join(self.data_dir, f"{f}_{self.grid_size}.csv")
        df = pd.read_csv(path, index_col=0)
        m = preprocessing.MinMaxScaler()
        x = df.iloc[:,2:].to_numpy().astype(np.float64)
        x_norm = m.fit_transform(x)
        y = df.iloc[:,:2].to_numpy().astype(np.float64)
        err_rate = [int(i != 0) for i in y[:, 0]]
        inj_rate = [int(i != 0) for i in y[:, 1]]
        return x_norm, err_rate

    def run_all(self):
        p = {}
        for f in self.funcs:
            res = {"Estimator": self.all.keys(),
                   "Accuracy": [],
                   "Accuracy Stddev": [],
                   "Precision": [],
                   "Precision Stddev": [],
                   "Recall": [],
                   "Recall Stddev": [],
                   "F1": [],
                   "F1 Stddev": [],
                   "Fit Time": [],
                   "Fit Time Stddev": [],
                   "Score Time": [],
                   "Score Time Stddev": []
                   }
            X, y = self.read_data(f)
            for k, v in self.all.items():
                clf = v()
                scores = cross_validate(clf, X, y=y, cv=self.cv,
                                         scoring=self.scoring)
                res["Accuracy"].append(scores["test_accuracy"].mean())
                res["Accuracy Stddev"].append(scores["test_accuracy"].std())
                res["Precision"].append(scores["test_precision"].mean())
                res["Precision Stddev"].append(scores["test_precision"].std())
                res["Recall"].append(scores["test_recall"].mean())
                res["Recall Stddev"].append(scores["test_recall"].std())
                res["F1"].append(scores["test_f1"].mean())
                res["F1 Stddev"].append(scores["test_f1"].std())
                res["Fit Time"].append(scores["fit_time"].mean())
                res["Fit Time Stddev"].append(scores["fit_time"].std())
                res["Score Time"].append(scores["score_time"].mean())
                res["Score Time Stddev"].append(scores["score_time"].std())

            res_pd = pd.DataFrame.from_dict(res)
            res_pd.columns.name = f"{f}_{self.grid_size}"
            res_pd.set_index("Estimator", inplace=True)
            p[f] = res_pd
        return p

if __name__ == "__main__":
    i = Inference(grid_size=494)
    res = i.run_all()
    for k,v in res.items():
        print(k, v)
        v.to_csv(f'{k}.csv', index=False)
