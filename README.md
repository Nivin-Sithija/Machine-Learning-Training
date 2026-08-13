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

## 4. [Clustering Urban Mobility Patterns](Clustering-urban-mobility/) (K-Means, Agglomerative, DBSCAN)

- Unsupervised partitioning of 723 days of UCI bike-sharing data into 5 usage regimes, compared
  across coverage, compactness, stability and interpretability.
- Independent validation: the partition reproduces calendar variables (working day, holiday) no
  algorithm ever saw.

---

## 5. [Time Series Analysis of Clinic Attendances](Time-Series-Clinic-Attendance/) (STL, ACF, stationarity testing)

- STL decomposition (robust vs non-robust), periodogram-based seasonality detection, robust
  remainder z-score anomaly flagging, and ADF/KPSS stationarity testing across two differencing
  routes.

---

## 6. [Spambase Preprocessing Benchmark](Spambase-Preprocessing-Benchmark/) (feature selection, Optuna, instance-hardness cleaning)

- IEEE-format paper: dataset quality, not model capacity, is the dominant bottleneck on UCI 
- 13 notebooks documenting the full investigation, including the SMOTE experiment that didn't
  survive contact with cleaner data.
