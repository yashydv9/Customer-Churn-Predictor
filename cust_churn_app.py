# importing libraries

import pandas as pd
import streamlit as st
import joblib

model = joblib.load ('churn_pred_model_tuned.pkl')


# building the streamlit app.

st.title ('Customer Churn Prediction App')
st.header ('Enter Customer Details')

gender = st.selectbox ('Gender', ['Female', 'Male'])
tenure = st.number_input ('Tenure (months)', min_value=0, max_value=100, value= 12)
monthly_charges = st.number_input ('Monthly Charges ($)', min_value=0.0, max_value=200.0, value= 50.0)
contract = st.selectbox ('Contract', ['Month-to-Month', 'One Year', 'Two Year'])
payment_method = st.selectbox ('Payment Method', ['Electronic Check', 'Mailed Check', 'Bank Transfer', 'Credit Card'])
internet_service = st.selectbox ('Internet Service', ['DSL', 'Fiber optic', 'No'])
online_security = st.selectbox ('Online Security', ['Yes', 'No', 'No internet service'])
tech_support = st.selectbox ('Tech Support', ['Yes', 'No', 'No internet service'])
paperless_billing = st.selectbox ('Paperless Billing', ['Yes', 'No'])
dependents = st.selectbox ('Dependents', ['Yes', 'No'])


gender_mapping = {'Female': 0, 'Male': 1}
paperless_billing_mapping = {'Yes': 1, 'No': 0}
dependents_mapping = {'Yes': 1, 'No': 0}


gender_encoded = gender_mapping[gender]
paperless_billing_encoded = paperless_billing_mapping[paperless_billing]
dependents_encoded = dependents_mapping[dependents]


input_data = pd.DataFrame ({
    'gender': [gender_encoded],
    'SeniorCitizen': [0],
    'Partner': [0], 
    'Dependents': [dependents_encoded],
    'tenure' : [tenure],
    'PhoneService': [0], 
    'PaperlessBilling': [paperless_billing_encoded],
    'MonthlyCharges': [monthly_charges],
    'Tenure_Group': [0], 
    'PaymentMethod_Credit card': [1 if payment_method == 'Credit Card' else 0],
    'PaymentMethod_Electronic check': [1 if payment_method == 'Electronic Check' else 0],
    'PaymentMethod_Mailed check' : [1 if payment_method == 'Mailed Check' else 0],
    'Contract_One year': [1 if contract == 'One Year' else 0],
    'Contract_Two year': [1 if contract == 'Two Year' else 0], 
    'InternetService_Fiber optic': [1 if internet_service == 'Fiber optic' else 0],
    'InternetService_No': [1 if internet_service == 'No' else 0], 
    'MultipleLines_No phone service': [0],
    'MultipleLines_Yes': [0], 
    'OnlineSecurity_No internet service': [1 if online_security == 'No internet service' else 0],
    'OnlineSecurity_Yes': [1 if online_security == 'Yes' else 0], 
    'OnlineBackup_No internet service': [0],
    'OnlineBackup_Yes': [0], 
    'DeviceProtection_No internet service': [0],
    'DeviceProtection_Yes': [0], 
    'TechSupport_No internet service': [1 if tech_support == 'No internet service' else 0],
    'TechSupport_Yes': [1 if tech_support == 'Yes' else 0], 
    'StreamingTV_No internet service': [0], 
    'StreamingTV_Yes': [0],
    'StreamingMovies_No internet service': [0], 
    'StreamingMovies_Yes': [0],
})

if st.button('Predict Churn'):
    prediction = model.predict (input_data)
    prediction_prob = model.predict_proba(input_data)

    if prediction[0] == 1:
        st.error('This customer is likely to churn.')
    else:
        st.success ('This customer is not likely to churn.')

    st.write (f'Probability of churn: {prediction_prob[0][1]:.2f}')
    with st.sidebar:
        st.image ('gender_vs_churn.png', caption= 'Gender vs Churn')
        st.image ('paymentmethod_vs_churn.png', caption= 'Payment Method vs Churn')
        st.image ('internetservice_vs_churn.png', caption= 'Internet Service vs Churn')
        st.markdown ('[For more graphs and info, click here.](https://github.com/yashydv9/Customer-Churn-Predictor.git)')
