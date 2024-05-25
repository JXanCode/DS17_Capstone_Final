import streamlit as st
import pandas as pd
import numpy as np
import pickle

def load_model():
    with open('xgb_final_model.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data['model']
scaler = data['scaler']

def load_data():
    df = pd.read_csv('data/friday_data_1976.csv')
    df.set_index('model_date',inplace=True)
    return df


friday_1976 = load_data()

def ranges(df,column):
    min_value = df[column].min()
    max_value = df[column].max()
    return f'{min_value:.2f} to {max_value:.2f}'



def show_predict_page():
    st.title("10-Year U.S. Treasury Yields Predictor")
    st.write("### Use the following fields to predict the 3-month change in the 10-year constant maturity U.S. Treasury yield.")
    st.write("#### Historical range is provided for each variable.")

    M2V = st.number_input(f"Velocity of M2 Money Stock [{ranges(friday_1976,'M2V')}]")
    PSAVERT = st.number_input(f"Personal Saving Rate (%) [{ranges(friday_1976,'PSAVERT')}]")
    UNRATE = st.number_input(f"Unemployment Rate (%) [{ranges(friday_1976,'UNRATE')}]")
    CPIAUCSL_pc = st.number_input(f"Quarterly % change in CPI [{ranges(friday_1976,'CPIAUCSL_pc')}]")
    CPILFESL_pc = st.number_input(f"Quarterly % change in Core CPI [{ranges(friday_1976,'CPILFESL_pc')}]")
    CSUSHPINSA_pc = st.number_input(f"Quarterly % change in S&P CoreLogic Case-Shiller U.S. National Home Price Index [{ranges(friday_1976,'CSUSHPINSA_pc')}]")
    GDPC1_pc = st.number_input(f"Quarterly % change in Real GDP (2017 dollars) [{ranges(friday_1976,'GDPC1_pc')}]")
    GFDEBTN_pc = st.number_input(f"Quarterly % change in Total Federal Debt [{ranges(friday_1976,'GFDEBTN_pc')}]")
    M1SL_pc = st.number_input(f"Quarterly % change in M1 (Money Supply) [{ranges(friday_1976,'M1SL_pc')}]")
    PAYEMS_pc = st.number_input(f"Quarterly % change in U.S. Non-farm Employees [{ranges(friday_1976,'PAYEMS_pc')}]")
    GSPC_pc = st.number_input(f"Quarterly % change in S&P 500 Index [{ranges(friday_1976,'^GSPC_pc')}]")
    TermSpread = st.number_input(f"Term Spread (10-year minus 2-year U.S. Treasury yield) [{ranges(friday_1976,'TermSpread')}]")

    ok = st.button("Predict yield change")

    if ok:
        X = np.array([[M2V, PSAVERT, UNRATE, CPIAUCSL_pc, CPILFESL_pc,
                       CSUSHPINSA_pc, GDPC1_pc, GFDEBTN_pc, M1SL_pc,
                       PAYEMS_pc, GSPC_pc, TermSpread]])
        X_scaled = scaler.transform(X)
        X_final = X_scaled.astype(float)

        yield_change = model.predict(X_final)

        if yield_change == 0:
            yield_category = 'less than -0.5'
        elif yield_change == 2:
            yield_category = 'greater than 0.5'
        else:
            yield_category = 'between -0.5 and 0.5'

        
        st.subheader(f"Predicted yield change in 3 months from today is {yield_category}")
    
    
    st.write("")
    st.write("")
    st.write("#### Description of variables:")
    st.write("")

    st.write(f"**Velocity of M2 Money Stock:** Ratio of nominal GDP to M2 money supply.")
    st.write(f"**Personal Saving Rate:** Savings as a percentage of disposable income.")
    st.write(f"**Unemployment Rate:** Unemployed persons as a percentage of the labor force (persons employed or looking for work). ")
    st.write(f"**Quarterly % change in CPI:** 3-month percentage change in the consumer price index for all urban consumers.")
    st.write(f"**Quarterly % change in Core CPI:** 3-month percentage change in the consumer price index (less food and energy items) for all urban consumers. ")
    st.write(f"**Quarterly % change in S&P CoreLogic Case-Shiller U.S. National Home Price Index:** 3-month percentage change in the value of single-family homes in 20 major metropolitan areas in the U.S.")
    st.write(f"**Quarterly % change in Real GDP:** 3-month percentage change in Gross Domestic Product adjusted for inflation in the value of goods and services.")
    st.write(f"**Quarterly % change Total Federal Debt:** 3-month percentage change in the total amount of outstanding debt by the U.S. Government.")
    st.write(f"**Quarterly % change in M1 (Money Supply):** 3-month percentage change in M1 money supply (currency and liquid deposits).")
    st.write(f"**Quarterly % change in U.S. Non-farm Employees:** 3-month percentage change in U.S. workers, excluding proprietors, household employees, unpaid volunteers and farm employees.")
    st.write(f"**Quarterly % change in S&P 500 Index:** 3-month percentage change in large cap U.S. equities.")
    st.write(f"**Term Spread:** difference between 10-year Treasury yield and 2-year Treasury yield.")

    st.write("")
    st.write("")
    st.write("Sources: FRED, Investopedia")
        

