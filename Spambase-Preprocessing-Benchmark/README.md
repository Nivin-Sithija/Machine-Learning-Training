# Reviving Legacy Benchmarks: Principled Preprocessing on UCI Spambase

IEEE-format paper (N.S. Seneviratne, University of Moratuwa) arguing that on the 1999 UCI
Spambase corpus (4,601 emails, 57 features), **dataset quality — not model capacity — is the
dominant accuracy bottleneck**. A seven-stage preprocessing pipeline is applied and eight
classical classifiers are re-evaluated at each stage.

## Contents

| Item | File |
|---|---|
| Paper (XeLaTeX source, IEEE conference format) | [paper.tex](paper.tex) |
| Research notebooks (numbered, run in order) | [01_data_preparation.ipynb](01_data_preparation.ipynb) → [13_mislabeled_only_cleaning.ipynb](13_mislabeled_only_cleaning.ipynb) |
| Raw data + column-naming script | [spambase.data](spambase.data), [Spam.csv](Spam.csv), [create_csv.py](create_csv.py) |
| Duplicate-removed corpus used from notebook 11 onward | [spambase_clean.csv](spambase_clean.csv) |

**Building the paper:** `paper.tex` uses `fontspec` (Times New Roman) and must be compiled with
**XeLaTeX**, not `pdflatex`. No compiled PDF is checked in.

## Pipeline

1. Feature standardisation
2. Seven filter-based feature selection methods, compared
3. Log-transform skewness correction
4. Domain-driven interaction feature engineering
5. Duplicate-record removal
6. Bayesian hyperparameter optimisation (Optuna) across 5 gradient-boosting variants
7. Instance-hardness analysis: separate "atypical" (high-confidence model disagreement) from
   "borderline" (near decision boundary) hard cases, and clean only the former

## Result

- Baseline XGBoost, no preprocessing: **95.77%** accuracy.
- After filter-based feature selection: **96.55%**.
- Instance-hardness analysis flags 208 hard instances (4.9%): 143 atypical, 65 borderline. Only
  the 143 atypical instances are removed — the 65 borderline cases are kept, on the grounds that
  "near the boundary" isn't the same failure mode as "the label is probably wrong."
- A super-stacking ensemble of five Optuna-tuned gradient-boosting models, retrained on the
  cleaned corpus, reaches **97.79% accuracy** (F1 = 0.9722, AUC = 0.9987, MCC = 0.9540) — a
  +1.44 pp gain over the pre-cleaning best, with no architecture change.

## Notebook sequence

`01` data preparation → `02` baseline classifiers → `03` SMOTE evaluation → `04` feature
selection → `05` feature engineering → `06` Optuna + stacking → `07` statistical significance
testing → `08` further improvements → `09` error analysis → `10` instance-hardness analysis →
`11` cleaned pipeline → `12` cleaned pipeline without SMOTE → `13` mislabeled-instance-only
cleaning (the version reported in the paper).

## Notes

- This started as University of Moratuwa coursework and grew into the paper above; the notebook
  numbering reflects the actual order of investigation, including the dead ends (e.g. `03`/`12`
  show SMOTE was tried and dropped — oversampling didn't survive contact with cleaner data).
- Earlier full drafts, an archive of ~14 superseded experiment notebooks, and two third-party
  reference papers were trimmed from this folder; they remain in git history
  (`git log --diff-filter=D --summary`) if needed.
