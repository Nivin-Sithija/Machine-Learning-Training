# Time Series Analysis of Daily Clinic Attendances

Worked analysis of a ~3-year daily clinic-attendance series (2022-01-03 to 2025-01-01):
decomposition, seasonality detection, anomaly flagging, and stationarity testing. Originally a
CS3621 (Data Mining) practical; kept here for the Part C code and results, which are original
analysis rather than course material.

## Contents

| Item | File |
|---|---|
| Analysis script (writes every plot to `partC_output/`) | [partC_analysis.py](partC_analysis.py) |
| Generated figures | [partC_output/](partC_output/) |
| Submitted answers (Parts A–D) | [Time-Series-Analysis-Report.pdf](Time-Series-Analysis-Report.pdf) |
| Dataset | [clinic_attendances.csv](clinic_attendances.csv) |

## What the script does

- **C1 — look first:** whole-series plot, first-eight-weeks zoom with weekends shaded,
  day-of-week attendance profile, and an additive-vs-multiplicative seasonality check (is the
  weekly swing proportional to the local level?).
- **C2 — periodogram:** peak frequencies in the de-trended series, and what changes if you skip
  de-trending first.
- **C3 — decomposition:** STL (robust vs non-robust), where the two trend estimates diverge most,
  and where a second (annual) seasonal component hides.
- **C4 — anomalies:** robust remainder z-score to flag incident dates, compared against a plain
  mean/std version to show how outliers distort the naive threshold.
- **C5 — stationarity:** two differencing routes (`log → diff(1) → diff(7)` vs `log → diff(7)`
  only) checked against ADF and KPSS, ACF at the first stage that passes both tests, and
  diagnostics for over-differencing.

## How to run

```
pip install numpy pandas matplotlib statsmodels
python partC_analysis.py
```

Reads `clinic_attendances.csv`, writes all figures to `partC_output/`, prints test statistics
and commentary to stdout.

## Notes

- The instructor-provided worksheet, reference notebook, and lecture slides were trimmed from
  this folder — they're course material, not original work. They remain in git history if
  needed.
