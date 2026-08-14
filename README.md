# Machine Learning Training Projects

## 1. Rock vs Metal Detection (Logistic Regression)

- The sonar data has a relatively linear relationship between features and classes
- Logistic Regression shows  probability estimates for predictions and easy to understand which features affect most (sklearn.linear_model - LogisticRegression)
---

## 2. Diabetes Prediction (Support Vector Machine)

- SVM is  used when clear separation is important, to find  optimal decision boundary by maximizing the margin between classes (sklearn - svm)

The diabetes dataset has features with very different scales 
Solution is Standardization (sklearn.preprocessing - StandardScaler)

---

## 3. Heart Disease Prediction (XGBoost & CatBoost)

- XGBoost used to  capture non linear paterns and also when dataset has both numerical features (age, blood pressure) and categorical features (chest pain type, gender)
- Used GridSearchCV for hyperparametertuning
- How to use a Pipeline with ColumnTransformer to impute and scale  (sklearn.compose - ColumnTransformer, sklearn.pipeline - Pipeline)

Tried RandomForestClassifier and also ensembled with XGB but didnt achieve higher score  <br>
Finally used Catboost Classifier- it handles categorical data without remembering to avoid overfit of XGB which achieved more accuracy

---

## 4. Spam Email Detection (Feature Selection, Optuna, Instance Hardness)

- Started as coursework on the UCI Spambase data (4601 emails, 57 features) and grew into an IEEE format paper - the point is that dataset quality, not model capacity, is what limits accuracy here
- Compared seven filter based feature selection methods, then log transform for skewness correction and domain driven interaction features
- Bayesian hyperparameter tuning across 5 gradient boosting variants instead of GridSearchCV, it searches smarter when the space is large (optuna)
- Instance hardness computed manually with cross validated out of fold predictions to find the rows models keep getting wrong (sklearn.model_selection - StratifiedKFold) - separated "atypical" (label probably wrong) from "borderline" (just near the boundary) and only removed the atypical ones

Baseline XGBoost was 95.77%, feature selection took it to 96.55% <br>
Stacking five tuned models on the cleaned data reached 97.79% without changing any architecture <br>
Tried SMOTE early on and it helped, but once the data was cleaned it stopped helping - kept both notebooks to show it

---

## 5. Time Series Analysis of Clinic Attendances (STL, ACF, Stationarity Testing)

- 3 years of daily clinic attendances, used to learn decomposition and stationarity properly rather than to predict anything
- STL decomposition run robust and non robust to see where the trend estimates disagree, and to find the annual component hiding under the weekly one (statsmodels.tsa.seasonal - STL)
- Periodogram to detect the seasonal periods from the data itself instead of assuming weekly
- Anomaly flagging with a robust z score on the remainder - a plain mean/std threshold gets distorted by the same outliers it is supposed to catch
- ADF and KPSS together for stationarity, they test opposite null hypotheses so agreeing on both is stronger evidence (statsmodels.tsa.stattools - adfuller, kpss)

Checked two differencing routes (log then diff(1) then diff(7), vs log then diff(7) only) and looked at ACF diagnostics for over differencing

---

## 6. Clustering Urban Mobility Patterns (K-Means, Agglomerative, DBSCAN)

- Unsupervised problem, no labels to check against, so the whole difficulty is deciding which partition is actually the good one
- 723 days of UCI bike sharing data described with 11 engineered features, partitioned with all three algorithms and compared on coverage, compactness, stability and interpretability (sklearn.cluster - KMeans, AgglomerativeClustering, DBSCAN)
- Picked K-Means with k=5, giving 5 usage regimes - peak commuter, cold season commuter, warm leisure, cold low demand leisure, and adverse weather suppressed demand

DBSCAN scored better on silhouette (0.336 vs 0.221) and stability, but only by throwing away 22.5% of days as noise and answering an easier 2 cluster question - higher score, worse answer <br>
Validated by checking the clusters against working day and holiday flags, which were never given to any algorithm, and they line up (χ² = 652 and χ² = 30) <br>
Season and weather line up too but that proves nothing, those were clustering inputs
