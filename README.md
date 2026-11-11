# Classical Reasoning Agent for Logical Entailment

**Akanksha Tiwari — Roll No. P26AI0002**  ·  AI Assignment (CSL7610)

The agent reads a knowledge base in English (*context*) and a *statement*, converts them into an internal logical
representation with hand-written parsers, and decides **True** (entailed) or **False** (contradicted or unknown) using
classical reasoning only: forward chaining with unification and stratified negation-as-failure, abduction–intervention–
propagation over causal models, and resolution refutation for first-order logic. No learned or generative model is
used for any prediction.

## Results (public data, as reported in `report.pdf`)

| Dataset | Queries | Accuracy | Inference time per sample |
|---|---:|---:|---:|
| RuleTaker (test) | 151,911 | 99.97% | 0.87 ms |
| FOLIO (validation, with FOL annotation) | 203 | 84.73% | 38.5 ms |
| CounterBench (alpha + backdoor) | 1,200 | 94.58% | 0.40 ms |
| **Average over the three datasets** | | **93.09%** | **13.26 ms = 0.0133 s** |

* `submission.csv` (all 153,314 public evaluation queries together): 99.91% in 141.3 s.
* FOLIO from the English text only (annotation hidden): 66.50% (always-False baseline 64.53%).
* Times are wall-clock times of the notebook on a laptop CPU (single thread, pure Python); they vary between machines.

## Repository contents

| File | Purpose |
|---|---|
| `reasoning_agent.ipynb` | complete implementation, evaluation, experiments, reasoning traces; writes `submission.csv` |
| `report.pdf` | representation, algorithms, experiments, traces |
| `submission.csv` | predictions `id,label` for the public evaluation queries |
| `README.txt` | run instructions submitted with the assignment |
| `download_data.py` | downloads the public datasets into `data/` |
| `requirements.txt` | Python packages |

## Reproduce

```bash
# 1. environment (tested with Python 3.11)
conda create -n ai_assign python=3.11 -y
conda activate ai_assign
pip install -r requirements.txt

# 2. data (creates data/ next to the notebook)
python download_data.py

# 3. run
jupyter notebook reasoning_agent.ipynb      # Kernel -> Restart & Run All (about 6-7 minutes)
```

The notebook prints accuracy and inference time for every dataset, the experiments and the traces, and writes
`submission.csv`. Expected files in `data/`: `ruletaker_test.jsonl`, `folio_train.jsonl`, `folio_validation.jsonl`,
`data_balanced_alpha_V1.json`, `data_balanced_backdoor_V2.json`.

**Private / new test file:** set `TEST_FILE = "your_file.csv"` in the first code cell and run all cells. Accepted formats
are CSV, JSON and JSON lines with columns `id`, `context` (or `premises` / `given_info`), `statement` (or `question` /
`conclusion`), and optionally `label` / `flag` / `answer` (then accuracy is printed). The public data is optional for this.

## How it works

| Input | Representation | Reasoning |
|---|---|---|
| RuleTaker-style rules | literals and rules with variables | forward chaining + unification, stratified negation as failure (`CLOSED_WORLD = True`) |
| CounterBench causal stories | boolean structural equations | abduction by enumeration, intervention, propagation in topological order |
| FOLIO with FOL annotation | CNF clauses after Skolemisation | resolution refutation (set of support, unit preference) |
| Other English | own English → FOL translation | same resolution prover |

Details, ablations and traces are in `report.pdf`.
