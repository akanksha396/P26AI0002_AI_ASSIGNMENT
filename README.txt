Reasoning Agent - AI Assignment
Akanksha Tiwari, Roll No. P26AI0002
================================

Files
-----
reasoning_agent.ipynb  complete implementation (parsers + reasoning engines + evaluation)
submission.csv         predictions (columns: id,label) written by the last notebook cell
report.pdf             short report (representation, algorithms, experiments, traces)
README.txt             this file

Environment
-----------
Tested with Python 3.11 and pandas 2.x (Windows, Anaconda environment).
Only pandas and the Python standard library are used by the notebook.
    conda create -n ai_assign python=3.11 -y
    conda activate ai_assign
    pip install pandas notebook datasets      (datasets: only for downloading the data)

Getting the public data (once)
------------------------------
Source (Hugging Face)          split(s) used               file(s) expected in data/
tasksource/ruletaker           test (151,911)              ruletaker_test.jsonl
tasksource/folio               train (1,001), validation (203)
                                                           folio_train.jsonl, folio_validation.jsonl
CounterBench/CounterBench      all (1,000 + 200)           data_balanced_alpha_V1.json,
                                                           data_balanced_backdoor_V2.json

RuleTaker and FOLIO: download with the `datasets` package and save each split as JSON lines,
e.g. from the project folder:
    python -c "from datasets import load_dataset as L; d=L('tasksource/ruletaker'); d['test'].to_json('data/ruletaker_test.jsonl')"
    python -c "from datasets import load_dataset as L; d=L('tasksource/folio'); [d[s].to_json(f'data/folio_{s}.jsonl') for s in d]"
(to_json writes one JSON object per line; no other preprocessing is done.)
CounterBench: its files have different columns, so load_dataset fails on it. Download the two
data_balanced_*.json files directly from the repository's "Files" tab (or copy them from the
Hugging Face cache) into data/. The two meta_model_*.json files are not used.

Folder layout
-------------
<project>/
    data/        the five files listed above
    submission/  reasoning_agent.ipynb, README.txt, report.pdf, submission.csv
DATA_DIR in the first code cell looks for ../data (or ./data).

How to run
----------
1. Open reasoning_agent.ipynb and choose Kernel -> Restart & Run All (about 6-7 minutes).
2. Printed: accuracy and inference time per dataset, accuracy by depth / question type,
   experiments (ablations, FOLIO with and without FOL annotation) and reasoning traces.
3. The last cell writes submission.csv (id,label; labels True/False). With TEST_FILE = None it
   predicts the 153,314 public evaluation queries (RuleTaker test 151,911 + FOLIO validation 203
   + CounterBench 1,200).

Evaluator input interface (private test set)
--------------------------------------------
The private test set is not released to students; TEST_FILE is the hook for the evaluator.
Set TEST_FILE in the setup cell to the test file (.csv, .json or .jsonl) and run all cells.
The public data is optional: without ../data the evaluation sections are skipped and the
notebook still writes submission.csv for TEST_FILE.
Recognised columns: id; context / premises / given_info; statement / question / conclusion;
optional label / flag / answer (accuracy is then printed); optional premises-FOL / conclusion-FOL.
Premises may be one text or a list of sentences. A file without a context or statement column
stops with a message listing the accepted column names.
Label mapping: entailed -> True; contradicted or unknown -> False.

Semantics setting
-----------------
CLOSED_WORLD = True (setup cell): for rule-style knowledge bases a negated literal holds when its
positive form cannot be derived (negation as failure). RuleTaker is built under this assumption
(99.94% closed world vs 75.11% open world on a 10,000-query sample). Set it to False for
open-world entailment, where "not P" must be stated or derived explicitly. FOL / English-to-FOL
resolution is always open world.

Routing (which engine answers a query)
--------------------------------------
1. "Would Y occur ..." question over "... causes ..." text -> causal engine
   (abduction by enumeration, intervention, forward propagation)
2. FOL annotation given -> resolution prover
3. Context fully parsed by the rule templates -> forward chaining with unification and
   stratified negation-as-failure (closed world)
4. Other English -> own English-to-FOL translation of the supported patterns -> resolution
5. Nothing usable -> False (not entailed)
No generative model is used for any prediction.
