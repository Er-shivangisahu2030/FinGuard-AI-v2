
# FinGuard AI v2: Financial Complaint Intelligence and Risk Assessment

## Project Overview

FinGuard AI is a financial complaint analysis system designed to help support teams understand customer complaints, identify possible scam indicators, assess risk, and direct cases to the appropriate team.

The project uses a combination of real consumer complaint narratives from the CFPB Consumer Complaint Database and synthetic scenarios based on Indian digital payment issues. The synthetic data covers cases such as UPI fraud, OTP scams, fake KYC messages, phishing, card fraud, and failed transactions.

The system uses Natural Language Processing (NLP) and machine learning to classify complaints, while a rule-based risk engine calculates an explainable risk score. It also stores complaint records in MySQL and provides dashboards for customers and support teams. A human verification process allows reviewers to correct predictions and contribute verified labels to future model training.

## Key Features

- **Hybrid dataset:** Combines 2,083 real CFPB complaint narratives with 3,000 synthetic scenarios, giving a total of 5,083 records.
- **Complaint classification:** Uses TF-IDF features and compares Logistic Regression, Linear SVM, and Multinomial Naive Bayes to identify complaint categories.
- **Scam indicator detection:** Checks complaint details for warning signs associated with scams and suspicious transactions.
- **Risk assessment:** Calculates a risk score using relevant complaint and transaction details, helping support teams prioritize cases.
- **Complaint routing:** Directs complaints to the appropriate support team based on their category and risk level.
- **Database management:** Stores complaint records and related information in MySQL.
- **Support dashboard:** Helps reviewers view complaints, examine risk levels, and monitor complaint trends.
- **Human verification:** Allows reviewers to confirm or correct model predictions before feedback is used for retraining.
- **Model versioning:** Keeps track of trained models and supports controlled updates using verified feedback.

## Dataset and Model Evaluation

The working dataset contains 5,083 records. Of these, 2,083 are real complaint narratives from the supplied CFPB dataset, while the remaining 3,000 are synthetic scenarios created to cover India-specific financial issues.

The project compares three machine learning algorithms using TF-IDF features. The selected Linear SVM model achieved approximately **87.4% accuracy and a weighted F1-score of 0.875** on the held-out test set.

These results apply only to the project's hybrid dataset. They should not be interpreted as evidence of real-world fraud detection accuracy.

## Technology Stack

- **Programming Language:** Python
- **NLP:** spaCy, TF-IDF
- **Machine Learning:** Scikit-learn, Logistic Regression, Linear SVM, Multinomial Naive Bayes
- **Backend:** FastAPI, Pydantic
- **Frontend:** Streamlit
- **Database:** MySQL
- **Data Processing:** Pandas, NumPy
- **Model Management:** Versioned model files and verified-feedback retraining workflow

## How the System Works

1. A customer submits a financial complaint through the application.
2. The system cleans the complaint text and extracts relevant features.
3. The trained machine learning model predicts the complaint category.
4. Scam indicators and transaction details are used to calculate a risk score.
5. The system provides relevant guidance and routes the complaint to the appropriate support team.
6. Complaint details and analysis results are stored in MySQL.
7. A support reviewer examines the prediction and corrects it when necessary.
8. Only verified reviewer labels are eligible for use in the retraining process.

## Important Limitations

The project is a prototype for complaint intelligence and risk assessment, not a production-ready fraud detection system. The CFPB dataset primarily represents US consumer complaints, while the synthetic records are designed to introduce Indian payment scenarios. The mapping between the original CFPB categories and FinGuard AI's categories is project-specific.

Risk scores are intended to support human decision-making, not establish that fraud has occurred. Financial actions and final decisions should remain subject to appropriate human review.
