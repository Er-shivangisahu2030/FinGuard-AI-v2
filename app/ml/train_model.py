import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

TRAIN_FILE='data/processed/train.csv'; TEST_FILE='data/processed/test.csv'
MODEL_DIR=Path('models'); MODEL_FILE=MODEL_DIR/'complaint_classifier.pkl'; METADATA_FILE=MODEL_DIR/'model_metadata.json'
train=pd.read_csv(TRAIN_FILE); test=pd.read_csv(TEST_FILE)
X_train,y_train=train['clean_text'].fillna(''),train['category']; X_test,y_test=test['clean_text'].fillna(''),test['category']
models={
 'Logistic Regression': LogisticRegression(max_iter=2000,class_weight='balanced'),
 'Linear SVM': LinearSVC(class_weight='balanced'),
 'Multinomial Naive Bayes': MultinomialNB(),
}
results=[]; trained={}
for name,clf in models.items():
    pipe=Pipeline([('tfidf',TfidfVectorizer(lowercase=False,ngram_range=(1,2),min_df=2,max_df=0.95,sublinear_tf=True)),('classifier',clf)])
    pipe.fit(X_train,y_train); pred=pipe.predict(X_test)
    results.append({'model':name,'accuracy':round(accuracy_score(y_test,pred),4),'precision':round(precision_score(y_test,pred,average='weighted',zero_division=0),4),'recall':round(recall_score(y_test,pred,average='weighted',zero_division=0),4),'f1_score':round(f1_score(y_test,pred,average='weighted',zero_division=0),4)})
    trained[name]=pipe
results_df=pd.DataFrame(results).sort_values(['f1_score','accuracy'],ascending=False).reset_index(drop=True)
best_name=results_df.iloc[0]['model']; best=trained[best_name]
MODEL_DIR.mkdir(exist_ok=True); joblib.dump(best,MODEL_FILE)
metadata={'model_name':best_name,'task':'Complaint Category Classification','feature':'clean_text','vectorizer':'TF-IDF','ngram_range':[1,2],'training_rows':len(train),'testing_rows':len(test),'metrics':results_df.to_dict(orient='records'),'categories':sorted(y_train.unique().tolist()),'dataset_source':'Hybrid: CFPB real complaint narratives + synthetic India-specific digital-payment scenarios'}
with open(METADATA_FILE,'w') as f: json.dump(metadata,f,indent=2)
with open(MODEL_DIR/'active_model.json','w') as f: json.dump({'active_model':'complaint_classifier.pkl','version':1,'model_name':best_name},f,indent=2)
print(results_df.to_string(index=False)); print('Best model:',best_name); print('Saved:',MODEL_FILE)
