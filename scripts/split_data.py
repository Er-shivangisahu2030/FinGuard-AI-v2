import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_FILE='data/processed/complaints_cleaned.csv'
TRAIN_FILE='data/processed/train.csv'
TEST_FILE='data/processed/test.csv'

df=pd.read_csv(INPUT_FILE)
train,test=train_test_split(df,test_size=0.20,random_state=42,stratify=df['category'])
train=train.sample(frac=1,random_state=42).reset_index(drop=True)
test=test.sample(frac=1,random_state=42).reset_index(drop=True)
train.to_csv(TRAIN_FILE,index=False); test.to_csv(TEST_FILE,index=False)
print('Train:',train.shape); print('Test:',test.shape)
print('\nTrain distribution:\n',train['category'].value_counts())
print('\nTest distribution:\n',test['category'].value_counts())
