#!/usr/bin/env python3

from __future__ import annotations

import os
import re
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RunMeta:
    test_id: int
    error_rate: float
    injection_rate: float
    label: int
    phase: str


class TimeSeriesDatasetBuilder:
    def __init__(
        self,
        raw_dir: str = "inference/raw/grid-494",
        out_dir: str = "inference/data",
        grid_size: int = 494,
        normalize_sequences: bool = True,
        fill_method: str = "ffill_bfill",
        fixed_length: Optional[int] = None,
    ) -> None:
        self.raw_dir = raw_dir
        self.out_dir = out_dir
        self.grid_size = grid_size
        self.normalize_sequences = normalize_sequences
        self.fill_method = fill_method
        self.fixed_length = fixed_length

        os.makedirs(self.out_dir, exist_ok=True)

    def build(self) -> None:
        run_files = self._discover_run_files()
        if not run_files:
            raise FileNotFoundError(f"No pmu_ts_*.csv files found under: {self.raw_dir}")

        summary_rows: List[Dict] = []
        metadata_rows: List[Dict] = []
        sequences: List[np.ndarray] = []
        labels: List[int] = []
        test_ids: List[int] = []
        feature_names_for_sequences: Optional[List[str]] = None
        sequence_lengths: List[int] = []

        for csv_path, test_id, error_rate, injection_rate in run_files:
            meta = RunMeta(
                test_id=test_id,
                error_rate=error_rate,
                injection_rate=injection_rate,
                label=0
                if (abs(error_rate) < 1e-9 and abs(injection_rate) < 1e-9)
                else 1,
                phase="normal"
                if (abs(error_rate) < 1e-9 and abs(injection_rate) < 1e-9)
                else "faulty",
            )

            df = self._load_single_run(csv_path)

            if feature_names_for_sequences is None:
                feature_names_for_sequences = [
                    c for c in df.columns if c != "timestamp_ms"
                ]

            df = self._align_feature_columns(df, feature_names_for_sequences)

            summary = self._extract_summary_features(df, meta)
            summary_rows.append(summary)

            metadata_rows.append(
                {
                    "test_id": meta.test_id,
                    "grid_size": self.grid_size,
                    "phase": meta.phase,
                    "error_rate": meta.error_rate,
                    "injection_rate": meta.injection_rate,
                    "label": meta.label,
                    "source_file": os.path.basename(csv_path),
                    "num_timesteps": len(df),
                }
            )

            seq = df[feature_names_for_sequences].to_numpy(dtype=np.float64)
            sequences.append(seq)
            labels.append(meta.label)
            test_ids.append(meta.test_id)
            sequence_lengths.append(seq.shape[0])

        summary_df = (
            pd.DataFrame(summary_rows).sort_values("test_id").reset_index(drop=True)
        )
        metadata_df = (
            pd.DataFrame(metadata_rows).sort_values("test_id").reset_index(drop=True)
        )

        X, seq_scaler = self._build_sequence_tensor(
            sequences=sequences,
            fixed_length=self.fixed_length,
            normalize=self.normalize_sequences,
        )

        y = np.asarray(labels, dtype=np.int64)
        tids = np.asarray(test_ids, dtype=np.int64)
        seq_lengths = np.asarray(sequence_lengths, dtype=np.int64)

        summary_csv = os.path.join(self.out_dir, "timeseries_summary_features.csv")
        metadata_csv = os.path.join(self.out_dir, "timeseries_run_metadata.csv")
        seq_npz = os.path.join(self.out_dir, "timeseries_sequences.npz")
        seq_scaler_json = os.path.join(self.out_dir, "timeseries_sequence_scaler.json")

        summary_df.to_csv(summary_csv, index=False)
        metadata_df.to_csv(metadata_csv, index=False)

        np.savez_compressed(
            seq_npz,
            X=X,
            y=y,
            test_id=tids,
            sequence_lengths=seq_lengths,
            feature_names=np.array(feature_names_for_sequences, dtype=object),
        )

        if seq_scaler is not None:
            with open(seq_scaler_json, "w", encoding="utf-8") as f:
                json.dump(seq_scaler, f, indent=2)

        print(f"[OK] Summary features saved to: {summary_csv}")
        print(f"[OK] Metadata saved to:         {metadata_csv}")
        print(f"[OK] Sequence dataset saved to: {seq_npz}")

        if seq_scaler is not None:
            print(f"[OK] Sequence scaler saved to:  {seq_scaler_json}")

        print("\nDataset summary:")
        print(f"  Runs found:             {len(run_files)}")
        print(f"  Normal runs:            {int((y == 0).sum())}")
        print(f"  Faulty runs:            {int((y == 1).sum())}")
        print(f"  Sequence tensor shape:  {X.shape}")
        print(f"  Feature count:          {len(feature_names_for_sequences)}")
        print(f"  Min sequence length:    {seq_lengths.min()}")
        print(f"  Max sequence length:    {seq_lengths.max()}")

    def _discover_run_files(self) -> List[Tuple[str, int, float, float]]:
        run_files: List[Tuple[str, int, float, float]] = []

        if not os.path.isdir(self.raw_dir):
            raise FileNotFoundError(f"Raw directory does not exist: {self.raw_dir}")

        pattern = re.compile(r"pmu_ts_(\d+)_([0-9.]+)_([0-9.]+)\.csv$")

        for fname in os.listdir(self.raw_dir):
            match = pattern.match(fname)
            if match:
                test_id = int(match.group(1))
                error_rate = float(match.group(2))
                injection_rate = float(match.group(3))

                run_files.append(
                    (
                        os.path.join(self.raw_dir, fname),
                        test_id,
                        error_rate,
                        injection_rate,
                    )
                )

        run_files.sort(key=lambda x: x[1])
        return run_files

    def _load_single_run(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)

        if df.empty:
            raise ValueError(f"Empty CSV: {csv_path}")

        if "timestamp_ms" not in df.columns:
            raise ValueError(
                f"'timestamp_ms' column missing in {csv_path}. "
                f"Columns found: {list(df.columns)}"
            )

        df = df.sort_values("timestamp_ms").reset_index(drop=True)

        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = self._fill_missing(df)

        if df.isnull().any().any():
            bad_cols = df.columns[df.isnull().any()].tolist()
            raise ValueError(
                f"NaNs remain after filling in {csv_path}. Problem columns: {bad_cols}"
            )

        df = df.drop_duplicates(subset=["timestamp_ms"], keep="first").reset_index(
            drop=True
        )

        return df

    def _fill_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.fill_method == "zero":
            return df.fillna(0)

        if self.fill_method == "ffill_bfill":
            return df.ffill().bfill()

        raise ValueError(f"Unsupported fill_method: {self.fill_method}")

    def _align_feature_columns(
        self, df: pd.DataFrame, feature_cols: List[str]
    ) -> pd.DataFrame:
        missing = [c for c in feature_cols if c not in df.columns]
        extra = [c for c in df.columns if c not in ["timestamp_ms"] + feature_cols]

        if missing:
            for col in missing:
                df[col] = 0.0

        if extra:
            df = df[["timestamp_ms"] + feature_cols]

        df = df[["timestamp_ms"] + feature_cols]
        return df

    def _extract_summary_features(self, df: pd.DataFrame, meta: RunMeta) -> Dict:
        row: Dict[str, float | int | str] = {
            "test_id": meta.test_id,
            "grid_size": self.grid_size,
            "phase": meta.phase,
            "error_rate": meta.error_rate,
            "injection_rate": meta.injection_rate,
            "label": meta.label,
            "num_timesteps": len(df),
            "duration_ms": float(
                df["timestamp_ms"].iloc[-1] - df["timestamp_ms"].iloc[0]
            )
            if len(df) > 1
            else 0.0,
        }

        feature_cols = [c for c in df.columns if c != "timestamp_ms"]

        t = df["timestamp_ms"].to_numpy(dtype=np.float64)
        if len(t) > 1:
            t = t - t[0]
        else:
            t = np.array([0.0], dtype=np.float64)

        for col in feature_cols:
            x = df[col].to_numpy(dtype=np.float64)

            row[f"{col}__mean"] = float(np.mean(x))
            row[f"{col}__std"] = float(np.std(x))
            row[f"{col}__min"] = float(np.min(x))
            row[f"{col}__max"] = float(np.max(x))
            row[f"{col}__median"] = float(np.median(x))
            row[f"{col}__range"] = float(np.max(x) - np.min(x))
            row[f"{col}__first"] = float(x[0])
            row[f"{col}__last"] = float(x[-1])
            row[f"{col}__delta"] = float(x[-1] - x[0])

            row[f"{col}__q25"] = float(np.percentile(x, 25))
            row[f"{col}__q75"] = float(np.percentile(x, 75))
            row[f"{col}__iqr"] = float(
                row[f"{col}__q75"] - row[f"{col}__q25"]
            )

            if len(x) > 1:
                row[f"{col}__auc"] = float(np.trapz(x, t))
            else:
                row[f"{col}__auc"] = float(x[0])

            row[f"{col}__slope"] = float(self._safe_slope(t, x))

            if len(x) > 1:
                dx = np.diff(x)
                row[f"{col}__diff_mean"] = float(np.mean(dx))
                row[f"{col}__diff_std"] = float(np.std(dx))
                row[f"{col}__diff_max"] = float(np.max(dx))
                row[f"{col}__diff_min"] = float(np.min(dx))
            else:
                row[f"{col}__diff_mean"] = 0.0
                row[f"{col}__diff_std"] = 0.0
                row[f"{col}__diff_max"] = 0.0
                row[f"{col}__diff_min"] = 0.0

        return row

    def _safe_slope(self, t: np.ndarray, x: np.ndarray) -> float:
        if len(t) < 2 or len(x) < 2:
            return 0.0

        if np.allclose(t, t[0]):
            return 0.0

        slope = np.polyfit(t, x, 1)[0]
        return float(slope)

    def _build_sequence_tensor(
        self,
        sequences: List[np.ndarray],
        fixed_length: Optional[int],
        normalize: bool,
    ) -> Tuple[np.ndarray, Optional[Dict]]:
        if not sequences:
            raise ValueError("No sequences were collected.")

        n_runs = len(sequences)
        n_features = sequences[0].shape[1]

        for seq in sequences:
            if seq.shape[1] != n_features:
                raise ValueError("Inconsistent feature dimension across runs.")

        max_len = max(seq.shape[0] for seq in sequences)
        target_len = fixed_length if fixed_length is not None else max_len

        scaler = None
        norm_sequences = sequences

        if normalize:
            stacked = np.vstack(sequences)
            feat_min = stacked.min(axis=0)
            feat_max = stacked.max(axis=0)

            denom = feat_max - feat_min
            denom[denom == 0] = 1.0

            norm_sequences = [(seq - feat_min) / denom for seq in sequences]
            scaler = {
                "type": "minmax",
                "feature_min": feat_min.tolist(),
                "feature_max": feat_max.tolist(),
            }

        X = np.zeros((n_runs, target_len, n_features), dtype=np.float32)

        for i, seq in enumerate(norm_sequences):
            seq_len = seq.shape[0]

            if seq_len >= target_len:
                X[i] = seq[:target_len]
            else:
                X[i, :seq_len, :] = seq

        return X, scaler


if __name__ == "__main__":
    builder = TimeSeriesDatasetBuilder(
        raw_dir="inference/raw/grid-494",
        out_dir="inference/data",
        grid_size=494,
        normalize_sequences=True,
        fill_method="ffill_bfill",
        fixed_length=None,
    )
    builder.build()
