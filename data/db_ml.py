# db_ml.py - COMPREHENSIVE Machine Learning, Statistics, Metrics, DA/BI, Data Viz
# Covers: ML Fundamentals, Algorithms, Metrics, Statistics, Data Analysis, Visualization

ML_QUESTIONS = []

def add(sub, q, a, is_coding=False, code_python=""):
    ML_QUESTIONS.append({
        "category": "ml_stats",
        "subcategory": sub,
        "question": q,
        "answer": a.strip(),
        "is_coding": is_coding,
        "code_sql": "",
        "code_java": "",
        "code_python": code_python.strip()
    })

# ═══════════════════════════════════════════════════════════════
# ML FUNDAMENTALS (50 questions)
# ═══════════════════════════════════════════════════════════════

add("ML Fundamentals", "What is the difference between supervised, unsupervised, and reinforcement learning?", """
* **Supervised Learning**: Model learns from labeled data (input-output pairs). Types: Classification (discrete labels) and Regression (continuous values). Examples: spam detection, house price prediction.
* **Unsupervised Learning**: Model finds hidden patterns in unlabeled data. Types: Clustering (K-Means, DBSCAN), Dimensionality Reduction (PCA, t-SNE), Association Rules. Examples: customer segmentation.
* **Reinforcement Learning**: Agent learns by interacting with an environment, receiving rewards/penalties. Examples: game playing (AlphaGo), robotics, autonomous driving.
""")

add("ML Fundamentals", "What is the Bias-Variance Trade-off?", """
* **Bias**: Error from overly simplistic model assumptions (underfitting). High bias = model can't capture data patterns.
* **Variance**: Error from sensitivity to training data fluctuations (overfitting). High variance = model memorizes noise.
* **Total Error** = Bias² + Variance + Irreducible Error.
* **Trade-off**: As model complexity increases, bias decreases but variance increases. The optimal model minimizes total error.
* **Solutions**: Regularization (L1/L2), cross-validation, ensemble methods, more training data.
""")

add("ML Fundamentals", "Explain L1 (Lasso) vs L2 (Ridge) regularization.", """
* **L1 (Lasso)**: Adds |w| penalty. Drives unimportant weights to exactly zero → performs feature selection, creates sparse models.
* **L2 (Ridge)**: Adds w² penalty. Shrinks all weights toward zero but never exactly zero → keeps all features, prevents any single feature from dominating.
* **Elastic Net**: Combines L1 + L2 penalties. Best of both worlds.
* **When to use**:
  - L1: When you suspect many irrelevant features (sparse solution desired).
  - L2: When all features contribute but you want to prevent overfitting.
""")

add("ML Fundamentals", "How do Decision Trees work? What are Gini Impurity and Information Gain?", """
Decision Trees recursively split data based on feature values to maximize class separation.
* **Gini Impurity**: Measures probability of misclassifying a randomly chosen element. Gini(p) = 1 - Σ(pᵢ²). Gini = 0 means pure node. Used by CART algorithm.
* **Entropy**: H(p) = -Σ(pᵢ log₂ pᵢ). Measures disorder/uncertainty.
* **Information Gain**: IG = Entropy(parent) - Σ(weighted × Entropy(child)). Higher IG = better split. Used by ID3/C4.5.
* **Stopping criteria**: Max depth, min samples per leaf, min information gain.
""")

add("ML Fundamentals", "Explain Random Forest vs Gradient Boosting (XGBoost, LightGBM).", """
* **Random Forest (Bagging)**:
  - Trains many independent trees in parallel on bootstrap samples.
  - Each split considers random subset of features.
  - Aggregates predictions by averaging (regression) or majority vote (classification).
  - Reduces variance. Robust to overfitting.
* **Gradient Boosting (Boosting)**:
  - Trains trees sequentially; each corrects errors of the ensemble so far.
  - Each tree fits the residual errors (negative gradient of loss).
  - Reduces bias. More prone to overfitting → needs regularization.
* **XGBoost**: Adds L1/L2 regularization, handles missing values, parallel tree construction.
* **LightGBM**: Histogram-based splitting, leaf-wise growth (faster on large data).
""")

add("ML Fundamentals", "What is cross-validation? Why is it important?", """
Cross-validation splits data into K folds, trains on K-1 folds and validates on the remaining fold, rotating K times.
* **K-Fold CV**: Standard approach. K=5 or K=10 most common.
* **Stratified K-Fold**: Maintains class distribution in each fold. Essential for imbalanced datasets.
* **Leave-One-Out (LOO)**: K = N. Computationally expensive but unbiased.
* **Why important**:
  1. More reliable performance estimate than a single train/test split.
  2. Detects overfitting.
  3. Uses all data for both training and validation.
  4. Critical for hyperparameter tuning.
""")

add("ML Fundamentals", "How do you handle imbalanced datasets?", """
When classes are heavily skewed (e.g., 1% fraud), standard accuracy is misleading.
* **Data-level techniques**:
  1. **Oversampling minority**: SMOTE (Synthetic Minority Over-sampling) creates synthetic examples.
  2. **Undersampling majority**: Random removal or Tomek Links.
  3. **Combination**: SMOTE + Tomek Links.
* **Algorithm-level techniques**:
  1. **Class weights**: Assign higher penalty for misclassifying minority class.
  2. **Cost-sensitive learning**: Different misclassification costs.
  3. **Focal Loss**: Down-weights easy examples, focuses on hard ones.
* **Evaluation**: Use Precision, Recall, F1, PR-AUC instead of accuracy.
""")

add("ML Fundamentals", "What is feature engineering? Common techniques.", """
Feature engineering transforms raw data into informative features that improve model performance.
* **Techniques**:
  1. **Encoding categoricals**: One-hot encoding, label encoding, target encoding.
  2. **Scaling numericals**: Min-Max normalization, Z-score standardization.
  3. **Binning**: Convert continuous to categorical (age groups).
  4. **Polynomial features**: Create interaction terms (x₁ × x₂) and powers (x²).
  5. **Log/Box-Cox transforms**: Handle skewed distributions.
  6. **Time features**: Extract day, month, day-of-week, is_weekend from timestamps.
  7. **Text features**: TF-IDF, word counts, n-grams.
  8. **Domain knowledge**: Ratios, aggregations, rolling statistics.
""")

add("ML Fundamentals", "What is the Kernel Trick in SVMs?", """
Support Vector Machines find the optimal hyperplane that maximizes the margin between classes.
* **Kernel Trick**: When data is not linearly separable, the kernel function maps data into a higher-dimensional space where it becomes separable — WITHOUT explicitly computing the transformation.
* **Common kernels**:
  - Linear: K(x,y) = x·y
  - Polynomial: K(x,y) = (x·y + c)^d
  - RBF/Gaussian: K(x,y) = exp(-γ||x-y||²) — most popular, handles complex boundaries
  - Sigmoid: K(x,y) = tanh(αx·y + c)
* **Key insight**: Kernel functions compute dot products in high-dimensional space efficiently.
""")

add("ML Fundamentals", "Explain PCA (Principal Component Analysis).", """
PCA is an unsupervised dimensionality reduction technique.
* **How it works**:
  1. Standardize the data (mean=0, std=1).
  2. Compute the covariance matrix.
  3. Calculate eigenvalues and eigenvectors.
  4. Sort eigenvectors by eigenvalue (descending).
  5. Select top-k eigenvectors (principal components).
  6. Project data onto these components.
* **Result**: Transforms features into orthogonal components that capture maximum variance.
* **Choosing k**: Use explained variance ratio. Keep components that explain ≥95% of total variance.
* **Limitations**: Linear only, loses interpretability, sensitive to scaling.
""")

add("ML Fundamentals", "K-Means vs KNN: What's the difference?", """
Completely different algorithms despite similar names:
* **K-Means** (Unsupervised Clustering):
  - Groups unlabeled data into K clusters.
  - Minimizes within-cluster distance to centroids.
  - Training: O(I × K × N × D). Prediction: O(K × D).
  - Choose K: Elbow method, Silhouette score.
* **KNN** (Supervised Classification/Regression):
  - Classifies new points based on K nearest neighbors' labels.
  - Lazy learner — no training phase.
  - Prediction: O(N × D) per query (slow on large datasets).
  - Choose K: Cross-validation (use odd K to avoid ties).
""")

add("ML Fundamentals", "What is Logistic Regression? Is it regression or classification?", """
Despite the name, Logistic Regression is a CLASSIFICATION algorithm.
* **How it works**: Applies sigmoid function σ(z) = 1/(1+e^(-z)) to a linear combination of features, outputting a probability between 0 and 1.
* **Decision boundary**: Threshold at 0.5 (or optimized threshold).
* **Loss function**: Binary Cross-Entropy (log loss): L = -[y·log(p) + (1-y)·log(1-p)].
* **Assumptions**: Linear decision boundary, features are independent, no multicollinearity.
* **Multiclass**: One-vs-Rest (OvR) or Softmax (multinomial).
""")

add("ML Fundamentals", "What is Gradient Descent? Types and differences.", """
Gradient Descent is an optimization algorithm that minimizes the loss function by iteratively updating parameters in the direction of steepest descent.
* **Update rule**: θ = θ - α · ∇L(θ), where α is the learning rate.
* **Types**:
  1. **Batch GD**: Uses entire dataset per update. Stable but slow.
  2. **Stochastic GD (SGD)**: Uses one random sample per update. Fast but noisy.
  3. **Mini-Batch GD**: Uses a small batch (32, 64, 128). Best trade-off — most common.
* **Learning rate**: Too high → diverges. Too low → very slow convergence.
* **Advanced optimizers**: Adam (adaptive learning rates), RMSprop, Adagrad.
""")

add("ML Fundamentals", "What is hyperparameter tuning? Common strategies.", """
Hyperparameters are settings configured before training (not learned from data). Tuning finds the best combination.
* **Strategies**:
  1. **Grid Search**: Exhaustive search over predefined parameter grid. Guaranteed to find best in grid but exponentially expensive.
  2. **Random Search**: Randomly samples parameter combinations. Often finds good results faster than grid search.
  3. **Bayesian Optimization**: Uses probabilistic model to intelligently choose next parameters. Efficient for expensive evaluations.
  4. **Optuna/Hyperopt**: Automated frameworks implementing Bayesian and TPE strategies.
* **Always use cross-validation** during tuning to avoid overfitting to the validation set.
""")

add("ML Fundamentals", "What is overfitting? How do you detect and prevent it?", """
Overfitting: Model learns noise and patterns specific to training data, failing to generalize.
* **Detection**:
  - Training accuracy >> validation accuracy.
  - Large gap between training and validation loss curves.
  - Model performs poorly on unseen data.
* **Prevention**:
  1. More training data.
  2. Regularization (L1, L2, dropout).
  3. Cross-validation.
  4. Early stopping (stop training when validation loss starts increasing).
  5. Simpler model architecture.
  6. Data augmentation (for images).
  7. Feature selection (remove irrelevant features).
  8. Ensemble methods.
""")

add("ML Fundamentals", "What is the curse of dimensionality?", """
As the number of features (dimensions) increases, the volume of the feature space grows exponentially, making data extremely sparse.
* **Effects**:
  1. Distance metrics become meaningless (all points are equally far apart).
  2. Models need exponentially more data to generalize.
  3. Overfitting risk increases dramatically.
  4. Computation time and storage increase.
* **Solutions**:
  1. Feature selection (remove irrelevant features).
  2. Dimensionality reduction (PCA, t-SNE, UMAP).
  3. Feature engineering (domain-driven feature creation).
  4. Regularization.
""")

add("ML Fundamentals", "What is a confusion matrix? Explain TP, FP, TN, FN.", """
A confusion matrix is a table showing actual vs predicted classifications:
* **True Positive (TP)**: Correctly predicted positive.
* **False Positive (FP)**: Incorrectly predicted positive (Type I error).
* **True Negative (TN)**: Correctly predicted negative.
* **False Negative (FN)**: Incorrectly predicted negative (Type II error).
* **Derived metrics**:
  - Accuracy = (TP+TN)/(TP+TN+FP+FN)
  - Precision = TP/(TP+FP) — "Of predicted positives, how many are correct?"
  - Recall = TP/(TP+FN) — "Of actual positives, how many did we find?"
  - F1 = 2×(Precision×Recall)/(Precision+Recall)
""")

# ═══════════════════════════════════════════════════════════════
# ML METRICS (10 questions)
# ═══════════════════════════════════════════════════════════════

add("ML Metrics", "Explain ROC curve and AUC. When is PR-AUC better?", """
* **ROC Curve**: Plots True Positive Rate (Recall) vs False Positive Rate at various classification thresholds.
* **AUC (Area Under ROC Curve)**: Summarizes ROC curve. AUC=1 is perfect, AUC=0.5 is random.
* **PR-AUC (Precision-Recall AUC)**: Plots Precision vs Recall. Better for imbalanced datasets because:
  - ROC-AUC can be misleadingly high when negatives dominate (high TN inflates FPR denominator).
  - PR-AUC focuses only on the positive class, giving a more honest performance picture.
""")

add("ML Metrics", "What is RMSE vs MAE vs MAPE? When to use each?", """
* **MAE (Mean Absolute Error)**: Average of |actual - predicted|. Robust to outliers. Interpretable in original units.
* **RMSE (Root Mean Squared Error)**: √(mean of (actual - predicted)²). Penalizes large errors more heavily than MAE. Use when large errors are especially costly.
* **MAPE (Mean Absolute Percentage Error)**: Average of |actual-predicted|/|actual| × 100. Scale-independent (percentage). Bad when actual values are near zero.
* **R² (Coefficient of Determination)**: 1 - (SS_res/SS_tot). Proportion of variance explained. R²=1 is perfect, R²=0 is as good as predicting the mean.
""")

add("ML Metrics", "What is the F1 Score? When would you prefer precision over recall?", """
* **F1 Score**: Harmonic mean of Precision and Recall. F1 = 2PR/(P+R). Ranges from 0 to 1.
* **Prefer Precision when**: False positives are costly (e.g., spam filter — marking important email as spam is bad).
* **Prefer Recall when**: False negatives are costly (e.g., cancer detection — missing a cancer patient is dangerous).
* **F-beta score**: Generalized version. β>1 weighs recall higher, β<1 weighs precision higher.
""")

add("ML Metrics", "What is log loss (cross-entropy loss)? Why is it preferred for classification?", """
* **Log Loss** = -1/N × Σ[yᵢ·log(pᵢ) + (1-yᵢ)·log(1-pᵢ)]
* Measures how far predicted probabilities are from actual labels.
* **Why preferred**: Unlike accuracy (discrete), log loss penalizes confident wrong predictions heavily. A model predicting 0.99 for a negative class gets a much higher penalty than one predicting 0.51.
* **Perfect model**: Log loss = 0. Random guessing: Log loss = 0.693 (binary).
""")

# ═══════════════════════════════════════════════════════════════
# STATISTICS (10 questions)
# ═══════════════════════════════════════════════════════════════

add("Statistics", "Explain the Central Limit Theorem (CLT).", """
The CLT states that the sampling distribution of the sample mean approaches a normal distribution as sample size (n) increases, regardless of the underlying population distribution.
* **Conditions**: Samples are independent, identically distributed (i.i.d.), and n ≥ 30 (rule of thumb).
* **Implication**: Mean of sample means = population mean (μ). Standard error = σ/√n.
* **Why it matters**: Enables hypothesis testing and confidence intervals even when population distribution is unknown.
""")

add("Statistics", "What is the difference between Type I and Type II errors?", """
* **Type I Error (False Positive)**: Rejecting the null hypothesis when it is actually true. Probability = α (significance level, typically 0.05).
* **Type II Error (False Negative)**: Failing to reject the null hypothesis when it is actually false. Probability = β.
* **Power** = 1 - β = probability of correctly detecting a true effect.
* **Trade-off**: Reducing α increases β (and vice versa). Increasing sample size reduces both errors.
* **Example**: Medical test — Type I: healthy person diagnosed as sick. Type II: sick person diagnosed as healthy.
""")

add("Statistics", "What is a p-value? How do you interpret it?", """
The p-value is the probability of observing data as extreme as (or more extreme than) the observed results, assuming the null hypothesis is true.
* **Interpretation**: Small p-value (< 0.05) = strong evidence against H₀ → reject H₀.
* **p-value is NOT**: The probability that H₀ is true. It's about the data, not the hypothesis.
* **Common thresholds**: p < 0.05 (significant), p < 0.01 (highly significant), p < 0.001 (very highly significant).
* **Caution**: Statistical significance ≠ practical significance. Large samples can make trivial effects "significant."
""")

add("Statistics", "Explain correlation vs causation. What is the Pearson correlation coefficient?", """
* **Correlation**: Two variables move together (positive or negative relationship). Does NOT imply one causes the other.
* **Causation**: A change in one variable DIRECTLY causes a change in another. Requires controlled experiments (A/B tests, RCTs) to establish.
* **Pearson's r**: Measures LINEAR correlation between two variables. Range: [-1, 1].
  - r = 1: Perfect positive linear relationship.
  - r = 0: No linear relationship (can still have non-linear relationship!).
  - r = -1: Perfect negative linear relationship.
* **Spearman's ρ**: Measures monotonic relationship (rank-based). More robust to outliers.
""")

add("Statistics", "What is a confidence interval? How do you interpret a 95% CI?", """
A confidence interval gives a range of plausible values for a population parameter.
* **95% CI interpretation**: If we repeated the experiment many times and computed a CI each time, 95% of those intervals would contain the true population parameter.
* **Formula** (for mean): x̄ ± z × (σ/√n), where z=1.96 for 95% CI.
* **Width depends on**: Sample size (larger n → narrower CI), confidence level (higher confidence → wider CI), variability (higher σ → wider CI).
* **Common misconception**: It does NOT mean there's a 95% probability the parameter is in THIS interval.
""")

add("Statistics", "Design an A/B test. What are the key steps and pitfalls?", """
* **Steps**:
  1. **Define hypothesis**: H₀ (no difference), H₁ (difference exists).
  2. **Choose metric**: Primary (conversion rate) and guardrail metrics.
  3. **Sample size calculation**: Using baseline rate, MDE, α=0.05, power=0.80.
  4. **Randomize**: Randomly assign users to control (A) and treatment (B).
  5. **Run experiment**: For full duration (avoid peeking!).
  6. **Analyze**: Statistical test (Z-test, t-test, chi-squared).
  7. **Decision**: If p < 0.05 and effect is practically significant, deploy.
* **Pitfalls**: Peeking (inflates false positive rate), novelty effect, sample ratio mismatch, Simpson's paradox, network effects.
""")

# ═══════════════════════════════════════════════════════════════
# DATA ANALYSIS & BI (20 questions)
# ═══════════════════════════════════════════════════════════════

add("Data Analysis", "Describe the end-to-end Data Analysis Lifecycle.", """
1. **Define Objectives**: Clarify the business question.
2. **Data Collection**: SQL queries, APIs, log files, web scraping.
3. **Data Cleaning / Wrangling**: Handle missing values, remove duplicates, fix data types, detect outliers, merge datasets.
4. **EDA (Exploratory Data Analysis)**: Descriptive statistics (mean, median, std), visualizations (histograms, box plots, scatter plots), correlations.
5. **Data Modeling**: Statistical tests (t-tests, chi-squared) or ML models.
6. **Visualization & Reporting**: Dashboards (Tableau, PowerBI), presentations.
""")

add("Data Analysis", "How do you handle missing values? Strategies and trade-offs.", """
* **Detection**: df.isnull().sum(), df.info(), missing percentage per column.
* **Strategies**:
  1. **Deletion**: Drop rows (df.dropna()) if <5% missing and MCAR (Missing Completely At Random).
  2. **Mean/Median/Mode Imputation**: Simple, fast. Risk: reduces variance, distorts relationships.
  3. **Forward/Backward Fill**: For time-series data.
  4. **KNN Imputer**: Uses K nearest neighbors to estimate values. Better accuracy.
  5. **Iterative Imputer (MICE)**: Models each missing feature as function of others.
  6. **Indicator variable**: Add a binary column is_missing_X to capture missingness pattern.
* **Trade-offs**: Deletion loses data. Simple imputation biases distributions. Complex imputation is computationally expensive.
""")

add("Data Analysis", "Explain Normalization vs Standardization.", """
* **Normalization (Min-Max Scaling)**: x_norm = (x - x_min) / (x_max - x_min). Scales to [0,1]. Use for algorithms that don't assume normal distribution (KNN, Neural Networks, image data).
* **Standardization (Z-score)**: x_std = (x - μ) / σ. Centers at mean=0, std=1. Unbounded. Use for algorithms assuming normal distribution (Linear Regression, PCA, SVM).
* **Key difference**: Standardization is less sensitive to outliers. Normalization is bounded.
* **RobustScaler**: Uses median and IQR instead of mean/std. Best when outliers are present.
""")

add("Data Analysis", "How do you detect and handle outliers?", """
* **Detection methods**:
  1. **IQR method**: Outlier if value < Q1 - 1.5×IQR or > Q3 + 1.5×IQR.
  2. **Z-score**: Outlier if |z| > 3.
  3. **Visual**: Box plots, scatter plots, histograms.
  4. **Isolation Forest**: ML-based anomaly detection.
* **Handling**:
  1. **Trimming**: Remove outliers (if data errors).
  2. **Capping/Winsorization**: Cap at 1st/99th percentile.
  3. **Log transform**: Reduces skewness.
  4. **Robust methods**: Use median instead of mean, use algorithms robust to outliers (trees).
  5. **Keep them**: If they represent valid extreme cases (fraud detection).
""")

add("Data Analysis", "What is EDA? What visualizations would you use?", """
EDA (Exploratory Data Analysis) explores datasets to summarize characteristics, find patterns, and detect anomalies.
* **Univariate**: Histograms (distribution), box plots (outliers), bar charts (categorical).
* **Bivariate**: Scatter plots (correlation), heatmaps (correlation matrix), grouped bar charts.
* **Multivariate**: Pair plots, parallel coordinates, dimensionality reduction plots (PCA, t-SNE).
* **Time-series**: Line plots, seasonal decomposition.
* **Key tools**: pandas.describe(), df.corr(), seaborn, matplotlib, plotly.
""")

add("Data Analysis", "What is ETL vs ELT? When to use which?", """
* **ETL (Extract, Transform, Load)**: Data is transformed BEFORE loading into the warehouse. Traditional approach for structured data.
  - Use when: Data needs cleaning/conforming before storage. Limited warehouse compute.
* **ELT (Extract, Load, Transform)**: Data is loaded raw into the warehouse, then transformed using warehouse compute power. Modern approach.
  - Use when: Cloud data warehouses (Snowflake, BigQuery) with massive compute. Need flexibility to transform data differently for different use cases.
* **Tools**: ETL: Informatica, Talend. ELT: dbt, Snowflake, BigQuery.
""")

# ═══════════════════════════════════════════════════════════════
# DATA VISUALIZATION (10 questions)
# ═══════════════════════════════════════════════════════════════

add("Data Visualization", "When to use bar chart vs line chart vs scatter plot?", """
* **Bar Chart**: Compare categories or discrete groups. Show frequency, count, or aggregated values. Vertical for categories, horizontal for long labels.
* **Line Chart**: Show trends over time. Continuous data on x-axis (dates, time). Use for time-series, progress tracking.
* **Scatter Plot**: Show relationship between two continuous variables. Detect correlation, clusters, outliers.
* **Histogram**: Show distribution/frequency of a single continuous variable. Detect skewness, modality.
* **Box Plot**: Show distribution summary (median, quartiles, outliers). Compare distributions across groups.
* **Heatmap**: Show magnitude in 2D matrix (correlation, confusion matrix).
""")

add("Data Visualization", "What is Tableau? Key features for data analysis.", """
Tableau is a business intelligence and data visualization tool.
* **Key features**:
  1. **Drag-and-drop interface**: No coding required for most visualizations.
  2. **Data connectors**: Connect to databases, Excel, CSV, cloud sources.
  3. **Calculated fields**: Custom metrics using built-in functions.
  4. **Dashboard creation**: Combine multiple visualizations into interactive dashboards.
  5. **LOD Expressions**: Level of Detail expressions for complex aggregations at different granularities.
  6. **Parameters**: Dynamic user inputs that control filters and calculations.
  7. **Tableau Server/Cloud**: Share dashboards with stakeholders.
""")
