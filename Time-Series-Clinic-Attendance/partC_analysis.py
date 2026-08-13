"""CS3621 L05 Practical - Part C worked solution.
Runs the whole hands-on pipeline and writes every plot into partC_output/.
"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf
import warnings
warnings.filterwarnings("ignore")

OUT = "partC_output/"
s = pd.read_csv("clinic_attendances.csv", parse_dates=[0], index_col=0).squeeze()
s.index.freq = "D"
print(f"{len(s)} rows, {s.index[0].date()} to {s.index[-1].date()}")
print(s.describe(), "\n")

# ---------------------------------------------------------------- C1. Look first
fig, ax = plt.subplots(figsize=(12, 3))
s.plot(ax=ax, lw=.7)
ax.set_title("C1.1  Whole series: daily clinic attendances, 2022-01-03 to 2025-01-01")
ax.set_ylabel("attendances"); fig.tight_layout(); fig.savefig(OUT+"C1_whole.png", dpi=130); plt.close(fig)

fig, ax = plt.subplots(figsize=(12, 3.2))
s.iloc[:56].plot(ax=ax, marker="o", ms=3.5, lw=1)
for d in s.index[:56][s.index[:56].dayofweek == 5]:
    ax.axvspan(d, d + pd.Timedelta(days=2), color="orange", alpha=.18)
ax.set_title("C1.1  First eight weeks (56 days) - weekends shaded")
ax.set_ylabel("attendances"); fig.tight_layout(); fig.savefig(OUT+"C1_first8weeks.png", dpi=130); plt.close(fig)

print("=== C1: day-of-week profile ===")
dow = s.groupby(s.index.dayofweek).mean()
dow.index = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
print(dow.round(1))
print("weekend/weekday ratio:", round(dow[["Sat","Sun"]].mean()/dow[:5].mean(), 3))

# C1.3 additive vs multiplicative: weekly range vs local level, by year-quarter
lvl = s.rolling(91, center=True).mean()
wk = s.resample("W")
tab = pd.DataFrame({"level": wk.mean(), "range": wk.max()-wk.min(), "std": wk.std()}).dropna()
tab = tab[(tab.index > s.index[7]) & (tab.index < s.index[-7])]
print("\n=== C1.3: is the weekly swing proportional to the level? ===")
print("corr(level, weekly range) =", round(tab.level.corr(tab.range), 3))
print("corr(level, weekly std)   =", round(tab.level.corr(tab["std"]), 3))
q = tab.assign(bin=pd.qcut(tab.level, 4, labels=["low","mid-lo","mid-hi","high"]))
print(q.groupby("bin", observed=True)[["level","range","std"]].mean().round(1))
g = q.groupby("bin", observed=True)
print("range/level by bin:", (g["range"].mean() / g["level"].mean()).round(3).to_dict())

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(tab.level, tab.range, s=12, alpha=.6)
m, b = np.polyfit(tab.level, tab.range, 1)
xx = np.linspace(tab.level.min(), tab.level.max(), 10)
ax.plot(xx, m*xx+b, "r--", label=f"slope={m:.2f} (>0 => multiplicative)")
ax.set_xlabel("weekly mean level"); ax.set_ylabel("weekly max - min")
ax.set_title("C1.3  Weekly swing grows with the level"); ax.legend()
fig.tight_layout(); fig.savefig(OUT+"C1_mult_evidence.png", dpi=130); plt.close(fig)

# ---------------------------------------------------------------- C2. Periodogram
y = s.values.astype(float)
yd = y - y.mean()
# the caveat from the lecture: de-trend, not just de-mean
trend_lin = np.polyval(np.polyfit(np.arange(len(y)), y, 1), np.arange(len(y)))
ydt = y - trend_lin

def pgram(v):
    p = np.abs(np.fft.rfft(v))**2 / len(v)
    f = np.fft.rfftfreq(len(v), 1.0)
    return f, p

f, P = pgram(ydt)
f0, P0 = pgram(yd)   # mean-removed only, for C2.2

def peaks(f, P, n=8, fmin=1/400):
    idx = [i for i in range(2, len(P)-1) if P[i] > P[i-1] and P[i] > P[i+1] and f[i] > fmin]
    idx.sort(key=lambda i: -P[i])
    return [(f[i], 1/f[i], P[i]) for i in idx[:n]]

print("\n=== C2.1: periodogram peaks (de-trended) ===")
print(f"{'freq (cyc/day)':>15} {'period (days)':>14} {'power':>14}")
for fr, per, pw in peaks(f, P):
    print(f"{fr:15.6f} {per:14.2f} {pw:14.1f}")

fig, axs = plt.subplots(1, 2, figsize=(12, 3.6))
axs[0].plot(f, P, lw=.8); axs[0].set_xlim(0, .5)
axs[0].set_xlabel("frequency (cycles/day)"); axs[0].set_ylabel("power")
axs[0].set_title("C2.1  Periodogram, de-trended (full band)")
for k, lab in [(1/7, "1/7"), (2/7, "2/7"), (3/7, "3/7"), (1/365.25, "1/365")]:
    axs[0].axvline(k, color="r", ls=":", lw=.8)
axs[1].plot(f, P, lw=.9); axs[1].set_xlim(0, .02); axs[1].set_yscale("log")
axs[1].axvline(1/365.25, color="r", ls=":", label="1/365.25 (annual)")
axs[1].set_xlabel("frequency (cycles/day)"); axs[1].set_title("C2.1  Low-frequency zoom (log power)")
axs[1].legend()
fig.tight_layout(); fig.savefig(OUT+"C2_periodogram.png", dpi=130); plt.close(fig)

print("\n=== C2.2: effect of skipping the de-trend ===")
lowband = f0 < 0.01
print("share of total power below f=0.01, mean-removed only:", round(P0[lowband].sum()/P0.sum(), 4))
print("share of total power below f=0.01, de-trended       :", round(P[f < 0.01].sum()/P.sum(), 4))
print("power at annual bin (k=3), mean-removed only:", round(P0[3], 1), " de-trended:", round(P[3], 1))
print("power at weekly peak,       mean-removed only:", round(P0[np.argmin(abs(f0-1/7))], 1),
      " de-trended:", round(P[np.argmin(abs(f-1/7))], 1))

fig, axs = plt.subplots(1, 2, figsize=(12, 3.4), sharey=True)
axs[0].plot(f0, P0, lw=.8); axs[0].set_xlim(0, .2)
axs[0].set_title("C2.2  Mean removed only (trend left in)")
axs[1].plot(f, P, lw=.8); axs[1].set_xlim(0, .2)
axs[1].set_title("C2.2  De-trended")
for a in axs: a.set_xlabel("frequency (cycles/day)")
axs[0].set_ylabel("power")
fig.tight_layout(); fig.savefig(OUT+"C2_detrend_effect.png", dpi=130); plt.close(fig)

# ---------------------------------------------------------------- C3. Decompose
res = STL(s, period=7, robust=True, seasonal=15, trend=181).fit()
fig = res.plot(); fig.set_size_inches(11, 8)
fig.suptitle("C3.1  STL(period=7, robust=True, seasonal=15, trend=181)", y=1.001)
fig.tight_layout(); fig.savefig(OUT+"C3_stl_robust.png", dpi=130); plt.close(fig)

resF = STL(s, period=7, robust=False, seasonal=15, trend=181).fit()
fig = resF.plot(); fig.set_size_inches(11, 8)
fig.suptitle("C3.2  STL with robust=False", y=1.001)
fig.tight_layout(); fig.savefig(OUT+"C3_stl_nonrobust.png", dpi=130); plt.close(fig)

d = (resF.trend - res.trend)
print("\n=== C3.2: where do the two trend estimates differ most? ===")
print("max |difference| =", round(abs(d).max(), 2), "on", d.abs().idxmax().date())
print("top 8 dates by |trend difference|:")
print(d.abs().sort_values(ascending=False).head(8).round(2))
for lab, sl in [("spike  2022-09-10", slice("2022-08-20", "2022-10-01")),
                ("frozen 2023-08-26..09-06", slice("2023-08-05", "2023-09-25")),
                ("ramp   2024-07-21..08-04", slice("2024-07-01", "2024-08-25"))]:
    print(f"  mean |diff| near {lab}: {abs(d[sl]).mean():.2f}")

fig, ax = plt.subplots(figsize=(12, 3.4))
res.trend.plot(ax=ax, label="robust=True", lw=1.4)
resF.trend.plot(ax=ax, label="robust=False", lw=1.4, ls="--")
for x in ["2022-09-10", "2023-08-26", "2024-07-28"]:
    ax.axvline(pd.Timestamp(x), color="r", ls=":", lw=.9)
ax.legend(); ax.set_title("C3.2  Trend: robust vs non-robust (red = injected faults)")
fig.tight_layout(); fig.savefig(OUT+"C3_trend_compare.png", dpi=130); plt.close(fig)

print("\n=== C3.3: where did the SECOND (annual) season go? ===")
tr = res.trend
print("trend min/max:", round(tr.min(), 1), round(tr.max(), 1), "range:", round(tr.max()-tr.min(), 1))
# annual wave should be visible inside the trend panel
ta = tr - tr.rolling(365, center=True).mean()
print("amplitude of 365-day wave sitting inside the TREND panel:", round(ta.std()*np.sqrt(2), 2))
rem_ = res.resid
ra = rem_.rolling(31, center=True).mean()
print("amplitude of any annual wave left in the REMAINDER:", round(ra.std()*np.sqrt(2), 2))
print("STL seasonal panel: 7-day period only. std =", round(res.seasonal.std(), 2))

fig, axs = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
tr.plot(ax=axs[0], lw=1.3); tr.rolling(365, center=True).mean().plot(ax=axs[0], lw=2, color="r",
        label="365-day mean (pure growth)")
axs[0].legend(); axs[0].set_title("C3.3  The annual season is riding inside the TREND panel")
ta.plot(ax=axs[1], lw=1.2, color="g")
axs[1].axhline(0, color="k", lw=.6)
axs[1].set_title("C3.3  Trend minus its own 365-day mean: the annual wave, isolated")
fig.tight_layout(); fig.savefig(OUT+"C3_second_season.png", dpi=130); plt.close(fig)

# ---------------------------------------------------------------- C4. Anomalies
rem = s - res.seasonal - res.trend
mad = 1.4826 * np.median(np.abs(rem - rem.median()))
z = (rem - rem.median()) / mad
print("\n=== C4: robust remainder z-score ===")
print("median(rem) =", round(rem.median(), 3), "  MAD-sigma =", round(mad, 3))

def incidents(dates, gap=3):
    out = []
    for dt in sorted(dates):
        if out and (dt - out[-1][-1]).days <= gap:
            out[-1].append(dt)
        else:
            out.append([dt])
    return out

for thr in [3, 4, 5, 6]:
    fl = s.index[np.abs(z) > thr]
    inc = incidents(list(fl))
    print(f"\n--- threshold {thr}: {len(fl)} days flagged, {len(inc)} incidents ---")
    for g in inc:
        a, b = g[0].date(), g[-1].date()
        zz = z[g[0]:g[-1]]
        print(f"   {a} .. {b}  ({len(g):2d} d)  z range [{zz.min():7.2f},{zz.max():7.2f}]"
              f"  dow={sorted({d.day_name()[:3] for d in g})}")

print("\n=== C4 flagged dates at threshold 5, with values ===")
fl5 = s.index[np.abs(z) > 5]
for dt in fl5:
    print(f"  {dt.date()} {dt.day_name()[:3]}  y={s[dt]:4d}  fitted={res.trend[dt]+res.seasonal[dt]:7.1f}"
          f"  rem={rem[dt]:8.2f}  z={z[dt]:7.2f}")

# C4.4 mean/std version
z2 = (rem - rem.mean()) / rem.std()
print("\n=== C4.4: same thing with mean and std (masking) ===")
print(f"rem.mean()={rem.mean():.3f}  rem.std()={rem.std():.3f}   vs median={rem.median():.3f} MADsig={mad:.3f}")
print(f"std/MADsigma inflation factor = {rem.std()/mad:.2f}x")
rows = []
for thr in [3, 4, 5, 6]:
    a = int((np.abs(z) > thr).sum()); b = int((np.abs(z2) > thr).sum())
    rows.append((thr, a, b))
print(f"{'thr':>4} {'robust flags':>13} {'mean/std flags':>15}")
for t, a, b in rows: print(f"{t:>4} {a:>13} {b:>15}")
print("\nper-incident survival under mean/std at threshold 5:")
for name, sl in [("spike 2022-09-10", ("2022-09-10","2022-09-10")),
                 ("frozen 2023-08-26..09-06", ("2023-08-26","2023-09-06")),
                 ("Sunday 2024-05-05", ("2024-05-05","2024-05-05")),
                 ("ramp 2024-07-21..08-04", ("2024-07-21","2024-08-04"))]:
    seg = slice(*sl)
    print(f"   {name:26s} robust {(np.abs(z[seg])>5).sum():2d}/{len(z[seg]):2d}"
          f"   mean-std {(np.abs(z2[seg])>5).sum():2d}/{len(z2[seg]):2d}")

fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
s.plot(ax=axs[0], lw=.6); axs[0].scatter(fl5, s[fl5], color="r", s=22, zorder=5)
axs[0].set_title("C4  Raw series with threshold-5 flags")
rem.plot(ax=axs[1], lw=.6, color="grey"); axs[1].scatter(fl5, rem[fl5], color="r", s=22, zorder=5)
axs[1].set_title("C4  STL remainder")
z.plot(ax=axs[2], lw=.6, label="robust (median/MAD)")
z2.plot(ax=axs[2], lw=.6, color="orange", label="mean/std")
for t in [3, 5]:
    axs[2].axhline(t, color="r", ls=":", lw=.7); axs[2].axhline(-t, color="r", ls=":", lw=.7)
axs[2].legend(); axs[2].set_title("C4.4  Robust z vs mean/std z - masking")
fig.tight_layout(); fig.savefig(OUT+"C4_anomalies.png", dpi=130); plt.close(fig)

fig, axs = plt.subplots(1, 4, figsize=(16, 3.2))
for ax, (t, sl) in zip(axs, [("spike", slice("2022-08-25","2022-09-25")),
                             ("frozen", slice("2023-08-10","2023-09-20")),
                             ("contextual Sunday", slice("2024-04-20","2024-05-20")),
                             ("ramp", slice("2024-07-05","2024-08-20"))]):
    s[sl].plot(ax=ax, marker="o", ms=3, lw=.9)
    f_ = [d for d in fl5 if sl.start <= str(d.date()) <= sl.stop]
    if f_: ax.scatter(f_, s[f_], color="r", s=30, zorder=5)
    ax.set_title(t, fontsize=10); ax.tick_params(labelsize=7)
fig.suptitle("C4  The four injected faults, close up")
fig.tight_layout(); fig.savefig(OUT+"C4_four_faults.png", dpi=130); plt.close(fig)

# ---------------------------------------------------------------- C5. Stationarity
def tests(v, name):
    v = pd.Series(v).dropna()
    a = adfuller(v, autolag="AIC")[1]
    k = kpss(v, regression="c", nlags="auto")[1]
    return dict(stage=name, n=len(v), adf_p=a, kpss_p=k,
                adf=("PASS" if a < .05 else "fail"), kpss=("PASS" if k > .05 else "fail"),
                both=("YES" if (a < .05 and k > .05) else "no"),
                var=float(np.var(v, ddof=1)), acf1=float(pd.Series(v).autocorr(1)))

logs = np.log(s)
r1 = {"raw": s, "log": logs, "log+diff1": logs.diff(), "log+diff1+seas7": logs.diff().diff(7)}
r2 = {"raw": s, "log": logs, "log+seas7 (no d1)": logs.diff(7)}

print("\n=== C5.1: route A - raw -> log -> diff(1) -> diff(7) ===")
print(f"{'stage':<22}{'n':>6}{'ADF p':>10}{'KPSS p':>10}{'ADF':>7}{'KPSS':>7}{'both?':>7}")
rowsA = []
for k_, v in r1.items():
    r = tests(v, k_); rowsA.append(r)
    print(f"{r['stage']:<22}{r['n']:>6}{r['adf_p']:>10.4f}{r['kpss_p']:>10.4f}{r['adf']:>7}{r['kpss']:>7}{r['both']:>7}")

print("\n=== C5.3: route B - raw -> log -> diff(7) only ===")
print(f"{'stage':<22}{'n':>6}{'ADF p':>10}{'KPSS p':>10}{'ADF':>7}{'KPSS':>7}{'both?':>7}")
rowsB = []
for k_, v in r2.items():
    r = tests(v, k_); rowsB.append(r)
    print(f"{r['stage']:<22}{r['n']:>6}{r['adf_p']:>10.4f}{r['kpss_p']:>10.4f}{r['adf']:>7}{r['kpss']:>7}{r['both']:>7}")

# C5.2 ACF at the first stage that passes both
first = next(r["stage"] for r in rowsA if r["both"] == "YES")
print(f"\n=== C5.2: first stage passing BOTH on route A = '{first}' ; its ACF ===")
series_first = r1[first].dropna()
from statsmodels.tsa.stattools import acf as acf_fn
a1 = acf_fn(series_first, nlags=30, fft=True)
band = 1.96/np.sqrt(len(series_first))
print(f"95% band = +/- {band:.4f}")
for lg in [1, 2, 3, 6, 7, 8, 13, 14, 21, 28]:
    print(f"  lag {lg:2d}: {a1[lg]:+.3f} {'  <-- OUTSIDE band' if abs(a1[lg]) > band else ''}")

fig, axs = plt.subplots(1, 2, figsize=(13, 3.6))
plot_acf(series_first, lags=30, ax=axs[0], zero=False)
axs[0].set_title(f"C5.2  ACF of '{first}' (route A)")
plot_acf(r1["log+diff1+seas7"].dropna(), lags=30, ax=axs[1], zero=False)
axs[1].set_title("C5.2  ACF of log+diff1+seas7")
fig.tight_layout(); fig.savefig(OUT+"C5_acf.png", dpi=130); plt.close(fig)

fig, axs = plt.subplots(1, 2, figsize=(13, 3.6))
plot_acf(r2["log+seas7 (no d1)"].dropna(), lags=30, ax=axs[0], zero=False)
axs[0].set_title("C5.3  ACF route B: log + seasonal diff 7 only")
plot_acf(r1["log+diff1+seas7"].dropna(), lags=30, ax=axs[1], zero=False)
axs[1].set_title("C5.4  ACF route A: log + d1 + seasonal diff 7")
fig.tight_layout(); fig.savefig(OUT+"C5_acf_routes.png", dpi=130); plt.close(fig)

print("\n=== C5.4: over-differencing diagnostics ===")
A = r1["log+diff1+seas7"].dropna(); B = r2["log+seas7 (no d1)"].dropna()
print(f"{'route':<34}{'variance':>14}{'lag-1 ACF':>12}")
print(f"{'A: log + d1 + D7':<34}{np.var(A, ddof=1):>14.6f}{A.autocorr(1):>12.3f}")
print(f"{'B: log + D7 only':<34}{np.var(B, ddof=1):>14.6f}{B.autocorr(1):>12.3f}")
print(f"variance ratio A/B = {np.var(A,ddof=1)/np.var(B,ddof=1):.2f}")

fig, axs = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
B.plot(ax=axs[0], lw=.5); axs[0].set_title(f"C5.4  Route B (log + D7): var={np.var(B,ddof=1):.5f}, lag1 ACF={B.autocorr(1):+.3f}")
A.plot(ax=axs[1], lw=.5, color="darkred"); axs[1].set_title(f"C5.4  Route A (log + d1 + D7): var={np.var(A,ddof=1):.5f}, lag1 ACF={A.autocorr(1):+.3f}")
fig.tight_layout(); fig.savefig(OUT+"C5_routes.png", dpi=130); plt.close(fig)

# extra: what the trend really looks like (for C5.4's last sub-question)
print("\n=== C5.4 supporting: shape of the trend ===")
yr = s.resample("YE").mean()
print("annual means:", yr.round(1).to_dict())
h1 = res.trend[:len(res.trend)//2]; h2 = res.trend[len(res.trend)//2:]
print(f"trend rise in first half: {h1.iloc[-1]-h1.iloc[0]:+.1f}   second half: {h2.iloc[-1]-h2.iloc[0]:+.1f}")
print("\nAll plots written to", OUT)
