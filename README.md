# Personalized-Nutrition-Recommendation-System

Overview:

This project is an end-to-end machine learning–based personalized nutrition recommendation system that predicts daily calorie and macronutrient requirements and analyzes meal-type patterns using user health, lifestyle, and dietary information.
The system focuses on accurate nutritional requirement prediction (regression) and includes a meal-type classification analysis supported by statistical validation.

Key Features:

Personalized diet recommendations based on health and lifestyle inputs
Daily calorie requirement prediction
Macronutrient prediction (carbohydrates, protein, fats)
Meal-type classification analysis (Balanced, Low-Carb, High-Protein, Low-Fat)
Web deployment using Flask, HTML, and CSS.

Dataset:

Personalized Medical Diet Recommendations Dataset (Kaggle)
Contains demographic, health, lifestyle, and dietary preference features

Methodology:

  Data Preprocessing:
  
  Handled categorical and numerical features using a ColumnTransformer
  Applied Ordinal Encoding for categorical variables and Standard Scaling for numerical variables
  Built a unified preprocessing + modeling pipeline
  
  Regression (Core Component):

  Implemented Multi-Output Regression to predict:

  Daily calories
  Carbohydrates
  Protein
  Fats

Models tested:Gradient Boosting, XGBoost (best performance with Gradient Boosting)
Achieved R² score of 0.94, indicating strong predictive performance

Classification (Analytical Component):

Built a multi-class classification model to analyze meal-type patterns

Evaluated using:

Accuracy
ROC–AUC curves
Confusion matrices

Performed statistical feature analysis using:

Mutual Information
Chi-Square tests

Results & Analysis:

Regression models demonstrated strong performance due to clear numerical relationships between inputs and nutritional targets
Classification performance remained close to random guessing (ROC–AUC ≈ 0.5)
Statistical tests showed near-zero dependency between features and meal-type labels
Conclusion: Classification performance is limited by dataset characteristics rather than model choice
This analysis highlights the importance of validating data suitability before over-optimizing models.

Deployment:

Deployed as a web application using Flask
Frontend built with HTML and CSS
Users can input health and lifestyle details to receive personalized nutritional recommendations

Tech Stack:

Python
Scikit-learn
Pandas, NumPy
Flask
HTML, CSS

Key Learnings:

Importance of statistical validation in machine learning
Difference between regression-friendly and classification-friendly datasets
Diagnosing model limitations using ROC–AUC, confusion matrices, and feature relevance tests.

Future Improvements:

Use a dataset with clearer class definitions for meal-type classification
Explore clustering-based meal grouping
Integrate real-time nutrition APIs for dynamic meal planning
