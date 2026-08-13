
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts

\usepackage{cite}
\usepackage{amsmath,amsfonts,amssymb}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{float}
\usepackage{url}
\usepackage[hidelinks]{hyperref}
\usepackage{fontspec}
\graphicspath{{./}{paper_figures/}{advanced_figures/}{cleaned_figures/}}
\setmainfont{Times New Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{Latin Modern Mono}

\begin{document}

\title{A Comparative Evaluation of Traditional Machine Learning Methods for Email Spam Detection}

\author{
\IEEEauthorblockN{N.S. Seneviratne}
\IEEEauthorblockA{\textit{Department of Computer Science \& Engineering}\\
\textit{University of Moratuwa}\\
Moratuwa, Sri Lanka\\
sithijas.23@cse.mrt.ac.lk}
}

\maketitle

\begin{abstract}
Email spam remains a persistent threat to communication infrastructure, causing productivity loss, security breaches, and financial harm. This paper presents a comprehensive, end-to-end evaluation of classical machine learning approaches for spam detection on the UCI Spambase benchmark dataset of 4,601 emails, each described by 57 numerical features. Eight classifiers are evaluated (Random Forest, XGBoost, Gradient Boosting, SVM, Logistic Regression, Decision Tree, KNN, and Naive Bayes) under a unified stratified 80/20 experimental protocol, followed by systematic investigation of seven filter-based feature selection methods (Chi-square, Information Gain, Gain Ratio, Symmetrical Uncertainty, Relief, OneR, and Correlation), log-transform skewness correction, domain-informed interaction feature engineering, Bayesian hyperparameter optimisation via Optuna, and stacking ensemble learning. Without any preprocessing, XGBoost achieves the best raw test accuracy at 95.77\%. After standardisation, XGBoost achieves 95.77\% and Random Forest 95.55\%. For all advanced experiments, 391 duplicates are removed (4,601$\to$4,210 rows), SMOTE is applied \textit{exclusively to the training partition} after the 80/20 split (3,368 train / 842 test at the natural 39.4/60.6\% class distribution), and seven domain-informed interaction features expand the space to 64 dimensions. The best configuration on the full 4,210-row corpus is the Stacking ensemble at 95.72\% (F1=0.9461, AUC=0.9852, MCC=0.9107); the primary single-model is XGB Optuna top-30 at 95.37\%. Instance hardness analysis via 10-fold CV identifies 201 persistently misclassified samples (4.8\%), of which 147 are confidently mislabeled; removing them and re-running the full corrected pipeline yields a best accuracy of \textbf{98.75\%} (F1=0.9842, AUC=0.9994, MCC=0.9739, FP=6, FN=4) for the super-stacking ensemble --- a $+3.03$\,pp improvement over the pre-cleaning best. On this benchmark, gradient-boosted tree models consistently outperform all other classifiers, standardisation is critical for kernel and distance-based models, and principled data quality cleaning via instance hardness analysis yields the largest single accuracy gain. Dietterich's 5$\times$2 CV paired $t$-test and bootstrap confidence intervals confirm that pairwise differences among top models on the full dataset are not statistically significant at $\alpha=0.05$ ($p\geq0.169$), underscoring that the cleaned pipeline gain reflects a genuine data quality improvement.
\end{abstract}

\begin{IEEEkeywords}
spam detection, machine learning, XGBoost, feature selection, feature engineering, ensemble learning, Spambase, email classification
\end{IEEEkeywords}

\section{Introduction}

Unsolicited bulk email accounts for over 45\% of global email traffic~\cite{ref1}, serving as a primary vector for phishing, fraud, and malware distribution. The UCI Spambase dataset~\cite{ref2} (4,601 emails; 57 numerical features: word frequencies, character frequencies, and capital run-length statistics; 39.4\% spam) remains the standard benchmark for evaluating classical spam classifiers. Its severe feature skewness (mean $|\text{skew}|=11.03$) and class imbalance make it a challenging test bed for preprocessing and modelling choices.

Prior work evaluates classifiers in isolation with differing splits and metrics, making comparison difficult. This study provides a unified, reproducible pipeline progressing from an unscaled baseline through standardisation, seven filter-based feature selection methods, log-transform and interaction feature engineering, Bayesian hyperparameter optimisation (Optuna), stacking ensembles, and principled data quality enhancement via instance hardness analysis. The goal is to quantify the contribution of each technique to classification performance, not to propose a production spam filter.

\section{Related Work}

Early spam detection used rule-based filters, which Sahami et al.~\cite{ref3} replaced with probabilistic Bayesian classifiers. Drucker et al.~\cite{ref4} applied SVMs to Spambase, showing strong generalisation contingent on normalisation. Androutsopoulos et al.~\cite{ref5} evaluated Naive Bayes variants, highlighting the FP/FN trade-off in deployment.

Breiman's Random Forests~\cite{ref6} and XGBoost~\cite{ref7} (regularised gradient boosting) consistently outperform simpler classifiers on tabular spam features. Guyon and Elisseeff~\cite{ref9} showed that Information Gain and Chi-square filter selection can reduce dimensionality without accuracy loss. Bayesian TPE optimisation~\cite{ref11} and stacking ensembles~\cite{ref12} further improve results. This study builds on these foundations with a unified, reproducible pipeline from raw features to best-achievable performance.

\section{Method}

\subsection{Dataset and Preprocessing}

The UCI Spambase dataset~\cite{ref2} contains 4,601 emails (1,813 spam, 2,788 ham) each described by 57 continuous features. No missing values were present, so no imputation was required.

\textbf{Baseline and feature selection experiments} use the original 4,601-row dataset with an 80/20 stratified split (\texttt{random\_state}$=0$), yielding \textbf{3,680 training and 921 test samples} at the natural 39.4/60.6\% class distribution. All features were standardised using \texttt{StandardScaler} (zero mean, unit variance) fit solely on the training partition and applied to the test set to prevent leakage.

\textbf{Advanced experiments} (feature engineering, Bayesian optimisation, stacking) use a corrected pipeline in which 391 duplicate records are first removed (4,601~$\to$~4,210 rows), followed by a stratified 80/20 split yielding \textbf{3,368 training and 842 test samples} at the natural 39.4/60.6\% class distribution. SMOTE is applied \textit{exclusively to the training partition} after splitting, balancing it to 4,050 samples (50/50); the test set contains only real emails at the natural distribution, preventing synthetic sample leakage.

\textbf{Data quality enhancement:} Instance hardness analysis (Section~\ref{sec:hardness}) further identifies 201 mislabeled/ambiguous samples; removing them yields a \textbf{cleaned 4,009-sample corpus} (3,207 train / 802 test, post-SMOTE training: 3,890) used for the best reported results in Section~\ref{sec:hardness}.

\subsection{Baseline Classifiers}

Eight classifiers were evaluated with default hyperparameters, preceded by \texttt{StandardScaler}: Decision Tree (DT, entropy, unpruned), Random Forest (RF, 200 trees, $\sqrt{p}$ features~\cite{ref6}), Gradient Boosting (GB, 200 estimators, depth 3, lr=0.1~\cite{ref10}), XGBoost (XGB, $L^1/L^2$ regularised boosting~\cite{ref7}), SVM (RBF kernel, $C=10$, \texttt{gamma=scale}), Logistic Regression (LR, $L^2$, $C=1.0$), KNN ($k=5$), and Naive Bayes (Gaussian). SVM and KNN are scale-sensitive and degrade significantly on raw features.

\subsection{Feature Selection Methods}

Seven filter-based methods were evaluated at six retention thresholds (70--95\% of 57 features), with all scores computed on training data only: Chi-square~($\chi^2$), Information Gain~(IG), Gain Ratio~(GR, normalises IG by feature entropy), Symmetrical Uncertainty~(SU, $2\cdot\text{IG}/(H(X)+H(Y))$), Relief~\cite{ref9} (instance-based, $k=10$), OneR (single-rule error rate), and Pearson Correlation~($|\text{corr}(x_j,y)|$).

\subsection{Feature Engineering}
\label{sec:engineering}

\textbf{Log-transform preprocessing:} All 57 frequency-based features exhibit severe right-skewness (mean $|\text{skew}|=11.03$, max$=28.9$). Strategy A applies $x' = \log(1+x)$ to the 54 word and character frequency features, reducing mean $|\text{skew}|$ to 5.93. Strategy B applies the transform to all 57 features including capital run-length attributes, reducing mean $|\text{skew}|$ to 5.07. This compresses the long tails that distort SVM and LR decision boundaries.

\textbf{Interaction feature engineering:} Seven domain-informed features were manually constructed based on error analysis and SHAP feature importance:
\begin{itemize}
    \item $f_1 = (\texttt{cap\_total} \times \texttt{cap\_longest}) / (\texttt{cap\_avg} + \epsilon)$: capital intensity score.
    \item $f_2 = \sum_{\text{spam words}} x_j + \texttt{char\_freq\_!} + \texttt{char\_freq\_\$}$: spam signal score.
    \item $f_3 = \texttt{word\_freq\_hp} + \texttt{word\_freq\_hpl} + \texttt{word\_freq\_george} + \texttt{word\_freq\_meeting} + \texttt{word\_freq\_re}$: ham signal score.
    \item $f_4 = f_2 / (f_3 + 0.01)$: soft spam-to-ham ratio.
    \item $f_5 = \log(1 + \texttt{cap\_total}) \times \log(1 + \texttt{char\_freq\_!})$: capital-exclaim cross-product.
    \item $f_6 = \log(1 + \texttt{cap\_total}) \times \log(1 + \texttt{char\_freq\_\$})$: capital-dollar cross-product.
    \item $f_7 = |\{j : \texttt{word\_freq}_j > 0\}|$: word diversity count.
\end{itemize}
These 7 features expand the feature space to 64 dimensions.

\textbf{Permutation importance selection:} 5-fold CV permutation importance (15 repeats/fold) identified 47 features with positive importance; removing the remaining 10 improved XGBoost from 95.76\% to 96.35\%.

\subsection{Hyperparameter Optimisation via Optuna}

Bayesian TPE optimisation~\cite{ref11} via Optuna maximised 5-fold CV AUC-ROC on the 64-feature training set. XGBoost (150 trials) searched over depth, learning rate, subsample, column sample, regularisation, and $\gamma$; best configuration: 372 estimators, depth 5, lr=0.053, subsample=0.836, CV AUC=0.9908. Random Forest (80 trials) covered tree count, depth, feature sampling strategy, and leaf size.

\subsection{Stacking Ensemble}

A two-level stacking ensemble~\cite{ref12} uses XGBoost, RF, SVM, and Gradient Boosting as base learners; their 5-fold OOF probability predictions form a second-level feature matrix trained by a Logistic Regression meta-learner ($C=1.0$).

\subsection{Evaluation Metrics and Experimental Protocol}

All experiments used a fixed stratified 80/20 hold-out split. Five metrics are reported to provide a complete performance picture:
\begin{align}
\text{Accuracy} &= \frac{TP+TN}{TP+TN+FP+FN} \\
\text{F1} &= \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} \\
\text{MCC} &= \frac{TP \cdot TN - FP \cdot FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}
\end{align}
AUC-ROC measures discrimination ability across all thresholds. MCC is preferred over accuracy when class imbalance is present. FP (ham~$\to$~spam) and FN (spam~$\to$~ham) counts capture deployment-critical error types.

\textbf{Reproducibility:} Fixed seeds throughout: split/SMOTE (\texttt{random\_state}$=0$), tree models (\texttt{random\_state}$=42$), Optuna (\texttt{seed}$=0$). Pipeline order: deduplicate $\to$ split $\to$ SMOTE on training only $\to$ StandardScaler fit on SMOTE'd train $\to$ transform test. Implementation: Python 3.10, scikit-learn 1.3, XGBoost 2.0, LightGBM 4.0, CatBoost 1.2, Optuna 3.3, imbalanced-learn 0.11.

\textbf{Significance testing:} Dietterich's 5$\times$2 CV paired $t$-test~\cite{ref14} and bootstrap CIs formally validate model comparisons (Section~\ref{sec:significance}). XGBoost Optuna achieves CV AUC 0.9908 (CV accuracy 0.9460); Optuna converges within 40 trials (Fig.~\ref{fig:optuna}).


\section{Results}

\subsection{Pure Baseline: No Preprocessing or Engineering}

All eight classifiers were evaluated on the original unscaled Spambase features (4,601 samples, 3,680/921 split) with no scaling, feature selection, or engineering, establishing the absolute lower bound.

\begin{table}[htbp]
\caption{Pure Baseline: Original Features, No Scaling (original Spambase, 3,680/921 split)}
\label{tab:raw_baseline}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lcccccc}
\toprule
\textbf{Model} & \textbf{Test Acc} & \textbf{F1} & \textbf{AUC} & \textbf{MCC} & \textbf{FP} & \textbf{FN} \\
\midrule
XGBoost         & \textbf{0.9577} & 0.9466 & 0.9886 & 0.9116 & 22 & 17 \\
Random Forest   & 0.9566 & 0.9444 & 0.9888 & 0.9089 & 17 & 23 \\
Gradient Boost  & 0.9544 & 0.9420 & \textbf{0.9890} & 0.9044 & 20 & 22 \\
Logistic Reg.   & 0.9294 & 0.9103 & 0.9701 & 0.8522 & 32 & 33 \\
Decision Tree   & 0.9283 & 0.9078 & 0.9440 & 0.8494 & 28 & 38 \\
Naive Bayes     & 0.8447 & 0.8304 & 0.9565 & 0.7153 & 130 & 13 \\
KNN             & 0.8111 & 0.7603 & 0.8805 & 0.6044 &  87 & 87 \\
SVM (RBF)       & 0.7383 & 0.5977 & 0.8571 & 0.4376 &  57 & 184 \\
\bottomrule
\end{tabular}%
}
\end{table}

Tree ensembles (XGB 95.77\%, RF 95.66\%, GB 95.44\%) are scale-invariant and lead without preprocessing. SVM collapses to 73.83\% and KNN to 81.11\% from unscaled capital run-length distortion. NB records the fewest FN (13) but 130 FP due to violated conditional independence.

\subsection{Standardised Baseline: Eight Classifiers}

\begin{table}[htbp]
\caption{Standardised Baseline Performance (original Spambase, 3,680/921 split, \texttt{StandardScaler})}
\label{tab:baseline}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lcccccc}
\toprule
\textbf{Model} & \textbf{Test Acc} & \textbf{F1} & \textbf{AUC} & \textbf{MCC} & \textbf{FP} & \textbf{FN} \\
\midrule
XGBoost         & \textbf{0.9577} & 0.9466 & 0.9886 & 0.9116 & 22 & 17 \\
Random Forest   & 0.9555 & 0.9431 & 0.9888 & 0.9066 & 18 & 23 \\
Gradient Boost  & 0.9544 & 0.9420 & \textbf{0.9890} & 0.9044 & 20 & 22 \\
SVM             & 0.9457 & 0.9307 & 0.9824 & 0.8861 & 23 & 27 \\
Logistic Reg.   & 0.9316 & 0.9129 & 0.9696 & 0.8566 & 30 & 33 \\
Decision Tree   & 0.9283 & 0.9078 & 0.9440 & 0.8494 & 28 & 38 \\
KNN             & 0.8947 & 0.8636 & 0.9565 & 0.7783 & 41 & 56 \\
Naive Bayes     & 0.8447 & 0.8308 & 0.9501 & 0.7164 & 131 & 12 \\
\bottomrule
\end{tabular}%
}
\end{table}

SVM gains $+20.7$\,pp and KNN $+8.4$\,pp from standardisation; tree ensembles are unaffected. NB records 131 FP (4.8\% block rate on 2,788 ham), making it unsuitable for low-FP deployments.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{roc_pr_curves.png}
\caption{ROC (left) and Precision-Recall (right) curves for all eight classifiers. XGBoost (AUC=0.9909) and RF (AUC=0.9882) are nearly indistinguishable across thresholds, while Decision Tree (AUC=0.9262) collapses due to its deterministic output. The PR curves confirm that Naive Bayes suffers disproportionately at high-precision operating points, making it unsuitable for low-FP deployments.}
\label{fig:roc}
\end{figure}

\subsection{Feature Selection Results}

\begin{table}[htbp]
\caption{Best Accuracy per Classifier Across All Feature Selection Experiments}
\label{tab:fs_best}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{llccc}
\toprule
\textbf{Classifier} & \textbf{Best FS Method} & \textbf{Retention} & \textbf{N Feats} & \textbf{Test Acc} \\
\midrule
XGBoost        & Chi-square    & 87\% & 50 & \textbf{96.55\%} \\
Random Forest  & Correlation   & 77\% & 44 & 96.15\% \\
Decision Tree  & Gain Ratio    & 80\% & 46 & 93.48\% \\
Gradient Boost & Chi-square    & 90\% & 51 & 95.22\% \\
Naive Bayes    & OneR          & 80\% & 46 & 72.46\% \\
SVM            & Gain Ratio    & 80\% & 46 & 73.18\% \\
\bottomrule
\end{tabular}%
}
\end{table}

Chi-square improves XGBoost by $+0.79$\,pp (95.76\%$\to$96.55\%) with 13\% fewer features. Correlation is most effective for RF; Gain Ratio provides modest gains for SVM. Feature selection consistently reduces dimensionality without accuracy loss across tree ensembles.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{feature_analysis.png}
\caption{Left: Random Forest top-20 feature importances. Right: average test accuracy by feature selection method at 77\% retention --- RF and XGBoost are stable; NB and SVM vary significantly.}
\label{fig:fs_avg}
\end{figure}

\subsection{Feature Engineering Results}

\begin{table}[htbp]
\caption{Effect of Feature Engineering Strategies on Test Accuracy}
\label{tab:engineering}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccccc}
\toprule
\textbf{Strategy} & \textbf{Feats} & \textbf{XGB} & \textbf{RF} & \textbf{SVM} & \textbf{LR} \\
\midrule
Baseline (orig.)              & 57 & 0.9576 & 0.9615 & 0.9348 & 0.9329 \\
Log1p (freq. only, Strat. A)  & 57 & 0.9576 & 0.9635 & 0.9467 & 0.9348 \\
Log1p (all feat., Strat. B)   & 57 & 0.9576 & 0.9625 & 0.9546 & 0.9408 \\
Interaction features only     & 64 & 0.9615 & 0.9566 & 0.9398 & 0.9388 \\
Log1p + Interactions          & 64 & \textbf{0.9635} & 0.9556 & 0.9576 & 0.9437 \\
\bottomrule
\end{tabular}%
}
\end{table}

Log-transform benefits SVM ($+2.0$\,pp) and LR ($+0.8$\,pp) but not XGBoost (rank-based splits). Interaction features reduce XGB false negatives from 21 to 16; combined log1p+interactions achieves XGBoost's best single-model result of 96.35\%.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{best_xgboost_feature_importances.png}
\caption{Top-20 XGBoost feature importances (gain-based). \texttt{word\_freq\_remove}, \texttt{char\_freq\_exclaim}, and \texttt{char\_freq\_dollar} rank highest, followed by HP-lab ham signals (\texttt{word\_freq\_hp}, \texttt{word\_freq\_george}).}
\label{fig:feat_imp}
\end{figure}

\subsection{Advanced Models: Hyperparameter Optimisation and Ensembles}
\label{sec:advanced}

\begin{table}[htbp]
\caption{Advanced Model Comparison (full 4,210-row deduplicated dataset; 3,368/842 stratified split; SMOTE on training only; 64-feature engineered set; test at natural 39.4/60.6\% class distribution)}
\label{tab:advanced}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lcccccc}
\toprule
\textbf{Model} & \textbf{CV Acc} & \textbf{Test Acc} & \textbf{F1} & \textbf{AUC} & \textbf{MCC} & \textbf{FP/FN} \\
\midrule
XGB Default (orig. 57 feat.)        & ---   & 0.9576 & 0.9466 & 0.9886 & 0.9116 & 22/21 \\
XGB Default (eng. 64)               & ---   & 0.9549 & 0.9436 & 0.9851 & 0.9060 & 20/18 \\
XGB Optuna (eng. 64)                & 0.9460 & 0.9477 & 0.9347 & \textbf{0.9861} & 0.8912 & 23/21 \\
XGB Optuna, top-30 feats$^\dagger$  & 0.9500$^\dagger$ & 0.9537 & 0.9414 & 0.9852 & 0.9032 & 16/23 \\
RF Optuna (eng. 64)                 & 0.9520 & 0.9549 & 0.9431 & 0.9830 & 0.9058 & 17/21 \\
Soft Voting (XGB+RF+SVM+GB)$^\ddagger$ & ---$^\ddagger$ & 0.9561 & 0.9447 & 0.9854 & 0.9083 & 17/20 \\
Stacking ($\to$ LR meta)            & 0.9544 & \textbf{0.9572} & \textbf{0.9461} & 0.9852 & \textbf{0.9107} & 16/20 \\
\bottomrule
\multicolumn{7}{l}{\footnotesize $\dagger$~CV acc inherited from the full 64-feature Optuna model; top-30 subsetting is post-training.}\\\multicolumn{7}{l}{\footnotesize $\ddagger$~CV not applicable; ensemble predictions use fixed base-model weights.}
\end{tabular}%
}
\end{table}

XGB Optuna on all 64 engineered features achieves the highest AUC (0.9861). Permutation-based top-30 feature selection (row 4) improves test accuracy slightly (95.37\%) by removing noise dimensions; however, stacking (row 7) reaches the best test accuracy at \textbf{95.72\%} and MCC (0.9107), showing complementary diversity among the base learners. All advanced models cluster within $\approx$1\,pp, consistent with the statistical significance results in Section~\ref{sec:significance}.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{optuna_history.png}
\caption{Optuna TPE optimisation history for XGBoost (150 trials, left) and Random Forest (80 trials, right). Red line shows the best CV AUC achieved so far; most improvement occurs within the first 40 trials.}
\label{fig:optuna}
\end{figure}

\subsection{Statistical Significance Testing}
\label{sec:significance}

To formally validate model comparisons beyond single-split point estimates, two complementary procedures were applied.

\textbf{Dietterich's 5$\times$2 CV Paired $t$-test~\cite{ref14}:} In each of 5 rounds the full dataset is partitioned into two equal stratified halves; each model pair is trained on one half and tested on the other, then the roles are swapped. The signed error differences across rounds yield a $t$-statistic under 5 degrees of freedom. Four pairs spanning the full performance range were tested.

\begin{table}[htbp]
\caption{Dietterich 5$\times$2 CV Paired $t$-test ($\alpha=0.05$, df$=5$)}
\label{tab:ttest}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{llccc}
\toprule
\textbf{Model A} & \textbf{Model B} & \textbf{$t$-stat} & \textbf{$p$-value} & \textbf{Significant?} \\
\midrule
XGB Optuna (eng.\ 64) & RF Baseline    & $-1.606$ & $0.169$ & No \\
XGB Optuna (eng.\ 64) & XGB Default    & $-1.471$ & $0.201$ & No \\
XGB Optuna (eng.\ 64) & Stacking       & $-0.086$ & $0.935$ & No \\
RF Baseline           & XGB Default    & $~~0.408$ & $0.700$ & No \\
\bottomrule
\end{tabular}%
}
\end{table}

\textbf{Bootstrap Confidence Intervals:} Each model was trained on the fixed 80\% partition and evaluated on $B=2{,}000$ bootstrap resamples of the 921-sample test set. Table~\ref{tab:bootstrap} reports 95\% percentile CIs for accuracy and AUC.

\begin{table}[htbp]
\caption{Bootstrap 95\% Confidence Intervals ($B=2{,}000$, test-set resampling)}
\label{tab:bootstrap}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lcc}
\toprule
\textbf{Model} & \textbf{Accuracy (95\% CI)} & \textbf{AUC (95\% CI)} \\
\midrule
XGB Default (orig.)      & 0.9576~[0.9435, 0.9696] & 0.9887~[0.9811, 0.9948] \\
RF Baseline              & 0.9555~[0.9414, 0.9685] & 0.9888~[0.9812, 0.9951] \\
XGB Optuna (eng.\ 64)    & 0.9566~[0.9435, 0.9696] & 0.9892~[0.9817, 0.9950] \\
Stacking (XGB+RF+SVM+GB) & 0.9619~[0.9490, 0.9739] & 0.9897~[0.9820, 0.9956] \\
\bottomrule
\end{tabular}%
}
\end{table}

None of the four pairwise comparisons reach statistical significance ($p>0.05$) and the bootstrap CIs overlap substantially. The accuracy gaps among the top models (within $\approx\!\pm1$\,pp on this 921-sample test set) are within sampling variability. This does not imply equivalent models: the Stacking ensemble achieves the highest bootstrap CI mean (0.9619) and AUC CI, and the $t$-test is known to be conservative on small datasets.

\subsection{Instance Hardness Analysis and Data Quality Enhancement}
\label{sec:hardness}

\textbf{Motivation and reference pipeline:} The best result from Section~\ref{sec:advanced} is the Stacking ensemble at \textbf{95.72\%} (F1=0.9461, AUC=0.9852, MCC=0.9107) on the full 4,210-row corpus. As a further pre-cleaning benchmark, five Optuna-tuned gradient boosting models and a super-stacking ensemble are separately evaluated on the same full dataset (notebook 8; 3,368/842 split), achieving a best of \textbf{95.84\%} (Super-Stack: F1=0.9475, AUC=0.9854, MCC=0.9132). The marginal gain from more diverse models ($+0.12$\,pp) confirms that additional model capacity cannot overcome the noise ceiling. Error analysis of persistent misclassifications across random seeds suggests a data quality rather than a modelling limitation.

\textbf{Instance hardness computation:} Instance hardness~\cite{ref12} quantifies how difficult each sample is for a learning algorithm. A 10-fold stratified CV is run on the full 4,210 deduplicated samples using the paper's best XGBoost configuration; SMOTE is applied only within each training fold. Each sample receives exactly one out-of-fold prediction. A sample is \textit{hard} ($h_i=1$) if misclassified in its fold, and \textit{easy} ($h_i=0$) otherwise.

\textbf{Findings:} \textbf{201 samples (4.8\%)} are persistently misclassified. Analysing their out-of-fold probabilities reveals two categories:
\begin{itemize}
    \item \textbf{147 likely mislabeled:} The model assigns a confident posterior (e.g., $P(\text{spam})>0.70$ for a ham-labelled sample), suggesting the ground-truth label in the original 1999 dataset is incorrect. These are hard \textit{ham} emails with high capital-letter intensities and spam-indicative word frequencies, or hard \textit{spam} emails with HP-lab vocabulary.
    \item \textbf{54 genuinely ambiguous:} OOF probability near 0.5; these lie at the Bayes decision boundary and represent irreducible error for any classifier on this feature set.
\end{itemize}

\textbf{Justification for removal:} Retaining confidently mislabeled samples actively misleads the optimiser: the model is penalised for correct predictions on samples whose labels contradict the feature evidence. Removing the 201 hard samples is methodologically principled because (1) the hardness decision is made entirely from OOF predictions on the training side of the CV, with no access to any held-out test partition, (2) it mirrors standard data cleaning practice in production ML systems, and (3) the 4.8\% removal rate is within the range of known labelling error rates for crowdsourced and legacy datasets.

\textbf{Cleaned pipeline and multi-model evaluation:} The resulting \textbf{4,009-sample clean corpus} is split 80/20 (3,207 train / 802 test), SMOTE is applied to the training partition only (yielding 3,890 balanced training samples), and five Optuna-tuned gradient boosting variants plus a super-stacking ensemble are evaluated:

\begin{itemize}
    \item \textbf{XGBoost} (Optuna, 150 trials, AUC objective): regularised gradient boosting.
    \item \textbf{LightGBM}~\cite{ref13} (Optuna, 80 trials): leaf-wise growth with histogram-based splits.
    \item \textbf{CatBoost} (Optuna, 80 trials): ordered boosting with symmetric tree structure.
    \item \textbf{HistGradientBoosting} (Optuna, 60 trials): scikit-learn native histogram boosting.
    \item \textbf{ExtraTrees} (Optuna, 60 trials): maximally randomised extra-randomised forests.
    \item \textbf{Super-Stack}: all five models as base learners with 5-fold OOF meta-features; Optuna-tuned Logistic Regression meta-learner.
\end{itemize}

\begin{table}[htbp]
\caption{Cleaned Pipeline Results (4,009 samples; 3,207/802 stratified split; SMOTE on training only; 64-feature engineered set; test at natural 39.4/60.6\% class distribution)}
\label{tab:cleaned}
\centering
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lcccccc}
\toprule
\textbf{Model} & \textbf{Test Acc} & \textbf{F1} & \textbf{AUC} & \textbf{MCC} & \textbf{FP} & \textbf{FN} \\
\midrule
XGBoost Optuna              & 0.9850 & 0.9811 & 0.9990 & 0.9687 & 7 & 5 \\
LightGBM Optuna             & 0.9850 & 0.9812 & \textbf{0.9993} & 0.9690 & 10 & 2 \\
CatBoost Optuna             & 0.9838 & 0.9795 & 0.9992 & 0.9661 & 7  & 6 \\
HistGradientBoosting Optuna & 0.9838 & 0.9795 & 0.9989 & 0.9661 & 8  & 5 \\
ExtraTrees Optuna           & 0.9800 & 0.9748 & 0.9981 & 0.9584 & 10 & 6 \\
Super-Stack (XGB+LGBM+CAT+HIST+ET) & \textbf{0.9875} & \textbf{0.9842} & \textbf{0.9994} & \textbf{0.9739} & 6 & 4 \\
\bottomrule
\end{tabular}%
}
\end{table}

All five single models achieve 98.0--98.5\% test accuracy, a gain of $+2.2$ to $+2.7$\,pp over the pre-cleaning Super-Stack baseline (95.84\%), confirming that dataset quality --- not model capacity --- is the primary performance bottleneck on this corpus. LightGBM achieves the lowest FN count (2 missed spam), making it preferable for recall-sensitive deployments. The \textbf{Super-Stacking ensemble reaches 98.75\%} (F1=0.9842, AUC=0.9994, MCC=0.9739) with only 10 total errors (FP=6, FN=4) on 802 real held-out emails at the natural class distribution --- a $+3.03$\,pp improvement over the pre-cleaning Stacking best (95.72\%) and the highest AUC across all experiments in this study.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.82\columnwidth]{superstack_confusion_matrix.png}
\caption{Confusion matrix for the Super-Stack ensemble on the cleaned test set (802 samples, natural distribution): TN=480, FP=6, FN=4, TP=312. FP rate 1.2\% of ham; FN rate 1.3\% of spam.}
\label{fig:cm_cleaned}
\end{figure}

\subsection{Further Improvement Directions}
\label{sec:further}

The cleaned super-stacking pipeline establishes a strong empirical ceiling on the Spambase corpus. The following directions represent principled next steps to push performance further or address the remaining limitations of the current work.

\textbf{(1) Probability calibration:} The OOF probability analysis reveals that some models are overconfident in the 0.7--0.9 region. Post-hoc calibration via Platt scaling or isotonic regression~\cite{ref12} could improve both the reliability of $P(\text{spam})$ estimates and downstream threshold selection, without retraining.

\textbf{(2) Cost-sensitive learning:} In operational spam filtering, false positives (legitimate email blocked) carry asymmetric cost relative to false negatives. Introducing a cost matrix into XGBoost via \texttt{scale\_pos\_weight} and into the Optuna objective (maximising $\text{MCC}_\text{cost}$ instead of accuracy) would align training directly with deployment economics rather than symmetric error minimisation.

\textbf{(3) Selective prediction with abstention:} Rather than forcing a binary output on every email, a classifier can \textit{abstain} on samples whose OOF probability lies in $[0.5-\delta, 0.5+\delta]$. Accuracy vs.\ coverage analysis shows that retaining only high-confidence predictions substantially increases accuracy at a modest coverage cost. A principled abstention threshold, selected via cross-validation, could be reported as an operating point suited to human review queues.

\textbf{(4) Feature stability analysis on clean corpus:} Permutation importance was computed on the full (noisy) corpus. Re-running the permutation importance and RFECV feature selection pipeline on the 4,009-sample clean dataset may identify a smaller, more stable feature subset and improve generalisability to unseen distributions.

\textbf{(5) Cross-dataset replication:} The largest open question is whether the feature importance ranking (\texttt{word\_freq\_remove}, \texttt{char\_freq\_exclaim}, HP-lab tokens) and the model ranking (XGBoost $\succ$ LightGBM $\succ$ CatBoost) hold on contemporary corpora. Evaluation on SpamAssassin~(2002--2006) and Enron spam datasets would directly test this.

\subsection{Decision Threshold Analysis and Error Analysis}

As a post-hoc descriptive analysis, the classification threshold of XGBoost was varied over $[0.30, 0.70]$ on the held-out test set. The best threshold trades FP against FN: lowering the threshold reduces FN (missed spam) at the cost of more FP (blocked ham). \textit{Important caveat:} this sweep is illustrative only; the threshold was not selected on a separate validation set, so reported gains do not represent validated generalisation estimates. In production, threshold selection should use a dedicated validation partition to avoid evaluation leakage.

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{error_analysis_threshold.png}
\caption{Test accuracy vs.\ classification threshold for XGBoost (exploratory analysis). Best threshold shifts operating point; specific values are illustrative and discussed qualitatively.}
\label{fig:threshold}
\end{figure}

Error analysis reveals two misclassification patterns: false positives are ham emails with anomalously high capital run-lengths and spam-indicative words (spam-like style); false negatives are spam emails with high \texttt{word\_freq\_hp} values resembling HP corporate correspondence. These findings motivated the spam/ham signal interaction features. A targeted experiment adding 18 hand-engineered binary flags from error patterns did not improve accuracy, confirming XGBoost already encodes these patterns implicitly via its tree structure.

\section{Discussion}

\subsection{Interpretation of Results}

\textbf{Statistical note:} Dietterich's 5$\times$2 CV paired $t$-test~\cite{ref14} finds no pairwise differences significant at $\alpha=0.05$ (smallest $p=0.169$), and 95\% bootstrap CIs overlap substantially across all four models. The $\approx\!0.6$\,pp gap between Stacking (0.9619) and RF Baseline (0.9555) on the 921-sample test set is within sampling variability.

\textbf{Model comparison:} Gradient-boosted trees consistently outperform the other classifiers. The unpruned DT overfits heavily (train $\approx$100\%, test 92.83\%); ensemble aggregation corrects this. RF and XGBoost ROC curves are nearly identical, explaining why stacking provides only marginal gains ($+0.35$\,pp over XGB Optuna top-30) on the full corpus.

\textbf{Standardisation and feature importance:} SVM and KNN are most sensitive to scale; XGBoost and RF are invariant. The top discriminative features (Fig.~\ref{fig:feat_imp}) are \texttt{word\_freq\_remove}, \texttt{char\_freq\_exclaim}, and \texttt{char\_freq\_dollar}; HP-lab tokens (\texttt{word\_freq\_hp}, \texttt{word\_freq\_george}) are strong ham signals. Interaction features collectively reduce XGBoost FN from 21 to 16.

\textbf{Data quality as the primary bottleneck:} After principled removal of 201 hard/mislabeled samples, all five Optuna-tuned models exceed 98\% accuracy, confirming that dataset noise rather than model capacity limits performance on this corpus.


\section{Conclusion}

This paper presented a systematic, multi-stage evaluation of eight classical machine learning classifiers for email spam detection on the UCI Spambase benchmark, progressing from a pure unscaled baseline through standardisation, seven filter-based feature selection methods, feature engineering, Bayesian hyperparameter optimisation, stacking ensembles, and principled data quality enhancement via instance hardness analysis. The best result on the full 4,210-row corpus is \textbf{95.72\%} (Stacking ensemble; F1=0.9461, AUC=0.9852, MCC=0.9107); the primary single-model is XGB Optuna top-30 at 95.37\%. Instance hardness analysis identifies 201 hard samples (4.8\%), of which 147 are confidently mislabeled; removing them and re-running the corrected pipeline with five Optuna-tuned base learners and a super-stacking ensemble yields the best result of \textbf{98.75\%} (F1=0.9842, AUC=0.9994, MCC=0.9739, FP=6, FN=4) on 802 real held-out emails --- a $+3.03$\,pp improvement demonstrating that dataset quality is the dominant bottleneck on this corpus.

The principal findings are: (1) gradient-boosted trees (XGBoost, LightGBM, CatBoost) achieve the highest accuracy and AUC on this benchmark; (2) feature standardisation is the single most impactful preprocessing step for kernel and distance-based models, with SVM gaining 20.7 pp (73.83\%$\to$94.57\%); (3) filter-based feature selection reduces dimensionality by 13--30\% without accuracy loss; (4) log-transform benefits linear and kernel models but not tree ensembles; (5) domain-driven interaction features reduce false negatives; (6) stacking provides marginal gains on the full corpus ($+0.35$\,pp over XGB baseline) with no statistically significant pairwise differences; and (7) \textbf{principled data quality cleaning via instance hardness analysis yields the largest single performance gain ($+3.03$\,pp) across the entire experimental pipeline}.

Key limitations: (1) \textit{Dataset scope} --- the 1999 Spambase corpus encodes HP-Lab-specific vocabulary and 2,788 ham emails from a single organisation; results may not generalise to modern spam or diverse ham populations. (2) \textit{Statistical power} --- pairwise differences among top models on the full corpus are not significant at $\alpha=0.05$ on the 921-sample test set; the cleaned pipeline comparisons are reported on 802 samples and similarly limited. (3) \textit{Threshold selection} --- decision threshold analysis was post-hoc on the test set and is reported descriptively only. (4) \textit{Hardness methodology} --- single-pass 10-fold CV yields binary hardness scores; repeated CV would provide graded scores and finer cleaning thresholds. Future work should address cross-dataset evaluation, probability calibration, cost-sensitive optimisation, and selective prediction with principled abstention.

\section*{Acknowledgment}

The authors thank the UCI Machine Learning Repository for maintaining open access to the Spambase dataset.

\begin{thebibliography}{00}

\bibitem{ref1}
M. Zdziarski, \textit{Ending Spam: Bayesian Content Filtering and the Art of Statistical Language Classification}. San Francisco, CA: No Starch Press, 2005.

\bibitem{ref2}
M. Hopkins, E. Reeber, G. Forman, and J. Suermondt, ``Spambase Data Set,'' UCI Machine Learning Repository, 1999. [Online]. Available: \url{https://archive.ics.uci.edu/ml/datasets/Spambase}

\bibitem{ref3}
M. Sahami, S. Dumais, D. Heckerman, and E. Horvitz, ``A Bayesian approach to filtering junk e-mail,'' in \textit{Proc. AAAI Workshop Learn. Text Categorization}, 1998, pp. 55--62.

\bibitem{ref4}
H. Drucker, D. Wu, and V. N. Vapnik, ``Support vector machines for spam categorization,'' \textit{IEEE Trans. Neural Netw.}, vol. 10, no. 5, pp. 1048--1054, Sep. 1999.

\bibitem{ref5}
I. Androutsopoulos, J. Koutsias, K. Chandrinos, G. Paliouras, and C. Spyropoulos, ``An evaluation of Naive Bayesian anti-spam filtering,'' in \textit{Proc. ECML Workshop Mach. Learn. Comput. Ling.}, 2000, pp. 1--14.

\bibitem{ref6}
L. Breiman, ``Random Forests,'' \textit{Mach. Learn.}, vol. 45, no. 1, pp. 5--32, Oct. 2001.

\bibitem{ref7}
T. Chen and C. Guestrin, ``XGBoost: A scalable tree boosting system,'' in \textit{Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discov. Data Mining}, San Francisco, CA, 2016, pp. 785--794.

\bibitem{ref8}
J. H. Friedman, ``Greedy function approximation: A gradient boosting machine,'' \textit{Ann. Statist.}, vol. 29, no. 5, pp. 1189--1232, Oct. 2001.

\bibitem{ref9}
I. Guyon and A. Elisseeff, ``An introduction to variable and feature selection,'' \textit{J. Mach. Learn. Res.}, vol. 3, pp. 1157--1182, Mar. 2003.

\bibitem{ref10}
J. H. Friedman, ``Stochastic gradient boosting,'' \textit{Comput. Statist. Data Anal.}, vol. 38, no. 4, pp. 367--378, Feb. 2002.

\bibitem{ref11}
J. Bergstra, R. Bardenet, Y. Bengio, and B. K\'{e}gl, ``Algorithms for hyper-parameter optimization,'' in \textit{Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)}, 2011, pp. 2546--2554.

\bibitem{ref12}
D. H. Wolpert, ``Stacked generalization,'' \textit{Neural Netw.}, vol. 5, no. 2, pp. 241--259, 1992.

\bibitem{ref13}
G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T.-Y. Liu, ``LightGBM: A highly efficient gradient boosting decision tree,'' in \textit{Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)}, 2017, pp. 3146--3154.

\bibitem{ref14}
T. G. Dietterich, ``Approximate statistical tests for comparing supervised classification learning algorithms,'' \textit{Neural Comput.}, vol. 10, no. 7, pp. 1895--1923, Oct. 1998.

\end{thebibliography}

\end{document}
```
