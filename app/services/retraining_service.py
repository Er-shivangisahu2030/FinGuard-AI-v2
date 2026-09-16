from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_FILE=Path('data/processed/complaints_cleaned.csv')
MODEL_DIR=Path('models')


def get_verified_feedback():
    from app.database.connection import get_db_connection
    c=get_db_connection(); cur=c.cursor(dictionary=True)
    cur.execute('''SELECT f.complaint_id, f.corrected_category, c.complaint_text, c.transaction_amount,
                   c.payment_method, c.unauthorized_transaction, c.severity, c.sentiment
                   FROM feedback f JOIN complaints c ON f.complaint_id=c.complaint_id
                   WHERE f.is_used_for_training=TRUE AND f.corrected_category IS NOT NULL AND f.corrected_category <> '' ''')
    rows=cur.fetchall(); cur.close(); c.close(); return pd.DataFrame(rows)


def retrain_from_verified_feedback():
    base=pd.read_csv(BASE_FILE)
    fb=get_verified_feedback()
    if fb.empty:
        return {'status':'skipped','message':'No verified feedback is available for retraining.'}
    from app.ml.preprocessor import clean_text
    fb=fb.rename(columns={'corrected_category':'category'})
    fb['clean_text']=fb['complaint_text'].fillna('').apply(clean_text)
    fb['complaint_id']=fb['complaint_id'].astype(str)
    cols=[c for c in base.columns if c in fb.columns]
    fb=fb[cols].copy()
    combined=pd.concat([base,fb],ignore_index=True)
    combined=combined.drop_duplicates(subset=['complaint_id'],keep='last')
    X=combined['clean_text'].fillna(''); y=combined['category']
    model=Pipeline([('tfidf',TfidfVectorizer(lowercase=False,ngram_range=(1,2),min_df=2,max_df=0.95,sublinear_tf=True)),('classifier',LogisticRegression(max_iter=2000,class_weight='balanced'))])
    model.fit(X,y)
    MODEL_DIR.mkdir(exist_ok=True)
    versions=[]
    for p in MODEL_DIR.glob('complaint_classifier_v*.pkl'):
        try: versions.append(int(p.stem.split('_v')[-1]))
        except ValueError: pass
    version=max(versions,default=1)+1
    version_file=MODEL_DIR/f'complaint_classifier_v{version}.pkl'
    joblib.dump(model,version_file)
    joblib.dump(model,MODEL_DIR/'complaint_classifier.pkl')
    registry={'active_model':version_file.name,'version':version,'model_name':'Logistic Regression','training_rows':len(combined),'verified_feedback_rows':len(fb)}
    (MODEL_DIR/'active_model.json').write_text(json.dumps(registry,indent=2))
    return {'status':'retrained','version':version,'training_rows':len(combined),'verified_feedback_rows':len(fb),'model':version_file.name}
