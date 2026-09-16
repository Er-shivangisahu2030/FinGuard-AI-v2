# FinGuard AI v2

FinGuard AI is an end-to-end financial complaint intelligence and risk-assessment prototype. It combines publicly available CFPB complaint narratives with synthetic India-specific digital-payment scenarios. The system classifies complaint text, detects scam indicators, calculates an explainable risk score, routes cases to support teams, stores complaints in MySQL, and supports human verification with model versioning and retraining.

## What changed in v2

- Uses a **hybrid dataset** instead of a fully synthetic dataset.
- Includes **2,083 CFPB complaint narratives** from the uploaded source file.
- Adds **3,000 synthetic scenarios** to cover UPI, OTP, KYC, phishing and other India-specific cases that are not well represented in the CFPB sample.
- Final working dataset: **5,083 records**.
- Adds a `source` field: `REAL_CFPB` or `SYNTHETIC`.
- Compares Logistic Regression, Linear SVM and Multinomial Naive Bayes using TF-IDF.
- Current evaluation on the held-out test set is about **87.4% accuracy / 0.875 weighted F1** for the selected Linear SVM. These metrics are for this hybrid dataset only and are not production fraud-detection performance.
- Adds human verification and **versioned retraining**. A customer complaint is not automatically treated as a training label. Only a verified reviewer label can enter the retraining pool.

## Architecture

```text
Real CFPB complaints + Synthetic India-specific scenarios
                         |
                         v
                  Clean + label data
                         |
                         v
                   spaCy preprocessing
                         |
                         v
                  TF-IDF (1-2 grams)
                         |
              +----------+----------+
              |          |          |
              v          v          v
             LR         SVM         NB
              +----------+----------+
                         |
                         v
                  Complaint category
                         |
              +----------+----------+
              |          |          |
              v          v          v
        Scam indicators Risk engine Guidance
                         |
                         v
                      Routing
                         |
                         v
                       MySQL
                         |
                 Support dashboard
                         |
                  Human verification
                         |
                         v
                 Verified training data
                         |
                         v
                Versioned retraining
```

## Dataset

The included working dataset is `data/raw/complaints_hybrid.csv`.

### Real source

The real portion comes from the CFPB Consumer Complaint Database. The supplied source file contains 100,000 rows, but only 2,083 rows contain usable complaint narratives after filtering. Those narrative records are retained for the hybrid dataset.

### Synthetic portion

Synthetic records supplement gaps in the public sample, especially:

- UPI fraud
- OTP scams
- fake KYC messages
- phishing
- card fraud
- unauthorized transactions
- refund issues
- payment failures
- account access problems
- other support cases

Synthetic records are explicitly marked with `source=SYNTHETIC`. They are not presented as real customer complaints.

## Final dataset columns

| Column | Purpose |
|---|---|
| `complaint_id` | Unique complaint identifier |
| `complaint_text` | Main NLP input |
| `category` | FinGuard ML target |
| `product` | Financial product/source context |
| `issue` | Original or synthetic issue |
| `sub_issue` | Detailed issue |
| `transaction_amount` | Risk-engine input |
| `payment_method` | Risk-engine/context field |
| `unauthorized_transaction` | Risk signal |
| `severity` | Risk signal |
| `sentiment` | Supporting context |
| `source` | `REAL_CFPB` or `SYNTHETIC` |
| `created_at` | Record date |

## FinGuard categories

```text
UPI_FRAUD
OTP_SCAM
FAKE_KYC
PHISHING
CARD_FRAUD
UNAUTHORIZED_TRANSACTION
REFUND_ISSUE
PAYMENT_FAILURE
ACCOUNT_ISSUE
OTHER
```

The mapping from CFPB's original taxonomy to these categories is a project-specific labeling layer. It is not an official CFPB taxonomy.

## Setup on Windows CMD

### 1. Create and activate environment

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Optional but recommended:

```cmd
python -m spacy download en_core_web_sm
```

The project still works with a lightweight tokenizer if the spaCy model is unavailable.

### 2. Configure MySQL

Edit `.env`:

```text
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=finguard_ai
API_BASE_URL=http://127.0.0.1:8000
```

### 3. Rebuild the hybrid dataset

The source file used by the script should be placed at:

```text
data/raw/cfpb_finguard_dataset.csv
```

Then run:

```cmd
python scripts\build_hybrid_dataset.py
python scripts\prepare_data.py
python scripts\split_data.py
python app\ml\train_model.py
python app\ml\evaluate_model.py
```

### 4. Initialize MySQL tables

From the project root:

```cmd
python -m app.database.models
```

### 5. Start FastAPI

```cmd
uvicorn app.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 6. Start customer application

Open another CMD window, activate the environment and run:

```cmd
python -m streamlit run frontend\customer_app.py
```

### 7. Start support dashboard

In another CMD window:

```cmd
python -m streamlit run frontend\team_dashboard.py
```

## Human-in-the-loop retraining

The project intentionally does **not** retrain from an unverified customer prediction.

```text
New complaint
     |
     v
ML prediction
     |
     v
MySQL complaint record
     |
     v
Human reviewer checks prediction
     |
     +---- correct/corrected label
     |
     v
Verified feedback
     |
     v
Retraining service
     |
     v
complaint_classifier_v2.pkl
     |
     v
Active model registry updated
```

When a reviewer checks **Use verified label for retraining** in the dashboard, the API stores the feedback and retrains the classifier. The new model is saved as a versioned file and also promoted as the active model.

This avoids the dangerous pattern of feeding the model's own unverified predictions back into training.

## API endpoints

- `GET /health`
- `POST /analysis/analyze`
- `POST /complaints`
- `GET /complaints`
- `GET /complaints/priority`
- `GET /complaints/{complaint_id}`
- `POST /feedback`
- `GET /analytics/summary`

## Interview explanation

A concise explanation is:

> "I built FinGuard AI as a complaint-intelligence and risk-assessment system. Because real financial complaint data is sensitive and India-specific labeled fraud data is difficult to obtain, I used a hybrid dataset. The primary real component is public CFPB complaint narratives, while synthetic records supplement India-specific UPI, OTP and KYC scenarios. I keep the source field so the two data types remain auditable. The complaint text goes through spaCy preprocessing and TF-IDF, and I compared Logistic Regression, Linear SVM and Naive Bayes. A separate rule-based risk engine combines complaint category, scam indicators, transaction context and severity. Complaints are stored in MySQL and exposed through FastAPI and Streamlit. Finally, support staff can verify predictions, and only verified feedback is used to retrain a new version of the model."

## Limitations

- CFPB data represents US consumer complaints and is not a statistical sample of all consumers.
- The synthetic component is for coverage of project-specific scenarios and must not be presented as real customer data.
- CFPB-to-FinGuard labels are a project-specific mapping and contain some unavoidable subjectivity.
- The reported model metrics describe this hybrid benchmark, not production fraud detection.
- A high risk score is decision support, not proof of fraud.
- Human investigation remains the final authority for financial actions.
