#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import preprocessing, tree, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.neural_network import BernoulliRBM


class Inference:
    def __init__(self, data_dir="data", grid_size=494, cv=5):
        self.funcs = ["cg_ref", "cg", "spv_ref", "mg_ref", "cg_timed"]
        self.data_dir = data_dir
        self.grid_size = grid_size
        self.cv = cv
        self.all = {
            "LR": self.lr, "DT": self.dt, "GB": self.gb, "RF": self.rf,
            "KNN": self.knn, "SVM": self.svm, "MLP": self.mlp,
            "RBM+LR": self.rbm_lr
        }
        self.scoring = {
            'accuracy': make_scorer(accuracy_score),
            'precision': make_scorer(precision_score),
            'recall': make_scorer(recall_score),
            'f1': make_scorer(f1_score)}

    def lr(self): return LogisticRegression(solver='lbfgs', max_iter=1000)
    def dt(self): return tree.DecisionTreeClassifier()
    def gb(self): return GradientBoostingClassifier()
    def rf(self): return RandomForestClassifier()
    def knn(self): return KNeighborsClassifier()
    def svm(self): return svm.SVC()
    def mlp(self): return MLPClassifier(hidden_layer_sizes=(32,16), max_iter=1000, random_state=42)
    def rbm_lr(self):
        rbm = BernoulliRBM(n_components=100, learning_rate=0.06, n_iter=10, random_state=42)
        lr = LogisticRegression(max_iter=1000)
        return Pipeline(steps=[('rbm', rbm), ('logistic', lr)])

    def read_data(self, f):
        path = os.path.join(self.data_dir, f"{f}_{self.grid_size}.csv")
        df = pd.read_csv(path, index_col=0)
        m = preprocessing.MinMaxScaler()
        x = df.iloc[:,2:].to_numpy().astype(np.float64)
        x_norm = m.fit_transform(x)
        y = df.iloc[:,:2].to_numpy().astype(np.float64)
        err_rate = [int(i != 0) for i in y[:, 0]]
        return x_norm, err_rate, df.columns[2:]

    def run_all(self):
        all_results = {}
        classifier_summary = {k: [] for k in self.all.keys()}
        output_lines = []

        for f in self.funcs:
            res = {"Estimator": self.all.keys(), "Accuracy": [], "Accuracy Stddev": [],
                   "Precision": [], "Precision Stddev": [], "Recall": [], "Recall Stddev": [],
                   "F1": [], "F1 Stddev": [], "Fit Time": [], "Fit Time Stddev": [],
                   "Score Time": [], "Score Time Stddev": []}

            X, y, feature_names = self.read_data(f)

            for k, v in self.all.items():
                clf = v()
                scores = cross_validate(clf, X, y=y, cv=self.cv, scoring=self.scoring, return_train_score=False)
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

                # Save for classifier-based comparison
                classifier_summary[k].append(res["F1"][-1])

            res_pd = pd.DataFrame.from_dict(res)
            res_pd.columns.name = f"{f}_{self.grid_size}"
            res_pd.set_index("Estimator", inplace=True)
            all_results[f] = res_pd
            res_pd.to_csv(os.path.join(self.data_dir, f'{f}.csv'))

        # Classifier comparison table by function
        classifier_df = pd.DataFrame(classifier_summary, index=self.funcs)
        classifier_df.to_csv(os.path.join(self.data_dir,"classifier_comparison_by_f1.csv"))

        # Feature importance and ranking output to file
        with open("sdc_sensitivity_and_features.txt", "w") as f:
            for clf_key in classifier_df.columns:
                ranked_funcs = classifier_df[clf_key].sort_values(ascending=False)
                f.write(f"=== Classifier: {clf_key} ===\n")
                f.write("SDC Sensitivity Ranking (by F1-score):\n")
                for func, f1_val in ranked_funcs.items():
                    f.write(f"{func}: F1 = {f1_val:.4f}\n")

                    X, y, feature_names = self.read_data(func)
                    model = self.all["RF"]()  # use RF consistently for feature importance
                    model.fit(X, y)
                    importances = model.feature_importances_
                    indices = np.argsort(importances)[::-1]
                    top_features = [(feature_names[i], importances[i]) for i in indices[:10]]

                    f.write(f"Top 10 important features in {func}:\n")
                    for name, weight in top_features:
                        f.write(f"  {name}: {weight:.5f}\n")
                    f.write("-\n")
                f.write("\n")

        return all_results, classifier_df

if __name__ == "__main__":
    i = Inference(data_dir="data", grid_size=494)
    res, clf_summary = i.run_all()
