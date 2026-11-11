"""
Downloads the public datasets used by reasoning_agent.ipynb into ./data

    python download_data.py

RuleTaker and FOLIO are loaded with the `datasets` library and every split is
saved as JSON lines. CounterBench's files have different columns, so
load_dataset() cannot read them together; its two question files are
downloaded directly instead (the meta_model_*.json files are not needed).
"""
import os

from datasets import load_dataset
from huggingface_hub import hf_hub_download

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# RuleTaker (test split is the one evaluated) and FOLIO (train + validation)
for short_name, hf_id in [("ruletaker", "tasksource/ruletaker"), ("folio", "tasksource/folio")]:
    ds = load_dataset(hf_id)
    for split in ds:
        out_path = os.path.join(DATA_DIR, f"{short_name}_{split}.jsonl")
        ds[split].to_json(out_path)
        print(f"{short_name:13s} {split:12s} {len(ds[split]):7d} rows -> {out_path}")

# CounterBench
for file_name in ["data_balanced_alpha_V1.json", "data_balanced_backdoor_V2.json"]:
    path = hf_hub_download(repo_id="CounterBench/CounterBench", filename=file_name,
                           repo_type="dataset", local_dir=DATA_DIR)
    print(f"counterbench  {file_name:32s} -> {path}")

print("done - files needed by the notebook:")
for name in ["ruletaker_test.jsonl", "folio_train.jsonl", "folio_validation.jsonl",
             "data_balanced_alpha_V1.json", "data_balanced_backdoor_V2.json"]:
    status = "ok" if os.path.exists(os.path.join(DATA_DIR, name)) else "MISSING"
    print(f"  {status:7s} data/{name}")
