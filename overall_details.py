import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def load_overall_analysis(df):
    st.title("Overall Analysis")
    
    # total Invested Amount
    total = round(df["amount"].sum())  
    
    # max amount infused in a startup
    max_funding = df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    
    # avg ticket size
    avg_funding = df.groupby("startup")["amount"].sum().mean()
    
    # total funded startups
    num_startups = df["startup"].nunique()
    
    col1,col2,col3,col4 = st.columns(4) 

    with col1:        
        st.metric("Total",str(total) + " Cr")
    with col2:
        st.metric("Max",str(max_funding)+" Cr")
    with col3:
        st.metric("Avg",str(round(avg_funding)) + " Cr")
    with col4:
        st.metric("Funded Startups",num_startups)
    
    # MoM Graph
    st.subheader("MoM Graph")
    selected_option = st.selectbox("Select Type",["Total","Count"])
    if selected_option == "Total":
    
        temp_df = df.groupby(["year","month"])["amount"].sum().reset_index()
    else:
        temp_df = df.groupby(["year","month"])["amount"].count().reset_index()    
        
    temp_df["x_axis"] = temp_df["month"].astype("str") + "-" + temp_df["year"].astype("str")   
    
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df["x_axis"],temp_df["amount"])
    st.pyplot(fig3)