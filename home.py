import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle

def main():
    loaded_model = pickle.load(open('https://github.com/Dharmik34/Bank-Term-Deposit-Subscription/blob/master/model.pkl', 'rb'))
    st.title("Check whether :bust_in_silhouette: client will :bell: subscribe a term deposit:money_with_wings:?")
    st.caption(':red[ All the filed values are required ]')

    df = pd.read_csv('final_bank_df.csv')
    df['day_last_contacted'] = df['day_last_contacted'].astype(str)
    print(df.info())
    df_col = []
    df_cat_col = []
    unique_values = []

    df_col = df.columns
    df_col = ['age', 'job_type', 'marital_status', 'education',
       'has_credit', 'avg_yearly_balance', 'housing_loan', 'personal_loan',
       'contact_type', 'day_last_contacted', 'month_last_contacted',
       'no_of_contact', 'contacts_before_campaign','previous_campaign_outcome', 'y',
       'call_duration_segment']

    df_cat_col = ['job_type', 'marital_status', 'education',
    'has_credit', 'housing_loan', 'personal_loan',
    'contact_type', 'day_last_contacted', 'month_last_contacted',
    'contacts_before_campaign','previous_campaign_outcome', 'y',
    'call_duration_segment']

    print(df_cat_col)

    for i in df_cat_col:
        unique_values.append(df[i].unique())

    def get_values(field):
        index_of_col = df_cat_col.index(field)
        return unique_values[index_of_col]

    enc = LabelEncoder()

    def transformer(value):
        for i in df_cat_col:
            for j in df[i]:
                if(j==value):
                    encoder = enc.fit(df[i])
                    encoded_value = encoder.transform([value])
                    return  encoded_value
                    break
        # index_of_col = df_cat_col.index(value)
        # encoder = enc.fit(unique_values[index_of_col])
        # encoded_value = encoder.transform([value])
        # return encoded_value

    with st.form("my_form"):

        age = st.number_input('Enter the year?',step=1)

        job_type = st.selectbox(
            'Choose the job_type',
            get_values('job_type'))

        marital_status = st.selectbox(
            'Choose the marital_status',
            get_values('marital_status'))

        education = st.selectbox(
            'Choose the education level',
            get_values('education'))

        has_credit = st.selectbox(
            'Do you have credit?',
            get_values('has_credit'))

        avg_yearly_balance = st.number_input('Enter your average yearly balance?',step=100)

        housing_loan = st.selectbox(
            'Do you have house loan?',
            get_values('housing_loan'))

        personal_loan = st.selectbox(
            'Do you have personal loan?',
            get_values('personal_loan'))

        contact_type = st.selectbox(
            'Please choose contact-type',
            get_values('contact_type'))

        day_last_contacted = st.selectbox(
            'A day when last contacted?',
            get_values('day_last_contacted'))

        month_last_contacted = st.selectbox(
            'A month when last contacted?',
            get_values('month_last_contacted'))

        no_of_contact = st.number_input('Enter number of contacts?',step=1)

        contacts_before_campaign = st.selectbox(
            'Contacted before campaign?',
            get_values('contacts_before_campaign'))

        previous_campaign_outcome = st.selectbox(
            'What is the outcome of previous campaign?',
            get_values('previous_campaign_outcome'))

        call_duration_segment = st.selectbox(
            'What is the call duration segment?',
            get_values('call_duration_segment'))

        submitted = st.form_submit_button("Submit")
    #
        if submitted:
            input = []
            converted_input = []
            job_type = transformer(job_type)
            marital_status = transformer(marital_status)
            education = transformer(education)
            has_credit = transformer(has_credit)
            housing_loan = transformer(housing_loan)
            personal_loan = transformer(personal_loan)
            contact_type = transformer(contact_type)
            day_last_contacted = transformer(day_last_contacted)
            month_last_contacted = transformer(month_last_contacted)
            contacts_before_campaign = transformer(contacts_before_campaign)
            previous_campaign_outcome = transformer(previous_campaign_outcome)
            call_duration_segment = transformer(call_duration_segment)
            input = [age,job_type,marital_status,education,has_credit,avg_yearly_balance,housing_loan,personal_loan,contact_type,day_last_contacted,month_last_contacted,no_of_contact,contacts_before_campaign,previous_campaign_outcome,call_duration_segment]

            for i in input:
                # st.text(i)
                converted_input.append(str(i).strip('[]'))
            for i in range(0, len(converted_input)):
                converted_input[i] = int(converted_input[i])
            converted_input = np.array(converted_input)
            # print(converted_input)

            prediction = loaded_model.predict([converted_input])
            # print('Prediction',prediction)

            if prediction[0] == 0:
                prediction = ":red[The customer :bust_in_silhouette: won't subscribe :no_bell: this scheme]"
            elif prediction[0] == 1:
                prediction = ":green[ The customer :bust_in_silhouette: will subscribe :bell: this scheme]"
            else:
                prediction = ":red[Invalid input! :x:]"
            st.subheader(prediction)

if __name__ == '__main__':
    main()
