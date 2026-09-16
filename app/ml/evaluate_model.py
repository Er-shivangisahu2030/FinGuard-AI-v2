import json
from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

MODEL_FILE = "models/complaint_classifier.pkl"
TEST_FILE = "data/processed/test.csv"
REPORT_FILE = "models/evaluation_report.json"
PRED_FILE = "data/processed/test_predictions.csv"

model = joblib.load(MODEL_FILE)
test = pd.read_csv(TEST_FILE)
pred = model.predict(test["clean_text"].fillna(""))
report = classification_report(test["category"], pred, output_dict=True, zero_division=0)
print(classification_report(test["category"], pred, zero_division=0))
labels = sorted(test["category"].unique())
cm = confusion_matrix(test["category"], pred, labels=labels)
fig, ax = plt.subplots(figsize=(12, 9))
ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, xticks_rotation=45)
plt.tight_layout()
plt.savefig("models/confusion_matrix.png", dpi=150)
plt.close()
out = test[["complaint_id", "complaint_text", "category"]].copy()
out["predicted_category"] = pred
out["prediction_correct"] = out["category"] == out["predicted_category"]
out.to_csv(PRED_FILE, index=False)
with open(REPORT_FILE, "w") as f:
    json.dump({"classification_report": report}, f, indent=2)
print("Saved evaluation report and predictions.")
