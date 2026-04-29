import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from investor_details import load_investor_details
from overall_details import load_overall_analysis


st.set_page_config(layout="wide",page_title="StartUp Analysis")


df = pd.read_csv("startup_cleaned.csv")
df["date"] = pd.to_datetime(df["date"],errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month


st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

if (option == "Overall Analysis"):
    load_overall_analysis(df)      
        
elif (option == "Startup"):
    st.title("StartUp Analysis")
    st.sidebar.selectbox("Select Startup",sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")

else:
    selected_investor = st.sidebar.selectbox("Select Investor",sorted(set(df["investors"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(df,selected_investor)







