import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide",page_title="StartUp Analysis")

df = pd.read_csv("startup_cleaned.csv")
df["date"] = pd.to_datetime(df["date"],errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month


def load_investor_details(investor):
    st.title(investor)
    
    # load the recent 5 investments of the investor
    last5_df = df[df["investors"].str.contains(investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)
    
    col1, col2 = st.columns(2)
    with col1:
    
        # biggest investments
        big_series = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values) #type: ignore
        st.pyplot(fig)
    
    
    with col2:
        
        # Sector - wise Investment
        vertical_series = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()

        st.subheader("Sectors invested in")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%1.1f%%") #type: ignore
        st.pyplot(fig1)
        
    col1, col2 = st.columns(2)
    
    with col1:
        # Stage(round) wise Investment
        stage_series = df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
        
        st.subheader("Round-wise Investing")
        fig3, ax3 = plt.subplots()
        ax3.pie(stage_series,labels=stage_series.index,autopct="%1.1f%%") #type: ignore
        st.pyplot(fig3)
        
    with col2:
        
        # City-wise Investment
        
        city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        
        st.subheader("City-wise Investing")
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series,labels=city_series.index,autopct="%1.1f%%") #type: ignore
        st.pyplot(fig3)
    
    col1, col2 = st.columns(2)

    with col1:
        # Year wise Investment    
        year_series = df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
        st.subheader("YoY Investment")
        fig2, ax2 = plt.subplots()
        ax2.plot(year_series.index,year_series.values) #type: ignore
        st.pyplot(fig2)
    
    with col2:
        # Similar Investment
        st.subheader("Similar Investor")
        similar_investor = df[df["investors"].str.contains(investor)]["investors"].str.split(",").sum()
        similar_investor.remove(investor)
        rows = []
        for x in similar_investor:
            
            total = df[df["investors"].str.contains(x,regex=False)]["amount"].sum()
            rows.append([x,total])
            

        similar_investor_df = pd.DataFrame(rows)
        list_investor_df = pd.DataFrame(similar_investor_df.sort_values(by=1,ascending=False)[0].unique()[:5]) #type: ignore
        list_investor_df.rename(columns = {0:"Similar Investor"},inplace=True)
        st.dataframe(list_investor_df)

def load_overall_analysis():
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
    
    

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

if (option == "Overall Analysis"):
    
    load_overall_analysis()
        
        
    
        
elif (option == "Startup"):
    st.title("StartUp Analysis")
    st.sidebar.selectbox("Select Startup",sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")

    
    
    
else:
    
    selected_investor = st.sidebar.selectbox("Select Investor",sorted(set(df["investors"].str.split(",").sum())))
    
    btn2 = st.sidebar.button("Find Investor Details")
    
    if btn2:
        load_investor_details(selected_investor)







