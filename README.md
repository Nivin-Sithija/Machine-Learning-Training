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

## 3. Heart Disease Prediction (XGBoost Classification)

- XGBoost used to  capture non linear paterns and also when dataset has both numerical features (age, blood pressure) and categorical features (chest pain type, gender)
- Used GridSearchCV for hyperparametertuning
- How to use a Pipeline with ColumnTransformer to impute and scale  (sklearn.compose - ColumnTransformer, sklearn.pipeline - Pipeline)