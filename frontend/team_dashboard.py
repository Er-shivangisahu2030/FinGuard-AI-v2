import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
load_dotenv(); API=os.getenv('API_BASE_URL','http://127.0.0.1:8000')
CATEGORIES=['UPI_FRAUD','OTP_SCAM','FAKE_KYC','PHISHING','CARD_FRAUD','UNAUTHORIZED_TRANSACTION','REFUND_ISSUE','PAYMENT_FAILURE','ACCOUNT_ISSUE','OTHER']
st.set_page_config(page_title='FinGuard Team Dashboard',page_icon='📊',layout='wide')
st.title('📊 FinGuard AI - Support Team Dashboard')
st.caption('Risk-prioritized complaint queue with human verification and model feedback')
try:
    r=requests.get(f'{API}/complaints?limit=200',timeout=15); r.raise_for_status(); rows=r.json()
    if rows:
        df=pd.DataFrame(rows)
        c1,c2,c3,c4=st.columns(4)
        c1.metric('Complaints',len(df)); c2.metric('Critical',int((df.risk_level=='CRITICAL').sum())); c3.metric('High',int((df.risk_level=='HIGH').sum())); c4.metric('Avg risk',round(df.risk_score.mean(),1))
        st.subheader('Priority queue')
        queue=df.sort_values(['risk_score','created_at'],ascending=[False,True])
        cols=[c for c in ['complaint_id','complaint_text','category','risk_score','risk_level','priority','assigned_team','payment_method','created_at'] if c in queue.columns]
        st.dataframe(queue[cols],use_container_width=True)
        st.subheader('Risk distribution')
        st.bar_chart(df['risk_level'].value_counts())
        st.subheader('Human verification')
        selected=st.selectbox('Select complaint',queue['complaint_id'].tolist())
        row=queue[queue.complaint_id==selected].iloc[0]
        st.write('**Complaint:**',row['complaint_text'])
        st.write('**Model prediction:**',row['category'])
        corrected=st.selectbox('Verified category',CATEGORIES,index=CATEGORIES.index(row['category']) if row['category'] in CATEGORIES else 0)
        comment=st.text_input('Reviewer comment')
        use=st.checkbox('Use verified label for retraining',value=True)
        if st.button('Save verification',type='primary'):
            payload={'complaint_id':selected,'predicted_category':row['category'],'corrected_category':corrected,'reviewer_decision':'reviewed','reviewer_comment':comment,'is_used_for_training':use}
            fr=requests.post(f'{API}/feedback',json=payload,timeout=120); fr.raise_for_status(); result=fr.json()
            st.success('Feedback saved.')
            if 'retraining' in result: st.info(f"Retraining result: {result['retraining']}")
            st.rerun()
    else:
        st.info('No complaints in the database yet.')
except Exception as e:
    st.error(f'Backend/database unavailable: {e}')
