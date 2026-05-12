#!/usr/bin/env python3

"""
timeseries_inference_analysis.py

Baseline ML analysis for merged PMU time-series row-level dataset.

Default input:
    inference/data/<matrix>/timeseries_merged_rows.csv

Default outputs:
    inference/data/<matrix>/timeseries_model_comparison.csv
    inference/data/<matrix>/timeseries_best_model.joblib
    inference/data/<matrix>/timeseries_feature_importance.csv
    inference/data/<matrix>/timeseries_confusion_matrix.csv
    inference/data/<matrix>/timeseries_test_predictions.csv
"""

from __future__ import annotations

import argparse
import os
import warnings
from typing import Dict, List, Tuple, Optional

import joblib
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier, BernoulliRBM


warnings.filterwarnings("ignore", category=ConvergenceWarning)


class TimeSeriesInference:
    def __init__(
        self,
        data_path: str,
        out_dir: str,
        matrix_name: str,
        random_state: int = 42,
        test_size: float = 0.2,
        cv_folds: int = 5,
    ) -> None:
        self.data_path = data_path
        self.out_dir = out_dir
        self.matrix_name = matrix_name
        self.random_state = random_state
        self.test_size = test_size
        self.cv_folds = cv_folds

        os.makedirs(self.out_dir, exist_ok=True)

        self.metadata_cols = [
            "source_file",
            "matrix_name",
            "grid_size",
            "test_id",
            "error_rate",
            "injection_rate",
            "label",
        ]

        self.models = {
            "LogisticRegression": LogisticRegression(
                max_iter=2000,
                random_state=self.random_state,
                class_weight="balanced",
            ),
            "RandomForest": RandomForestClassifier(
                n_estimators=300,
                random_state=self.random_state,
                class_weight="balanced",
            ),
            "GradientBoosting": GradientBoostingClassifier(
                random_state=self.random_state,
            ),
            "SVM": SVC(
                probability=True,
                kernel="rbf",
                random_state=self.random_state,
                class_weight="balanced",
            ),
            "MLP": MLPClassifier(
                hidden_layer_sizes=(64, 32),
                max_iter=1500,
                random_state=self.random_state,
            ),
	    "RBM_LR": Pipeline(
        	steps=[
            	    ("imputer", SimpleImputer(strategy="median")),
           	    ("minmax", MinMaxScaler()),
                    ("rbm", BernoulliRBM(
	                n_components=64,
	                learning_rate=0.01,
	                batch_size=16,
	                n_iter=30,
	                random_state=self.random_state,
	                verbose=False,
	            )),
	            ("logreg", LogisticRegression(
	                max_iter=2000,
	                random_state=self.random_state,
	                class_weight="balanced",
	            )),
	        ]
	    ),
        }

    def run(self) -> None:
        df = self._load_data()
        X, y, groups, feature_cols, meta_df = self._prepare_features(df)

        print("Dataset loaded successfully")
        print(f"  Matrix:                  {self.matrix_name}")
        print(f"  Input file:              {self.data_path}")
        print(f"  Output dir:              {self.out_dir}")
        print(f"  Total row samples:       {len(df)}")
        print(f"  Total runs/test_ids:     {groups.nunique()}")
        print(f"  Feature columns:         {len(feature_cols)}")
        print(f"  Normal row samples:      {int((y == 0).sum())}")
        print(f"  Faulty row samples:      {int((y == 1).sum())}")

        X_train, X_test, y_train, y_test, groups_train, groups_test, meta_train, meta_test = (
            self._group_train_test_split(X, y, groups, meta_df)
        )

        print("\nGroup-based train/test split")
        print(f"  Train rows:              {len(X_train)}")
        print(f"  Test rows:               {len(X_test)}")
        print(f"  Train runs/test_ids:     {groups_train.nunique()}")
        print(f"  Test runs/test_ids:      {groups_test.nunique()}")

        self._validate_group_split(groups_train, groups_test)

        results = []
        best_model_name: Optional[str] = None
        best_pipeline: Optional[Pipeline] = None
        best_f1 = -1.0
        best_test_outputs = None

        for model_name, model in self.models.items():
            print(f"\nRunning model: {model_name}")

            pipeline = self._build_pipeline(model)

            cv_scores = self._cross_validate_model(
                pipeline=pipeline,
                X_train=X_train,
                y_train=y_train,
                groups_train=groups_train,
            )

            pipeline.fit(X_train, y_train)

            y_pred = pipeline.predict(X_test)
            y_prob = self._predict_proba_safe(pipeline, X_test)

            metrics = self._compute_metrics(y_test, y_pred, y_prob)
            metrics["model"] = model_name
            metrics.update(cv_scores)

            results.append(metrics)

            print(
                f"  Test Accuracy: {metrics['test_accuracy']:.4f} | "
                f"Precision: {metrics['test_precision']:.4f} | "
                f"Recall: {metrics['test_recall']:.4f} | "
                f"F1: {metrics['test_f1']:.4f} | "
                f"ROC-AUC: {metrics['test_roc_auc']:.4f}"
            )

            if metrics["test_f1"] > best_f1:
                best_f1 = metrics["test_f1"]
                best_model_name = model_name
                best_pipeline = pipeline
                best_test_outputs = {
                    "y_test": y_test.copy(),
                    "y_pred": y_pred.copy(),
                    "y_prob": y_prob.copy() if y_prob is not None else None,
                    "meta_test": meta_test.copy(),
                }

        results_df = pd.DataFrame(results).sort_values(
            by=["test_f1", "test_recall", "test_precision", "test_accuracy"],
            ascending=False,
        ).reset_index(drop=True)

        results_path = os.path.join(self.out_dir, "timeseries_model_comparison.csv")
        results_df.to_csv(results_path, index=False)

        print("\n==================================================")
        print("Model comparison complete")
        print(
            results_df[
                [
                    "model",
                    "cv_accuracy_mean",
                    "cv_accuracy_std",
                    "cv_precision_mean",
                    "cv_precision_std",
                    "cv_recall_mean",
                    "cv_recall_std",
                    "cv_f1_mean",
                    "cv_f1_std",
                    "cv_roc_auc_mean",
                    "cv_roc_auc_std",
                    "test_accuracy",
                    "test_precision",
                    "test_recall",
                    "test_f1",
                    "test_roc_auc",
                ]
            ].to_string(index=False)
        )
        print("==================================================")

        if best_pipeline is None or best_model_name is None or best_test_outputs is None:
            raise RuntimeError("No best model identified. Something went wrong.")

        model_path = os.path.join(self.out_dir, "timeseries_best_model.joblib")
        joblib.dump(best_pipeline, model_path)

        print(f"\nBest model: {best_model_name}")
        print(f"Best model saved to: {model_path}")
        print(f"Comparison CSV saved to: {results_path}")

        self._save_confusion_matrix(
            y_true=best_test_outputs["y_test"],
            y_pred=best_test_outputs["y_pred"],
        )

        self._save_test_predictions(
            meta_test=best_test_outputs["meta_test"],
            y_test=best_test_outputs["y_test"],
            y_pred=best_test_outputs["y_pred"],
            y_prob=best_test_outputs["y_prob"],
            best_model_name=best_model_name,
        )

        self._save_feature_importance_if_available(
            best_pipeline=best_pipeline,
            feature_cols=feature_cols,
            best_model_name=best_model_name,
        )

    def _load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Input file not found: {self.data_path}")

        df = pd.read_csv(self.data_path)

        if df.empty:
            raise ValueError(f"Input CSV is empty: {self.data_path}")

        required_cols = ["test_id", "label"]

        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        return df

    def _prepare_features(
        self,
        df: pd.DataFrame,
    ) -> Tuple[pd.DataFrame, pd.Series, pd.Series, List[str], pd.DataFrame]:
        available_metadata_cols = [c for c in self.metadata_cols if c in df.columns]

        feature_cols = [c for c in df.columns if c not in available_metadata_cols]

        if not feature_cols:
            raise ValueError("No PMU feature columns found after removing metadata columns.")

        X = df[feature_cols].copy()
        y = df["label"].astype(int).copy()
        groups = df["test_id"].astype(int).copy()
        meta_df = df[available_metadata_cols].copy()

        for col in X.columns:
            X[col] = pd.to_numeric(X[col], errors="coerce")

        return X, y, groups, feature_cols, meta_df

    def _group_train_test_split(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        groups: pd.Series,
        meta_df: pd.DataFrame,
    ):
        splitter = GroupShuffleSplit(
            n_splits=1,
            test_size=self.test_size,
            random_state=self.random_state,
        )

        train_idx, test_idx = next(splitter.split(X, y, groups=groups))

        X_train = X.iloc[train_idx].reset_index(drop=True)
        X_test = X.iloc[test_idx].reset_index(drop=True)

        y_train = y.iloc[train_idx].reset_index(drop=True)
        y_test = y.iloc[test_idx].reset_index(drop=True)

        groups_train = groups.iloc[train_idx].reset_index(drop=True)
        groups_test = groups.iloc[test_idx].reset_index(drop=True)

        meta_train = meta_df.iloc[train_idx].reset_index(drop=True)
        meta_test = meta_df.iloc[test_idx].reset_index(drop=True)

        return (
            X_train,
            X_test,
            y_train,
            y_test,
            groups_train,
            groups_test,
            meta_train,
            meta_test,
        )

    def _validate_group_split(
        self,
        groups_train: pd.Series,
        groups_test: pd.Series,
    ) -> None:
        train_ids = set(groups_train.unique())
        test_ids = set(groups_test.unique())
        overlap = train_ids.intersection(test_ids)

        if overlap:
            raise RuntimeError(
                f"Data leakage detected. These test_id values exist in both train and test: {sorted(overlap)}"
            )

        print("  Group leakage check:     PASSED")

    def _build_pipeline(self, model) -> Pipeline:
        return Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", clone(model)),
            ]
        )

    def _cross_validate_model(
        self,
        pipeline: Pipeline,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        groups_train: pd.Series,
    ) -> Dict[str, float]:
        unique_groups = groups_train.nunique()
        n_splits = min(self.cv_folds, unique_groups)

        if n_splits < 2:
            return {
                "cv_accuracy_mean": np.nan,
                "cv_accuracy_std": np.nan,
                "cv_precision_mean": np.nan,
                "cv_precision_std": np.nan,
                "cv_recall_mean": np.nan,
                "cv_recall_std": np.nan,
                "cv_f1_mean": np.nan,
                "cv_f1_std": np.nan,
                "cv_roc_auc_mean": np.nan,
                "cv_roc_auc_std": np.nan,
            }

        cv = StratifiedGroupKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=self.random_state,
        )

        scoring = {
            "accuracy": "accuracy",
            "precision": "precision",
            "recall": "recall",
            "f1": "f1",
            "roc_auc": "roc_auc",
        }

        cv_results = cross_validate(
            pipeline,
            X_train,
            y_train,
            groups=groups_train,
            cv=cv,
            scoring=scoring,
            return_train_score=False,
            n_jobs=-1,
        )

        return {
            "cv_accuracy_mean": float(np.mean(cv_results["test_accuracy"])),
            "cv_accuracy_std": float(np.std(cv_results["test_accuracy"])),
            "cv_precision_mean": float(np.mean(cv_results["test_precision"])),
            "cv_precision_std": float(np.std(cv_results["test_precision"])),
            "cv_recall_mean": float(np.mean(cv_results["test_recall"])),
            "cv_recall_std": float(np.std(cv_results["test_recall"])),
            "cv_f1_mean": float(np.mean(cv_results["test_f1"])),
            "cv_f1_std": float(np.std(cv_results["test_f1"])),
            "cv_roc_auc_mean": float(np.mean(cv_results["test_roc_auc"])),
            "cv_roc_auc_std": float(np.std(cv_results["test_roc_auc"])),
        }

    def _predict_proba_safe(self, pipeline: Pipeline, X_test: pd.DataFrame):
        model = pipeline.named_steps["model"]

        if hasattr(model, "predict_proba"):
            return pipeline.predict_proba(X_test)[:, 1]

        if hasattr(model, "decision_function"):
            decision = pipeline.decision_function(X_test)
            decision = np.asarray(decision, dtype=float)

            min_v = decision.min()
            max_v = decision.max()

            if max_v - min_v == 0:
                return np.zeros_like(decision)

            return (decision - min_v) / (max_v - min_v)

        return None

    def _compute_metrics(
        self,
        y_true,
        y_pred,
        y_prob=None,
    ) -> Dict[str, float]:
        metrics = {
            "test_accuracy": float(accuracy_score(y_true, y_pred)),
            "test_precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "test_recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "test_f1": float(f1_score(y_true, y_pred, zero_division=0)),
        }

        if y_prob is not None:
            try:
                metrics["test_roc_auc"] = float(roc_auc_score(y_true, y_prob))
            except Exception:
                metrics["test_roc_auc"] = np.nan
        else:
            metrics["test_roc_auc"] = np.nan

        return metrics

    def _save_confusion_matrix(
        self,
        y_true,
        y_pred,
    ) -> None:
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

        cm_df = pd.DataFrame(
            cm,
            index=["Actual_Normal", "Actual_Faulty"],
            columns=["Pred_Normal", "Pred_Faulty"],
        )

        out_path = os.path.join(self.out_dir, "timeseries_confusion_matrix.csv")
        cm_df.to_csv(out_path)

        print(f"Confusion matrix saved to: {out_path}")

    def _save_test_predictions(
        self,
        meta_test: pd.DataFrame,
        y_test,
        y_pred,
        y_prob,
        best_model_name: str,
    ) -> None:
        pred_df = meta_test.copy().reset_index(drop=True)

        pred_df["y_true"] = np.asarray(y_test)
        pred_df["y_pred"] = np.asarray(y_pred)

        if y_prob is not None:
            pred_df["y_score"] = np.asarray(y_prob)

        pred_df["best_model"] = best_model_name

        out_path = os.path.join(self.out_dir, "timeseries_test_predictions.csv")
        pred_df.to_csv(out_path, index=False)

        print(f"Test predictions saved to: {out_path}")

    def _save_feature_importance_if_available(
        self,
        best_pipeline: Pipeline,
        feature_cols: List[str],
        best_model_name: str,
    ) -> None:
        model = best_pipeline.named_steps["model"]
        out_path = os.path.join(self.out_dir, "timeseries_feature_importance.csv")

        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_

            fi_df = pd.DataFrame(
                {
                    "feature": feature_cols,
                    "importance": importances,
                    "model": best_model_name,
                }
            ).sort_values(by="importance", ascending=False)

            fi_df.to_csv(out_path, index=False)

            print(f"Feature importance saved to: {out_path}")
            return

        if hasattr(model, "coef_"):
            coefs = np.ravel(model.coef_)

            fi_df = pd.DataFrame(
                {
                    "feature": feature_cols,
                    "coefficient": coefs,
                    "abs_coefficient": np.abs(coefs),
                    "model": best_model_name,
                }
            ).sort_values(by="abs_coefficient", ascending=False)

            fi_df.to_csv(out_path, index=False)

            print(f"Model coefficients saved to: {out_path}")
            return

        print(f"No feature importance available for best model: {best_model_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PMU time-series ML inference")

    parser.add_argument(
        "--matrix",
        type=str,
        default="494_bus",
        help="Matrix name, example: 494_bus, 662_bus, 1138_bus, bcsstk19",
    )

    parser.add_argument(
        "--data-path",
        type=str,
        default=None,
        help="Input merged dataset path",
    )

    parser.add_argument(
        "--out-dir",
        type=str,
        default=None,
        help="Output directory",
    )

    args = parser.parse_args()

    matrix_name = args.matrix
    data_path = args.data_path or f"inference/data/{matrix_name}/timeseries_merged_rows.csv"
    out_dir = args.out_dir or f"inference/data/{matrix_name}"

    analysis = TimeSeriesInference(
        data_path=data_path,
        out_dir=out_dir,
        matrix_name=matrix_name,
        random_state=42,
        test_size=0.2,
        cv_folds=5,
    )

    analysis.run()
