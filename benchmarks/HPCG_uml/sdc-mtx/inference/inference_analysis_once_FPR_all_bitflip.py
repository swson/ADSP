#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import preprocessing, tree, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import (
    make_scorer, accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix
)
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.neural_network import BernoulliRBM


class Inference:
    def __init__(self, data_dir, output_dir, cv=5):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.cv = cv
        self.funcs = [
            os.path.splitext(f)[0] for f in os.listdir(self.data_dir)
            if f.endswith(".csv")
        ]
        os.makedirs(self.output_dir, exist_ok=True)

        self.all = {
            "LR": self.lr, "DT": self.dt, "GB": self.gb, "RF": self.rf,
            "KNN": self.knn, "SVM": self.svm, "MLP": self.mlp,
            "RBM+LR": self.rbm_lr
        }

        # 기존 scoring 유지 (주의: precision/recall/f1에서 0 division 방지)
        self.scoring = {
            'accuracy': make_scorer(accuracy_score),
            'precision': make_scorer(precision_score, zero_division=0),
            'recall': make_scorer(recall_score, zero_division=0),
            'f1': make_scorer(f1_score, zero_division=0),
        }

    def lr(self): return LogisticRegression(solver='lbfgs', max_iter=1000)
    def dt(self): return tree.DecisionTreeClassifier()
    def gb(self): return GradientBoostingClassifier()
    def rf(self): return RandomForestClassifier()
    def knn(self): return KNeighborsClassifier()
    def svm(self): return svm.SVC()
    def mlp(self): return MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=1000, random_state=42)
    def rbm_lr(self):
        rbm = BernoulliRBM(n_components=100, learning_rate=0.06, n_iter=10, random_state=42)
        lr = LogisticRegression(max_iter=1000)
        return Pipeline(steps=[('rbm', rbm), ('logistic', lr)])

    def read_data(self, file_name):
        path = os.path.join(self.data_dir, file_name + ".csv")

        df = pd.read_csv(path)

        if df.columns[0].startswith("Unnamed"):
            df = df.drop(columns=[df.columns[0]])
        
        m = preprocessing.MinMaxScaler()
        x = df.iloc[:, 2:].to_numpy().astype(np.float64)
        x_norm = m.fit_transform(x)
  
        er_raw = df.iloc[:, 0]
        y = []
        for val in er_raw:
            try:
                v = float(val)
                y.append(0 if v == 0.0 else 1)
            except:
                y.append(1)  # b0-0 같은 문자열이면 Error로 처리

        y = np.array(y, dtype=int)
        
        return x_norm, y, df.columns[2:]

    
    def _cv_confusion_stats(self, clf, X, y):
        """
        fold별로 모델 학습/예측을 수행하고 confusion matrix(TN,FP,FN,TP)를
        fold 단위로 저장해서 mean/std 를 계산한다.
        """
        skf = StratifiedKFold(n_splits=self.cv, shuffle=True, random_state=42)

        tn_list, fp_list, fn_list, tp_list = [], [], [], []

        for train_idx, test_idx in skf.split(X, y):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            clf_fold = clf  # 기본은 그대로 사용
            # 일부 estimator는 fit 후 상태가 남으므로 fold마다 새 인스턴스가 더 안전
            # -> 간단히 clone 대신 새로 생성하도록 호출부에서 새 clf 넘김(아래 run_all 참고)

            clf_fold.fit(X_train, y_train)
            y_pred = clf_fold.predict(X_test)

            cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
            tn, fp, fn, tp = cm.ravel()
            tn_list.append(tn); fp_list.append(fp); fn_list.append(fn); tp_list.append(tp)

        def mean_std(a):
            a = np.array(a, dtype=float)
            return a.mean(), a.std()

        tn_m, tn_s = mean_std(tn_list)
        fp_m, fp_s = mean_std(fp_list)
        fn_m, fn_s = mean_std(fn_list)
        tp_m, tp_s = mean_std(tp_list)

        return {
            "TN": tn_m, "TN Stddev": tn_s,
            "FP": fp_m, "FP Stddev": fp_s,
            "FN": fn_m, "FN Stddev": fn_s,
            "TP": tp_m, "TP Stddev": tp_s,
        }

    def run_all(self):
        all_results = {}
        classifier_summary = {k: [] for k in self.all.keys()}

        for f in self.funcs:
            print(f"[INFO] Processing {f}.csv ...")
            res = {
                "Estimator": self.all.keys(),
                "Accuracy": [], "Accuracy Stddev": [],
                "Precision": [], "Precision Stddev": [],
                "Recall": [], "Recall Stddev": [],
                "F1": [], "F1 Stddev": [],

                # TP/FP/FN/TN + stddev
                "TP": [], "TP Stddev": [],
                "FP": [], "FP Stddev": [],
                "FN": [], "FN Stddev": [],
                "TN": [], "TN Stddev": [],

                "Fit Time": [], "Fit Time Stddev": [],
                "Score Time": [], "Score Time Stddev": []
            }

            X, y, feature_names = self.read_data(f)

            for k, v in self.all.items():
                # (1) 기존 metric + time
                clf = v()
                scores = cross_validate(
                    clf, X, y=y, cv=self.cv,
                    scoring=self.scoring,
                    return_train_score=False
                )

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

                # (2) fold별 confusion matrix로 TP/FP/FN/TN
                # fold마다 새 estimator가 필요하므로 v()로 새로 생성해서 fold loop에서 사용
                cm_stats = self._cv_confusion_stats(v(), X, y)

                res["TP"].append(cm_stats["TP"])
                res["TP Stddev"].append(cm_stats["TP Stddev"])
                res["FP"].append(cm_stats["FP"])
                res["FP Stddev"].append(cm_stats["FP Stddev"])
                res["FN"].append(cm_stats["FN"])
                res["FN Stddev"].append(cm_stats["FN Stddev"])
                res["TN"].append(cm_stats["TN"])
                res["TN Stddev"].append(cm_stats["TN Stddev"])

                classifier_summary[k].append(res["F1"][-1])

            res_pd = pd.DataFrame.from_dict(res)
            res_pd.columns.name = f
            res_pd.set_index("Estimator", inplace=True)
            all_results[f] = res_pd

            out_path = os.path.join(self.output_dir, f"{f}_results.csv")
            res_pd.to_csv(out_path)

        classifier_df = pd.DataFrame(classifier_summary, index=self.funcs)
        classifier_df.to_csv(os.path.join(self.output_dir, "classifier_comparison.csv"))

        # (기존 feature importance 부분 그대로)
        with open(os.path.join(self.output_dir, "imp_counters.txt"), "w") as f_out:
            for clf_key in classifier_df.columns:
                ranked_funcs = classifier_df[clf_key].sort_values(ascending=False)
                f_out.write(f"=== Classifier: {clf_key} ===\n")
                f_out.write("SDC Sensitivity Ranking (by F1-score):\n")
                for func, f1_val in ranked_funcs.items():
                    f_out.write(f"{func}: F1 = {f1_val:.4f}\n")
                    X, y, feature_names = self.read_data(func)
                    model = self.all["RF"]()
                    model.fit(X, y)
                    importances = model.feature_importances_
                    indices = np.argsort(importances)[::-1]
                    top_features = [(feature_names[i], importances[i]) for i in indices[:20]]

                    f_out.write(f"Top 20 important features in {func}:\n")
                    for name, weight in top_features:
                        f_out.write(f"  {name}: {weight:.5f}\n")
                    f_out.write("-\n")
                f_out.write("\n")

        return all_results, classifier_df


if __name__ == "__main__":


    matrix_names = ["494_bus", "662_bus", "1138_bus", "bcsstk01", "bcsstk19", "bcsstk20", "bfwb62", "bfwb398", "bfwb782"]
    dataset_range = range(1, 6)  # 1~5

    data_root = "output_all/bitflip_MSB"
    out_root = "inf_all/inf_bitflip_MSB"
    os.makedirs(data_root, exist_ok=True)
    os.makedirs(out_root, exist_ok=True)    

    for matrix_name in matrix_names:
        for dataset_id in dataset_range:
            data_dir = os.path.join(data_root, f"{matrix_name}_{dataset_id}")
            output_dir = os.path.join(out_root, f"{matrix_name}_{dataset_id}")

            os.makedirs(output_dir, exist_ok=True)

            if not os.path.isdir(data_dir):
                print(f"[SKIP] Missing folder: {data_dir}")
                continue

            csvs = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
            if len(csvs) == 0:
                print(f"[SKIP] No CSV files in: {data_dir}")
                continue

            print("\n====================================================")
            print(f"[RUN] Matrix: {matrix_name}, Dataset: {dataset_id}")
            print(f"      data_dir  = {data_dir}")
            print(f"      output_dir= {output_dir}")
            print("====================================================")

            i = Inference(data_dir=data_dir, output_dir=output_dir, cv=5)
            res, clf_summary = i.run_all()









