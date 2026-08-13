"""Content for the CS3621 L05 answers report.

Blocks are tuples:
  ("part", text)             part banner, bold Times New Roman 14
  ("q", text)                question, verbatim from the worksheet, bold TNR 14
  ("a", text)                answer paragraph, TNR 12
  ("img", filename, caption) figure from partC_output/
  ("table", [rows])          first row is the header
"""

TITLE = "CS3621 Data Mining - Lecture 05 Practical"
SUBTITLE = ""

BLOCKS = [

# ------------------------------------------------------------------ PART A
("part", "Part A"),

("q", "A1. What is each series made of?\n"
      "Four series, each 20 years of monthly data. For each of A, B, C and D, write down: "
      "(1) which components are present: trend, seasonality, cycle, or none of them; "
      "(2) if there is seasonality, is it additive or multiplicative, and how can you tell from the picture alone; "
      "(3) one sentence on what kind of real quantity might behave that way."),
("table", [
    ["Series", "Components", "Additive or multiplicative", "Real quantity"],
    ["A", "Trend + 12-month seasonality + noise. No cycle.",
     "Additive. Rulers along the peaks and troughs come out parallel: the level rises, the swing does not.",
     "Monthly electricity use in a growing town, where each winter adds a fixed number of heating units."],
    ["B", "Trend + very strong 12-month seasonality + noise. No cycle.",
     "Multiplicative. The rulers fan apart, late cycles about twice as tall as early ones, so the swing grows in "
     "proportion to the level.",
     "Monthly airline passengers or retail sales, where December is +30% on whatever the business is doing."],
    ["C", "Cycle + noise only. No trend (2006 and 2025 sit at the same level), no seasonality.",
     "Does not apply. The oscillations differ in both length and depth, which is what disqualifies them from being "
     "seasonal.",
     "A manufacturing new-orders index, swinging with the business cycle at intervals nobody can diarise."],
    ["D", "A wandering stochastic trend. No seasonality, no fixed period at all.",
     "Does not apply. Long smooth excursions (down to 2014, up to 2022, a dip, then up) with high short-run "
     "persistence.",
     "An exchange rate or commodity price index, where each move builds on the last."],
]),

("q", "A2. Match each series to its ACF\n"
      "Here are the four autocorrelation functions of those same four series, in a scrambled order. "
      "Match i, ii, iii, iv to A, B, C, D. For each match, give the one visual feature that settles it. "
      'Answers of the form "it just looks like it" score nothing.'),
("table", [
    ["ACF", "Series", "The one visual feature that settles it"],
    ["i", "C", "Goes clearly negative (about -0.49 near lag 7), then oscillates with decaying humps that die by lag "
                "30. Negative autocorrelation is mean reversion, so it is stationary, ruling out A, B and D."],
    ["ii", "A", "Slow decay that stays positive to lag 40 (1.00 to 0.46) with only a faint ripple near lags 12, 24 and "
                "36. Slow positive decay means trend, and the weak ripple means the trend dominates the season."],
    ["iii", "D", "An almost perfectly straight smooth decay, no bumps at all, never negative. The total absence of a "
                 "ripple is the discriminator."],
    ["iv", "B", "Large humps on lags 12, 24 and 36 with deep dips to about 0.1 between them, so seasonality of period "
                "12 dominates the trend."],
]),
("a", "The ripple separates ii from iii, and its depth separates ii from iv."),

("q", "A3. Which are stationary?\n"
      "For each of P, Q, R and S: stationary, yes or no? If no, state which of the three conditions fails, and what "
      "you would do about it. Then the harder half of the question. Below are the p-values from the two tests. For two "
      "of these four the tests agree with your eyes, and for two they do not. Explain each disagreement."),
("table", [
    ["Series", "Stationary?", "Which condition fails", "What I would do"],
    ["P", "Yes", "None. Flat level, constant spread, no repeating pattern.", "Nothing. Model it as it stands."],
    ["Q", "No", "Condition 3: a strong regular oscillation, so the expected value depends on where you are in the "
                "cycle.", "Seasonally difference at the period of the oscillation. Read the period off the ACF or "
                "periodogram first."],
    ["R", "No", "Condition 2: the mean is flat but the spread widens steadily from left to right.",
           "Stabilise the variance with a log or Box-Cox transform, then re-check with a rolling-variance plot."],
    ["S", "No", "Condition 1: a step change, high for the first half then abruptly low.",
           "Difference it, or better, find the break point and use a step dummy or analyse the two regimes separately."],
]),
("a", "Series Q. Neither test looks for periodic structure: ADF asks only whether shocks persist, and a bounded "
      "oscillation always comes back, so it rejects at p < 0.001, while KPSS asks whether the level drifts and Q's "
      "level is flat, so it returns its ceiling of 0.10. The ACF or periodogram is what catches it."),
("a", "Series R. Both tests are built from the level and neither inspects the variance, so R's constant mean earns a "
      "clean bill while its spread grows visibly. A rolling standard deviation plot catches it. ADF and KPSS together "
      "certify the level and nothing else, which recurs in B4 and in C5.2."),

("q", "A4. Read the periodogram\n"
      "1. How many periodic components are in this series, and what is the period of each? Show the arithmetic. "
      "2. Only one of them is visible to the eye in the left-hand panel. Which, and why is the other one so hard to "
      "see there? 3. If these were monthly observations, would you call either of these components seasonality? "
      "Justify."),
("table", [
    ["Peak", "Frequency (cycles/obs)", "Arithmetic", "Period"],
    ["small, left", "0.0083", "T = 1 / 0.0083", "about 120 observations"],
    ["tall, centre", "0.083", "T = 1 / 0.083", "about 12 observations"],
]),
("a", "1. Two components, since period is the reciprocal of frequency. Harmonics of a 12-period wave would land to the "
      "right of the tall peak (1/6, 1/4, 1/3), not to its left, so the low-frequency peak is genuine."),
("a", "2. Only the 12-observation component is visible. The 240-observation window holds exactly two cycles of a "
      "120-period wave, and two repetitions do not read as a rhythm; the slow component is also about five times "
      "weaker and the eye files slow smooth movement under trend. The periodogram projects the whole record onto every "
      "frequency at once instead of counting repetitions."),
("a", "3. The 12-month component is seasonality: a fixed period, known in advance, locked to the calendar. The "
      "120-month component is a cycle, since ten years matches no calendar unit and real components at that scale run "
      "8 to 13 years."),

("q", "A5. Judge the remainder\n"
      "Two people decompose the same series and show you the remainder from their model. Which model is finished, and "
      "which is not? Name every piece of evidence you can see, and for the unfinished one say specifically what "
      "structure has been left behind and roughly what its period is."),
("a", "Model 1 is finished. Its remainder is a structureless band around zero with constant width, every ACF spike "
      "from lag 1 lies inside the band, the distribution is single-peaked and symmetric about zero, and the scale is "
      "small at about plus or minus 2.5."),
("a", "Model 2 is not. It still oscillates visibly; its ACF has huge alternating spikes far outside the band that do "
      "not decay out to lag 30, which is a leftover deterministic wave rather than an AR or MA process; its "
      "distribution is bimodal, because a sinusoid spends most of its time near its turning points; and its spread is "
      "about 60% wider."),
("a", "What was left behind is a fixed-period seasonal component. ACF peaks sit at lags 7, 14, 21 and 28 (+0.68, "
      "+0.65, +0.66, +0.60) with the deepest negatives midway between, so the period is about 7 observations, a weekly "
      "cycle for daily data. Re-run the decomposition with period 7, or seasonally difference at lag 7."),

# ------------------------------------------------------------------ PART B
("part", "Part B"),

("q", "B1. The shuffle test, in your own words\n"
      "In the lecture we shuffled the airline series and the histogram did not change at all. Explain, in no more than "
      "four sentences, why no statistic computed from the histogram can ever detect the difference, and name one "
      "statistic that can."),
("a", "A histogram records only how many times each value occurred, so the position of each observation on the time "
      "axis is thrown away the moment the bars are drawn. Shuffling is a permutation, which changes only the order and "
      "leaves the multiset of values, and every bar height, exactly as it was. Any statistic computed from the "
      "histogram is a function of those counts alone, so the mean, variance, skewness, kurtosis, quantiles, min and "
      "max must all return identical answers by construction. The lag-1 autocorrelation can tell them apart, because "
      "it is computed from neighbouring pairs and so reads the ordering the histogram discarded."),

("q", "B2. Season or cycle?\n"
      "Classify each of the following as seasonality, a cycle, or neither, and give the one-line test you applied. "
      "1. Ice cream sales, monthly, in Colombo. 2. The number of sunspots, annually, with peaks roughly 11 years "
      "apart. 3. Electricity demand, hourly, over one month. 4. The price of rice after a drought year. "
      "5. Hospital admissions on the day after a public holiday. 6. The boom and bust of the semiconductor industry, "
      "roughly every 4 to 6 years."),
("a", "The test throughout: is the period fixed, known in advance, and locked to the calendar or clock?"),
("table", [
    ["#", "Series", "Answer", "Test applied"],
    ["1", "Ice cream sales, monthly, Colombo", "Seasonality",
     "Fixed at 12 months and locked to the calendar. Small amplitude in a tropical climate does not disqualify it; "
     "only a variable period would."],
    ["2", "Sunspots, peaks about 11 years apart", "Cycle",
     "\"Roughly\" is the answer. Cycles run 9 to 13 years, tied to solar dynamics rather than a calendar."],
    ["3", "Electricity demand, hourly, one month", "Seasonality",
     "Two of them, both clock-locked: 24 hours and 168 hours. Multiple seasonal periods in one series is normal, and "
     "is the situation in Part C."],
    ["4", "Rice price after a drought year", "Neither",
     "A one-off response to an external shock, with no period. Model it as an intervention with a dummy."],
    ["5", "Admissions after a public holiday", "Neither",
     "A calendar-event effect. Holidays fall on irregular moving dates, so there is no fixed spacing, but they are "
     "predictable from a calendar, unlike a cycle. Use a holiday dummy."],
    ["6", "Semiconductor boom and bust, 4 to 6 years", "Cycle",
     "The question states a variable period. Driven by investment and inventory dynamics, with length and amplitude "
     "varying between occurrences."],
]),

("q", "B3. Why did differencing not finish the job?\n"
      "On the airline data we took logs and then one difference, and the ADF p-value was still 0.071. Explain what was "
      "still in the series, why a first difference cannot remove it, and what does remove it. Be precise about which "
      "lag is involved and why."),
("a", "The 12-month seasonality was still there. The log fixed the growing amplitude and the difference removed the "
      "trend, but the expected value still depends on which month it is, so ADF still sees structure at p = 0.071."),
("a", "A first difference cannot remove it because for y(t) = T(t) + S(t) + e(t) with S periodic, the differenced "
      "series contains S(t) - S(t-1), and January's seasonal level differs from December's, so nothing cancels. Worse, "
      "S(t) - S(t-1) is itself periodic with period 12: differencing a wave gives another wave of the same period. One "
      "difference annihilates a degree-one polynomial in t, never a periodic function."),
("a", "A seasonal difference at lag 12 removes it, because periodicity means S(t) = S(t-12) exactly, so the two terms "
      "are identical and cancel; you compare January with January. Any other lag compares mismatched positions in the "
      "cycle, and lags 24 or 36 would cancel too but discard more data. The full recipe is log, d = 1, then D = 1 at "
      "lag 12, which is SARIMA(0,1,1)(0,1,1)12."),

("q", "B4. The test that was wrong\n"
      "You are given a series whose mean is dead flat but whose swings get visibly wider every year. ADF returns "
      "p < 0.001. Your project partner writes \"ADF confirms the series is stationary, so we proceeded to fit ARIMA\". "
      "Write the two-sentence correction you would put in the review comments."),
("a", "ADF tests one thing only, whether there is a unit root in the level, so p < 0.001 tells us the mean is stable "
      "and says nothing about the variance, which here widens visibly every year. Stationarity requires constant "
      "variance as well as constant mean, so stabilise it first with a log or Box-Cox transform, then re-run ADF "
      "alongside KPSS and inspect the ACF and a rolling standard deviation plot before fitting anything."),

("q", "B5. Order of operations\n"
      "Why do we stabilise the variance before we remove the trend, and not the other way round? Give a concrete "
      "reason, not \"because the slides said so\"."),
("a", "The transform is non-linear and differencing is linear, so the two do not commute. For a multiplicative series "
      "y(t) = T(t) S(t) e(t), the log turns the products into sums, giving additive noise of constant spread, so one "
      "difference then leaves a residual whose variance is the same in year ten as in year one."),
("a", "Differencing first leaves every term multiplied by the current level, so a 5% wobble is 5 units early and 50 "
      "units late and the growing variance survives in full. A log afterwards cannot rescue it: a differenced series "
      "contains negative values, where the log is undefined, and the multiplicative structure lives in the levels that "
      "differencing has already destroyed."),

("q", "B6. The anomaly a threshold cannot find\n"
      "A clinic records 165 attendances on a Sunday. The lowest weekday count all year is 168 and the highest is 260, "
      "so 165 is not an extreme value in any global sense. Yet it is a serious anomaly. 1. Which of the three kinds of "
      "anomaly is this? 2. Explain why no threshold applied to the raw series can catch it, however cleverly you "
      "choose the threshold. 3. Describe, in two steps, a procedure that does catch it."),
("a", "1. A contextual anomaly: the value is ordinary globally and it is a single observation, so it is neither a "
      "point nor a collective anomaly. It is abnormal only as a Sunday."),
("a", "2. A raw threshold is a pair of horizontal lines, so it is a function of the value alone. Put the upper line "
      "below 165 and you flag every weekday of the year; put it above 260 and 165 passes. There is no line in between, "
      "because you would need 165 to be too high while 168 to 260 is fine. The information that makes it anomalous, "
      "the day of week, is not on the y-axis, which also disposes of percentile thresholds, global z-scores and IQR "
      "fences."),
("a", "3. Step 1: decompose with STL at period 7 and form rem = y - trend - seasonal, so each day becomes a deviation "
      "from what its own weekday should have been; the Sunday's expectation is about 55, so its remainder is roughly "
      "+110. Step 2: flag |z| > 4 or 5 on z = (rem - median(rem)) / (1.4826 * MAD(rem)), using median and MAD so the "
      "anomalies cannot inflate the scale and hide behind it. Step 1 moved the missing dimension onto the y-axis, so a "
      "one-dimensional threshold now works."),

# ------------------------------------------------------------------ PART C
("part", "Part C"),

("q", "C1. Look first\n"
      "1. Plot the whole series, then plot only the first eight weeks. What do you see in the second plot that is "
      "invisible in the first? 2. Write two sentences naming every component you can identify, with the period of "
      "each. 3. Is the seasonality additive or multiplicative here? Give the evidence."),
("img", "C1_whole.png", "The whole series. The level rises, but 1,095 daily points compressed into a few inches render as a solid band."),
("img", "C1_first8weeks.png", "The first eight weeks (56 days), weekends shaded. The smear resolves into a repeating weekly shape."),
("a", "1. The weekly cycle and its shape. At full-series resolution 156 weeks are squeezed into about 12 inches, "
      "roughly one week every 2 mm, so the oscillation renders as solid ink and looks like noise. Zoomed in it is a "
      "regular deterministic pattern: five high weekdays declining from a Monday peak to Friday, then a cliff on "
      "Saturday and a bottom on Sunday."),
("table", [
    ["Day", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    ["Mean attendances", "183.8", "169.6", "164.3", "162.6", "153.6", "66.6", "55.4"],
]),
("a", "2. The series has a rising but decelerating trend (annual means 120.5, 140.0, 149.3, so a gain of 19.5 in the "
      "second year and only 9.3 in the third) and a very strong weekly seasonality of period 7 days. On top sits a "
      "weaker annual seasonality of period about 365 days (amplitude around 17, roughly 12% of the level, peaking "
      "mid-year), multiplicative noise of 5 to 6%, and the four anomalies found in C4."),
("img", "C1_mult_evidence.png", "Each point is one week: peak-to-trough range against mean level. The positive slope is the multiplicative signature."),
("a", "3. Multiplicative. The swing grows with the level, corr(level, weekly range) = 0.635 and corr(level, weekly SD) "
      "= 0.659, where an additive model gives roughly zero by construction."),
("table", [
    ["Level bucket", "Mean level", "Mean weekly range", "Range / level"],
    ["low", "114.1", "111.6", "0.978"],
    ["mid-low", "128.2", "123.6", "0.964"],
    ["mid-high", "141.5", "137.2", "0.970"],
    ["high", "163.9", "150.5", "0.919"],
]),
("a", "The absolute range rises 35% across the buckets while the ratio stays near 0.95, and Sunday sits at about 0.30 "
      "of Monday throughout rather than at Monday minus 128 patients. So logs come first, which makes the model "
      "additive and stabilises the variance in one step."),

("q", "C2. Find the periods without assuming them\n"
      "Compute the periodogram. Remember the caveat from the lecture about what you must do to the series first. "
      "1. Which periods does it find? Report them in days, and say what each one means in plain English. "
      "2. What happens to the plot if you skip the de-trending step? Try it and describe the difference in one "
      "sentence."),
("a", "The caveat: de-trend before the FFT, not merely subtract the mean. A trend is a very low frequency, very high "
      "energy component, and leaving it in dumps power into the lowest bins and leaks across their neighbours, which "
      "is where a long-period seasonal component lives. Below, a fitted straight line has been removed as well."),
("img", "C2_periodogram.png", "Left: the full band with the weekly fundamental and its harmonics marked. Right: the low-frequency zoom on a log scale, with the annual peak at 1/365.25."),
("table", [
    ["Frequency (cycles/day)", "Arithmetic", "Period (days)", "Power", "What it is"],
    ["0.142466", "1 / 0.142466", "7.02", "423,766", "The weekly cycle: five working days at full capacity, then a skeleton weekend service."],
    ["0.285845", "1 / 0.285845", "3.50", "395,554", "Not separate: the second harmonic of the weekly cycle (7 / 2)."],
    ["0.428311", "1 / 0.428311", "2.33", "55,627", "Not separate: the third harmonic (7 / 3)."],
    ["0.002740", "1 / 0.002740", "365.0", "127,907", "The annual cycle, a yearly swing of about 12% peaking mid-year. 0.002740 = 3/1095, so it lands exactly in bin k = 3."],
]),
("a", "1. Two genuine periods, 7 days and 365 days. The weekly pattern is an asymmetric near-square shape rather than "
      "a sine, and Fourier represents any non-sinusoidal periodic waveform as a fundamental plus every integer "
      "multiple, so 3.50 and 2.33 days are harmonics. The test is arithmetic: 0.285845 / 0.142466 = 2.006 and "
      "0.428311 / 0.142466 = 3.006. Reporting four periods is the classic mistake here."),
("img", "C2_detrend_effect.png", "Left: mean removed only. Right: de-trended. The difference is at the extreme left edge, where the trend's energy piles up."),
("a", "2. Skipping the de-trend piles false trend energy into the two or three lowest bins, raising a wall next to the "
      "annual peak and dropping its prominence over its neighbours from about 13:1 to under 2:1, so the annual "
      "component stops looking like a peak and starts looking like a low-frequency smear."),
("table", [
    ["FFT bin", "Period (days)", "Mean removed only", "De-trended", "Inflation"],
    ["k = 1", "1095", "58,148", "10,087", "5.8x"],
    ["k = 2", "547", "18,188", "2,847", "6.4x"],
    ["k = 3", "365 (annual)", "103,385", "127,907", "0.8x, the real peak is understated"],
    ["k = 4", "274", "1,473", "36", "40.9x"],
    ["k = 5", "219", "1,421", "15", "95.9x"],
]),
("a", "Peak-to-neighbour contrast at the annual bin goes from 1.78 to 12.68 and the peak's own power rises 24%, while "
      "the weekly peak barely moves (0.2%) because it sits far from the contaminated region. De-trending matters for "
      "long-period components and hardly at all for short ones."),

("q", "C3. Decompose\n"
      "1. Run it. Describe each of the four panels in one sentence. 2. Run it again with robust=False. Where do the "
      "two trend estimates differ most, and why there? 3. This series has two seasonal periods. STL removed one of "
      "them. Where did the other one go? Point at the panel it ended up in."),
("img", "C3_stl_robust.png", "STL with period = 7, robust = True, seasonal = 15, trend = 181."),
("a", "1. Observed: the raw series, dominated by the weekly sawtooth, which fills the panel as a dense band. Trend: a "
      "smooth curve from about 97 up to 166 and back to 123, and not monotone, since it rises and falls on a one-year "
      "rhythm. Seasonal: the repeating 7-day pattern, SD 49.5, peaking Monday and troughing Sunday, its amplitude "
      "growing slowly because seasonal=15 lets the shape evolve. Resid: a flat band a few units wide, punctured by "
      "four excursions in September 2022, late August 2023, April 2024 and late July 2024."),
("img", "C3_trend_compare.png", "The two trend estimates. Red dotted lines mark the injected faults; the curves separate only around them."),
("a", "2. The maximum discrepancy is 5.05 attendances, on 16 to 23 July 2024, just before and during the 15-day "
      "inflated run; mean absolute differences near each fault are 4.85 for the ramp, 3.06 for the frozen block and "
      "0.95 for the single-day spike, and elsewhere the curves coincide."),
("a", "The trend is a LOESS smoother over a 181-day window, and with robust=False every point carries full weight, so "
      "contaminated points drag the fit towards themselves; robust=True gives each point a bisquare weight from its "
      "own residual, so anomalies are refitted almost as if absent. The ordering is about leverage: one bad point in "
      "181 is diluted despite being a 185% excursion, while 12 or 15 consecutive bad days push the same way and look "
      "like a genuine shift in level. Use robust=True whenever you plan to hunt anomalies in the remainder."),
("img", "C3_second_season.png", "Top: the trend (blue) against its own 365-day moving average (red). Bottom: the difference, a clean one-year wave of amplitude about 17."),
("a", "3. The annual season went into the trend panel, since STL was given period=7 and its seasonal panel can only "
      "hold a 7-day pattern. The trend is not monotone, alternating peaks and troughs at almost exactly twelve-month "
      "intervals, and subtracting its own 365-day moving average isolates a clean one-year sinusoid of amplitude about "
      "17, against only about 6.5 left in the remainder. It lands there because the 181-day smoothing window is about "
      "half the annual wavelength, so a LOESS smoother tracks the annual wave and reports it as trend. Use MSTL(s, "
      "periods=(7, 365)), or trend=731, or Fourier regressors for the annual term."),

("q", "C4. Hunt the anomalies\n"
      "There are four deliberate faults in this dataset. Find them. 1. List the dates you flag at a threshold of 5, "
      "and group them into distinct incidents. 2. For each incident, say which of the three kinds of anomaly it is. "
      "3. Repeat at thresholds 3, 4 and 6. Tabulate how many flags are real and how many are false alarms at each. "
      "Which threshold would you ship, and what does your choice assume about the cost of a false alarm? "
      "4. Now recompute z using rem.mean() and rem.std() instead of the median and MAD. What changes, and what is that "
      "failure called?"),
("a", "1. With median(rem) = 0.262 and MAD-sigma = 6.660, threshold 5 flags 18 days in 10 raw incidents."),
("img", "C4_anomalies.png", "Top: the raw series with the threshold-5 flags. Middle: the STL remainder. Bottom: robust z (blue) against mean/SD z (orange)."),
("table", [
    ["#", "Dates", "Days", "Values", "|z| range", "Identification"],
    ["1", "2022-06-06 (Mon)", "1", "211 vs 176 expected", "5.14", "false alarm"],
    ["2", "2022-09-10 (Sat)", "1", "97 vs 58 expected", "5.88", "FAULT 1"],
    ["3", "2023-01-17 (Tue)", "1", "118 vs 157 expected", "5.93", "false alarm"],
    ["4", "2023-04-21 to 04-24", "2", "207, 235", "5.08 - 5.35", "false alarm"],
    ["5", "2023-08-26 to 08-27", "2", "161, 161", "13.96 - 16.27", "FAULT 2 (part)"],
    ["6", "2023-09-02 to 09-03", "2", "161, 161", "14.13 - 16.25", "FAULT 2 (part)"],
    ["7", "2024-04-07 (Sun)", "1", "187 vs 64 expected", "18.48", "FAULT 3"],
    ["8", "2024-07-25 (Thu)", "1", "227 vs 181 expected", "6.84", "FAULT 4 (part)"],
    ["9", "2024-07-29 to 08-03", "6", "255, 235, 242, 225, 261, 107", "5.12 - 13.53", "FAULT 4 (part)"],
    ["10", "2024-12-30 (Mon)", "1", "189 vs 147 expected", "6.26", "false alarm"],
]),
("a", "Incidents 5 and 6 are one event, the weekend days at either end of a twelve-day block reading exactly 161, "
      "whose intervening weekdays are not flagged because 161 is a plausible weekday count. Incidents 8 and 9 are "
      "likewise one event, the ramp of 21 July to 4 August 2024, whose early days are inflated too gently to cross the "
      "threshold. So the correct reading is four real incidents and four false alarms."),
("img", "C4_four_faults.png", "The four deliberate faults, close up. Flagged days in red."),
("table", [
    ["Fault", "True extent", "Days", "max |z|", "Kind", "Why"],
    ["1", "2022-09-10", "1", "5.88",
     "Point", "A Saturday at 97 when neighbouring Saturdays run 50 to 62. Isolated, and extreme given its own "
              "expectation rather than globally."],
    ["2", "2023-08-26 to 2023-09-06", "12", "16.27",
     "Collective (frozen sensor)", "No individual value is anomalous, since 161 is an ordinary weekday count; twelve "
              "consecutive identical integers under 5.5% noise is what is impossible. Only the four weekend days cross "
              "|z| > 5, so a detector reading flagged dates alone would miss the mechanism."],
    ["3", "2024-04-07", "1", "18.48",
     "Contextual", "187 sits mid-range for a weekday (102 to 261), so no raw threshold isolates it, yet it is the most "
              "extreme point in three years once the weekly context is removed."],
    ["4", "2024-07-21 to 2024-08-04", "15", "13.53",
     "Collective (gradual drift)", "The multiplier grows from 1.00 to about 1.45 over 15 days, so 7 days never reach "
              "|z| > 5 and the event is only visible as a run. A CUSUM-style test complements a per-point z-score."],
]),
("a", "The four remaining incidents are false alarms: isolated days 30 to 40 attendances from expectation, about 5 to "
      "6 MAD-sigmas. With 1,095 observations, 5.5% noise and slightly heavy tails, a handful past 5 sigma over three "
      "years is expected."),
("table", [
    ["Threshold", "Days flagged", "Real days", "False-alarm days", "Precision", "Distinct incidents", "Faults detected"],
    ["3", "60", "17", "43", "28%", "37", "4 / 4"],
    ["4", "32", "15", "17", "47%", "20", "4 / 4"],
    ["5", "18", "13", "5", "72%", "10", "4 / 4"],
    ["6", "12", "11", "1", "92%", "6", "3 / 4"],
]),
("a", "3. Ship threshold 5: it is the largest threshold that still recovers all four faults and the smallest with a "
      "tolerable false-alarm rate. Going from 3 to 5 discards 38 of the 43 false-alarm days and costs 4 real days that "
      "belong to faults detected anyway, while going from 5 to 6 saves 4 false days but loses Fault 1, whose spike "
      "peaks at 5.88. The choice assumes a false alarm is moderately expensive and a missed incident worse: under two "
      "harmless investigations a year is an acceptable price, with a human reviewing each flag. Automatic secondary "
      "checking would push me to 3 or 4; an expensive manual audit would push me to 6 with a run-based test alongside."),
("table", [
    ["Scale estimate", "Centre", "Spread"],
    ["Robust (median, 1.4826 x MAD)", "0.262", "6.660"],
    ["Classical (mean, SD)", "1.689", "12.082"],
    ["Inflation", "6.4x", "1.81x"],
]),
("table", [
    ["Fault", "Robust max |z|", "Robust days flagged at 5", "Classical max |z|", "Classical days flagged at 5"],
    ["1 point spike", "5.88", "1 of 1", "3.12", "0 of 1, missed entirely"],
    ["2 frozen block", "16.27", "4 of 12", "8.85", "4 of 12"],
    ["3 contextual Sunday", "18.48", "1 of 1", "10.07", "1 of 1"],
    ["4 ramp", "13.53", "7 of 15", "7.34", "1 of 15"],
]),
("a", "4. The SD comes out 1.81x larger than the robust scale, so every z-score shrinks by that factor: at threshold 5 "
      "the classical score flags 6 days rather than 18 and detects 3 of 4 faults, losing the point spike outright at "
      "3.12 and collapsing the ramp from 7 flagged days to 1."),
("a", "That failure is masking. The 27 contaminated days are included when the mean and SD are computed, and because "
      "the SD squares each deviation, a few large residuals dominate the sum, so the anomalies inflate the yardstick "
      "used to measure them and large ones hide small ones. Median and MAD have a 50% breakdown point, depending on "
      "rank rather than magnitude, so 2.5% contamination leaves them untouched. The 1.4826 makes the MAD an unbiased "
      "estimate of sigma for normal data."),

("q", "C5. Make it stationary\n"
      "Build the treatment pipeline and report the evidence at every stage. 1. Produce a table with one row per stage, "
      "reporting ADF p and KPSS p: raw, after a log, after a first difference, after a seasonal difference at lag 7. "
      "At which stage does the series first pass both tests? 2. Plot the ACF of the series at the stage where it first "
      "passes. Look at lag 7. Do you still believe the tests? 3. Now try a second route: log, then go straight to the "
      "seasonal difference at lag 7, with no first difference at all. Does it pass? 4. Compare the two routes using "
      "the two over-differencing diagnostics from the lecture: the variance of the final series, and its lag-1 "
      "autocorrelation. Which route would you ship, and why? What does that tell you about the trend in this series?"),
("a", "H0(ADF) is a unit root, so we want a small p. H0(KPSS) is stationarity, so we want a large p."),
("table", [
    ["Stage (Route A)", "n", "ADF p", "KPSS p", "ADF", "KPSS", "Both?"],
    ["raw", "1095", "0.2260", "0.0100", "fail", "fail", "no"],
    ["log", "1095", "0.1522", "0.0947", "fail", "pass", "no"],
    ["log + diff(1)", "1094", "0.0000", "0.1000", "pass", "pass", "YES"],
    ["log + diff(1) + diff(7)", "1087", "0.0000", "0.1000", "pass", "pass", "yes"],
]),
("a", "1. It first passes both at log plus first difference, before any seasonal differencing. The log alone satisfies "
      "KPSS (0.010 to 0.095) by flattening the saturating growth, but ADF still cannot reject a unit root at 0.152, "
      "and the first difference then sends ADF to essentially zero."),
("img", "C5_acf.png", "Left: the ACF of log + diff(1), the stage that passed both tests. Right: the same series after a seasonal difference at lag 7."),
("table", [
    ["Lag", "1", "2", "3", "6", "7", "8", "14", "21", "28"],
    ["ACF of log + diff(1)", "-0.066", "-0.444", "+0.011", "-0.053", "+0.961", "-0.053", "+0.948", "+0.942", "+0.935"],
]),
("a", "2. No. The 95% band is 1.96/sqrt(1094) = 0.0593 and lag 7 is +0.961, sixteen times that width, with lags 14, 21 "
      "and 28 barely decaying, so the weekly cycle is completely intact and knowing the value seven days ago gives 92% "
      "of today's variance. Both tests were fooled for the same reason as series Q in A3: a bounded periodic component "
      "contributes no unit root and has a constant long-run level, so neither test has any power against it. The ACF "
      "is the only standard instrument that can see seasonality."),
("table", [
    ["Stage (Route B)", "n", "ADF p", "KPSS p", "ADF", "KPSS", "Both?"],
    ["raw", "1095", "0.2260", "0.0100", "fail", "fail", "no"],
    ["log", "1095", "0.1522", "0.0947", "fail", "pass", "no"],
    ["log + diff(7), no first difference", "1088", "0.0000", "0.1000", "pass", "pass", "YES"],
]),
("img", "C5_acf_routes.png", "Left: Route B, log + diff(7). Right: Route A, log + diff(1) + diff(7), with its large negative lag-1 spike."),
("a", "3. Yes, and unlike Route A it passes for the right reasons. The seasonal difference removes the weekly cycle "
      "exactly, Sunday against Sunday, and removes a locally linear trend as a side effect, so one operation does both "
      "jobs."),
("img", "C5_routes.png", "Route B above, Route A below. The extra difference makes the series noisier, not cleaner."),
("table", [
    ["Route", "Final series", "Variance", "Lag-1 ACF", "Verdict"],
    ["A", "log + diff(1) + diff(7)", "0.021845", "-0.417", "over-differenced"],
    ["B", "log + diff(7)", "0.013902", "+0.215", "appropriately differenced"],
    ["Ratio A / B", "", "1.57x", "", ""],
]),
("a", "4. Route A's extra difference raises the variance by 57% instead of lowering it, which means it removed "
      "something that was not there and injected noise, and its lag-1 autocorrelation of -0.417 is close to the -0.5 "
      "that differencing white noise produces. Route B's +0.215 is ordinary short-memory structure for an AR or MA "
      "term. Ship Route B: log, then a single seasonal difference at lag 7."),
("a", "The first difference was unnecessary, so the series has no unit root and no stochastic trend, and d = 0 with "
      "D = 1 at m = 7 is enough. The trend is deterministic and saturating (annual means 120.5, 140.0, 149.3, so "
      "growth is roughly halving each year), the STL trend turns over by rising 53 then falling 27, and ADF's p = "
      "0.152 on the log series was a false signal caused by the strong seasonality it has no power against. Specify "
      "SARIMA(p,0,q)(P,1,Q)7 on the logged series and handle any residual slow growth with Fourier regressors or a "
      "damped trend, not more differencing."),

# ------------------------------------------------------------------ PART D
("part", "Part D"),

("q", "D1. Review this analysis\n"
      "A colleague sends you the following two-paragraph analysis of the clinic data, with these two figures. It "
      "contains five distinct errors. Find them, and for each one say what is wrong and what should have been done "
      "instead."),
("a", "Error 1, trend: a straight line fitted to a curve that is visibly not straight. Annual means of 120.5, 140.0 "
      "and 149.3 mean growth is roughly halving each year, and the fitted line has R-squared = 0.030 because about 97% "
      "of the variance is the weekly cycle the model does not contain. Their own left figure shows the smoothed line "
      "levelling off and declining at the right edge while the red line marches on at a constant angle. Decompose "
      "first with STL(s, period=7), fit a curved form to the seasonally adjusted series, and report fit quality."),
("a", "Error 2, forecast: a significant slope treated as a licence to extrapolate three years, with no interval. The "
      "p-value of 6.7e-9 only says the slope is not exactly zero within the observed window, and with n = 1,095 a "
      "trivial slope explaining 3% of the variance becomes highly significant. Carrying 10.8 per year forward gives "
      "about 174 by January 2027 when the trend has already flattened near 150, and staffing is driven by peak load "
      "anyway, with Mondays at 184 against Sunday's 55. Fit a seasonal model, validate with rolling origins against a "
      "seasonal naive benchmark, and forecast the day-of-week profile with intervals over a horizon of weeks, not "
      "years."),
("a", "Error 3, stationarity: declared from ADF alone with the weekly seasonality untouched. The ACF of that "
      "differenced series has lag 7 at +0.948 against a 95% band of 0.059, with lags 14, 21 and 28 barely decaying. A "
      "first difference cannot remove a periodic component (B3), and ADF has no power against seasonality. Seasonally "
      "difference at lag 7, run KPSS alongside ADF, and plot the ACF before declaring anything stationary."),
("a", "Error 4, stationarity: \"I did not need to transform anything because the mean is what matters\". Stationarity "
      "needs constant variance too, and this seasonality is multiplicative, with corr(level, weekly range) = 0.635 and "
      "the mean weekly range rising from 111.6 to 150.5 across level buckets. Their second figure shows the "
      "differenced series fanning out, and feeding a heteroskedastic series to ARIMA makes the prediction intervals "
      "too wide early and too narrow late. Take logs or Box-Cox first, then difference, and verify with a rolling SD "
      "plot."),
("a", "Error 5, outliers: a global mean plus or minus 3 SD band on the raw series, with zero flags read as clean data. "
      "The band is 136.65 +/- 3 x 53.77 = [-24.6, 298.0] while the data spans 37 to 261, so no day could ever have "
      "been flagged, and the SD is measuring the weekly seasonality rather than the noise, whose robust scale is 6.66. "
      "A raw threshold cannot find three of the four faults however it is set (B6). Threshold the remainder of a "
      "robust STL fit at |z| > 5 using median and MAD, plus a run-based rule for the multi-day faults."),
("table", [
    ["#", "Area", "The error", "The correction"],
    ["1", "Trend", "Straight line fitted to a saturating curve; R-squared = 0.03 unreported",
     "Decompose first; fit a curved trend to the seasonally adjusted series and report fit quality"],
    ["2", "Forecast", "Significance mistaken for predictive validity; three-year extrapolation with no interval",
     "Seasonal model, rolling-origin validation, prediction intervals, a defensible horizon"],
    ["3", "Stationarity", "ADF alone after one difference; ACF at lag 7 is +0.95",
     "Seasonal difference at lag 7, KPSS alongside ADF, and always plot the ACF"],
    ["4", "Stationarity", "No variance stabilisation on a visibly multiplicative series",
     "Log or Box-Cox before differencing; verify with a rolling SD plot"],
    ["5", "Outliers", "Global mean +/- 3 SD band [-24.6, 298.0] is wider than the data; zero flags read as clean",
     "Robust z-score on the STL remainder at |z| > 5, plus a run-based rule; finds all four faults"],
]),
]
