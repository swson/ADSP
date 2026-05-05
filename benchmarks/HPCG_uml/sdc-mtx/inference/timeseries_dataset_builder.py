#!/usr/bin/env python3

from __future__ import annotations

import os
import re
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
    source_file: str


class TimeSeriesDatasetBuilder:
    def __init__(
        self,
        raw_dir: str = "inference/raw/grid-494",
        out_dir: str = "inference/data",
        grid_size: int = 494,
        fill_method: str = "ffill_bfill",
        keep_source_file: bool = False,
    ) -> None:
        self.raw_dir = raw_dir
        self.out_dir = out_dir
        self.grid_size = grid_size
        self.fill_method = fill_method
        self.keep_source_file = keep_source_file

        os.makedirs(self.out_dir, exist_ok=True)

    def build(self) -> None:
        run_files = self._discover_run_files()

        if not run_files:
            raise FileNotFoundError(f"No pmu_ts_*.csv files found under: {self.raw_dir}")

        merged_rows: List[pd.DataFrame] = []
        metadata_rows: List[Dict] = []
        reference_feature_cols: Optional[List[str]] = None

        for csv_path, test_id, error_rate, injection_rate in run_files:
            label = 0 if abs(error_rate) < 1e-9 and abs(injection_rate) < 1e-9 else 1
            phase = "normal" if label == 0 else "faulty"

            meta = RunMeta(
                test_id=test_id,
                error_rate=error_rate,
                injection_rate=injection_rate,
                label=label,
                phase=phase,
                source_file=os.path.basename(csv_path),
            )

            df = self._load_single_run(csv_path)

            feature_cols = [c for c in df.columns if c != "timestamp_ms"]

            if reference_feature_cols is None:
                reference_feature_cols = feature_cols

            df = self._align_feature_columns(df, reference_feature_cols)

            raw_df = df.drop(columns=["timestamp_ms"]).copy()

            summary_features = self._extract_selected_summary_features(
                df=df,
                feature_cols=reference_feature_cols,
            )

            for stat_col, stat_value in summary_features.items():
                raw_df[stat_col] = stat_value

            insert_cols = [
                ("label", meta.label),
                ("injection_rate", meta.injection_rate),
                ("error_rate", meta.error_rate),
                ("test_id", meta.test_id),
            ]

            if self.keep_source_file:
                insert_cols.insert(0, ("source_file", meta.source_file))

            for col_name, col_value in reversed(insert_cols):
                raw_df.insert(0, col_name, col_value)

            merged_rows.append(raw_df)

            metadata_rows.append(
                {
                    "test_id": meta.test_id,
                    "grid_size": self.grid_size,
                    "phase": meta.phase,
                    "error_rate": meta.error_rate,
                    "injection_rate": meta.injection_rate,
                    "label": meta.label,
                    "source_file": meta.source_file,
                    "num_timesteps": len(df),
                    "num_raw_pmu_counters": len(reference_feature_cols),
                    "num_summary_features": len(summary_features),
                }
            )

        merged_df = pd.concat(merged_rows, ignore_index=True)
        metadata_df = pd.DataFrame(metadata_rows).sort_values("test_id").reset_index(drop=True)

        merged_csv = os.path.join(self.out_dir, "timeseries_merged_rows.csv")
        metadata_csv = os.path.join(self.out_dir, "timeseries_run_metadata.csv")

        merged_df.to_csv(merged_csv, index=False)
        metadata_df.to_csv(metadata_csv, index=False)

        y = merged_df["label"].astype(int)

        raw_feature_count = len(reference_feature_cols) if reference_feature_cols else 0
        summary_feature_count = 6 * raw_feature_count
        total_feature_count = raw_feature_count + summary_feature_count

        print(f"[OK] Raw + summary row-level dataset saved to: {merged_csv}")
        print(f"[OK] Run metadata saved to:                  {metadata_csv}")

        print("\nDataset summary:")
        print(f"  Files/runs found:        {len(run_files)}")
        print(f"  Normal runs:             {sum(1 for _, _, e, i in run_files if abs(e) < 1e-9 and abs(i) < 1e-9)}")
        print(f"  Faulty runs:             {sum(1 for _, _, e, i in run_files if not (abs(e) < 1e-9 and abs(i) < 1e-9))}")
        print(f"  Final dataset rows:      {len(merged_df)}")
        print(f"  Raw PMU feature count:   {raw_feature_count}")
        print(f"  Summary feature count:   {summary_feature_count}")
        print(f"  Total ML feature count:  {total_feature_count}")
        print(f"  Final CSV columns:       {len(merged_df.columns)}")

        print("\nLabel distribution:")
        print(y.value_counts().sort_index().to_string())

    def _discover_run_files(self) -> List[Tuple[str, int, float, float]]:
        run_files: List[Tuple[str, int, float, float]] = []

        if not os.path.isdir(self.raw_dir):
            raise FileNotFoundError(f"Raw directory does not exist: {self.raw_dir}")

        pattern = re.compile(r"pmu_ts_(\d+)_([0-9.]+)_([0-9.]+)\.csv$")

        for fname in os.listdir(self.raw_dir):
            match = pattern.match(fname)

            if not match:
                continue

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

        df = df.drop_duplicates(subset=["timestamp_ms"], keep="first").reset_index(drop=True)

        return df

    def _fill_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.fill_method == "zero":
            return df.fillna(0)

        if self.fill_method == "ffill_bfill":
            return df.ffill().bfill()

        raise ValueError(f"Unsupported fill_method: {self.fill_method}")

    def _align_feature_columns(
        self,
        df: pd.DataFrame,
        reference_feature_cols: List[str],
    ) -> pd.DataFrame:
        missing = [c for c in reference_feature_cols if c not in df.columns]

        for col in missing:
            df[col] = 0.0

        extra = [
            c for c in df.columns
            if c not in ["timestamp_ms"] + reference_feature_cols
        ]

        if extra:
            print(f"[WARN] Dropping extra columns: {extra}")

        return df[["timestamp_ms"] + reference_feature_cols]

    def _extract_selected_summary_features(
        self,
        df: pd.DataFrame,
        feature_cols: List[str],
    ) -> Dict[str, float]:
        summary: Dict[str, float] = {}

        t = df["timestamp_ms"].to_numpy(dtype=np.float64)

        if len(t) > 1:
            t = t - t[0]
        else:
            t = np.array([0.0], dtype=np.float64)

        for col in feature_cols:
            x = df[col].to_numpy(dtype=np.float64)

            summary[f"{col}__mean"] = float(np.mean(x))
            summary[f"{col}__std"] = float(np.std(x))
            summary[f"{col}__min"] = float(np.min(x))
            summary[f"{col}__max"] = float(np.max(x))
            summary[f"{col}__delta"] = float(x[-1] - x[0])
            summary[f"{col}__slope"] = float(self._safe_slope(t, x))

        return summary

    def _safe_slope(self, t: np.ndarray, x: np.ndarray) -> float:
        if len(t) < 2 or len(x) < 2:
            return 0.0

        if np.allclose(t, t[0]):
            return 0.0

        return float(np.polyfit(t, x, 1)[0])


if __name__ == "__main__":
    builder = TimeSeriesDatasetBuilder(
        raw_dir="inference/raw/grid-494",
        out_dir="inference/data",
        grid_size=494,
        fill_method="ffill_bfill",
        keep_source_file=False,
    )

    builder.build()
