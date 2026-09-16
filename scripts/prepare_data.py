import re
from pathlib import Path
import pandas as pd
import spacy

INPUT_FILE = 'data/raw/complaints_hybrid.csv'
OUTPUT_FILE = 'data/processed/complaints_cleaned.csv'

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    nlp = None
    print('en_core_web_sm not found; using lightweight fallback tokenizer.')

def clean_text(text):
    text = str(text or '').lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if nlp is None:
        return ' '.join(w for w in text.split() if len(w) > 1)
    doc = nlp(text)
    return ' '.join(t.lemma_ for t in doc if not t.is_stop and not t.is_punct and not t.is_space and len(t.text) > 1)

df = pd.read_csv(INPUT_FILE, low_memory=False)
for col, default in [('complaint_text',''),('payment_method','UNKNOWN'),('sentiment','neutral'),('category','OTHER'),('source','UNKNOWN')]:
    df[col] = df[col].fillna(default).astype(str)
df['transaction_amount'] = pd.to_numeric(df.get('transaction_amount', 0), errors='coerce').fillna(0)
df['unauthorized_transaction'] = pd.to_numeric(df.get('unauthorized_transaction', 0), errors='coerce').fillna(0).astype(int)
df['severity'] = pd.to_numeric(df.get('severity', 1), errors='coerce').fillna(1).clip(1,4).astype(int)
df = df[df['complaint_text'].str.len() >= 30].copy()
df = df.drop_duplicates(subset=['complaint_id']).copy()
df['clean_text'] = df['complaint_text'].apply(clean_text)
df = df[df['clean_text'].str.strip() != ''].reset_index(drop=True)
cols = ['complaint_id','complaint_text','clean_text','category','product','issue','sub_issue','transaction_amount','payment_method','unauthorized_transaction','severity','sentiment','source','created_at']
cols = [c for c in cols if c in df.columns]
Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
df[cols].to_csv(OUTPUT_FILE, index=False)
print('Saved', OUTPUT_FILE, 'shape=', df.shape)
print('\nCategory distribution:\n', df['category'].value_counts())
print('\nSource distribution:\n', df['source'].value_counts())
