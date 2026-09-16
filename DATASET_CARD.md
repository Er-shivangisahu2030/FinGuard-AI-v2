# FinGuard AI v2 Dataset Card

## Composition

- Real component: 2,083 usable complaint narratives from the supplied CFPB-derived CSV.
- Synthetic component: 3,000 project-generated scenarios.
- Total: 5,083 records.
- Split: 80% training, 20% held-out testing with stratification.

## Why hybrid data?

The public complaint sample provides real-world financial complaint language. Synthetic scenarios fill coverage gaps for India-specific digital-payment cases such as UPI, OTP and KYC scams that are not sufficiently represented in the supplied sample.

## Important distinction

`source=REAL_CFPB` means the record originated from the supplied CFPB-derived data file. `source=SYNTHETIC` means it was generated for this project. Synthetic records are not real customer complaints.

## Labeling

FinGuard categories are a project-specific taxonomy. Real CFPB records are mapped from their product/issue/sub-issue fields using a conservative rule-based mapping. The mapping is not an official CFPB classification.

## Model benchmark

On the current held-out hybrid test set:

- Linear SVM: 87.41% accuracy, 0.875 weighted F1
- Logistic Regression: 87.12% accuracy, 0.873 weighted F1
- Multinomial Naive Bayes: 81.51% accuracy, 0.821 weighted F1

These numbers are benchmark results for this dataset, not evidence of production fraud-detection accuracy.
