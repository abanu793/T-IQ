# src/etl.py
import os
import json
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Dict, Any

DATA_RAW = Path("data/raw")
DATA_PROCESSED = Path("data/processed")
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


def safe_read_csv(path: str, **kwargs) -> pd.DataFrame:
    """Read CSV with safe defaults."""
    return pd.read_csv(path, low_memory=False, **kwargs)


def safe_read_json(path: str, **kwargs) -> pd.DataFrame:
    """Read JSON; if nested list of records, normalize."""
    df = pd.read_json(path, **kwargs)
    # if nested, try to normalize
    if df.shape[1] == 1 and isinstance(df.iloc[0, 0], (dict, list)):
        try:
            return pd.json_normalize(df.iloc[:, 0])
        except Exception:
            return df
    return df


def list_data_files(ext: List[str] = None) -> List[Path]:
    """Return list of files under data/raw matching extensions (e.g. ['csv','json'])."""
    if ext is None:
        exts = ["csv", "json", "xlsx", "parquet", "txt"]
    else:
        exts = ext
    files = []
    for e in exts:
        files.extend(list(DATA_RAW.rglob(f"*.{e}")))
    return files


def save_processed(df: pd.DataFrame, name: str):
    """Save processed dataframe to data/processed as parquet and csv."""
    p_parq = DATA_PROCESSED / f"{name}.parquet"
    p_csv = DATA_PROCESSED / f"{name}.csv"
    df.to_parquet(p_parq, index=False)
    df.to_csv(p_csv, index=False)
    return p_parq, p_csv


def load_any(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    if p.suffix.lower() in [".csv"]:
        return safe_read_csv(path)
    if p.suffix.lower() in [".json"]:
        return safe_read_json(path, orient="records")
    if p.suffix.lower() in [".parquet"]:
        return pd.read_parquet(path)
    if p.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    # fallback: try pandas read_table
    return pd.read_table(path, low_memory=False)
