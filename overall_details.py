import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
    
    fig3, ax3 = plt.subplots(figsize=(8,3))
    ax3.plot(temp_df["x_axis"],temp_df["amount"])
    ax3.set_xticks(temp_df["x_axis"][::3])
    for label in ax3.get_xticklabels():
        label.set_rotation(45)
    st.pyplot(fig3)
    
    # Sector-wise Analysis
    st.subheader("Sector-wise Analysis")
    col1,col2 = st.columns(2)
    
    with col1:
        st.write("Top Sectors by Investment Amount")
        top_invested_sector = df.groupby(["vertical"])["amount"].sum().sort_values(ascending=False).head(15)
        fig1,ax1 = plt.subplots()
        ax1.pie(top_invested_sector,labels = top_invested_sector.index,autopct="%1.1f%%") #type: ignore
        st.pyplot(fig1)
    
    with col2:
        st.write("Sector-wise Investment Count (Deal Frequency)")
        top_invested_sector = df.groupby(["vertical"])["amount"].count().sort_values(ascending=False).head(10)
        
        fig1,ax1 = plt.subplots()
        ax1.bar(top_invested_sector.index,top_invested_sector.values) #type: ignore
        for label in ax1.get_xticklabels():
            label.set_rotation(90)
        st.pyplot(fig1)
    
    # City-wise Anaylsis
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("City-wise Anaylsis")
        city_series = df.groupby("city")["amount"].sum().sort_values(ascending=False).head(10)
        
        fig2,ax2 = plt.subplots()
        ax2.pie(city_series,labels=city_series.index,autopct="%1.1f%%")
        st.pyplot(fig2)
    
    with col2:
        st.subheader("Top startups - Year wise")

        temp1 = df.drop_duplicates("startup",keep="first")
        temp_df = temp1.groupby(["year","startup"])["amount"].sum().sort_values(ascending=False).reset_index()
        final_df = temp_df.drop_duplicates(subset=["year"],keep="first").sort_values(by=["year"]).reset_index().drop("index",axis=1)
        st.dataframe(final_df)
        
    col1,col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Investors")
        top_10_investors = df.groupby("investors")['amount'].sum().sort_values(ascending=False).head(9)
        fig1,ax1 = plt.subplots()
        ax1.bar(top_10_investors.index,top_10_investors.values)
        for labels in ax1.get_xticklabels():
            labels.set_rotation(90)
        st.pyplot(fig1)
    
    with col2:
        st.subheader("Types of Funding")
        new_df = df["round"].value_counts().sort_values(ascending=False)
        top_n = 10
        top_rounds = new_df.head(top_n)
        top_rounds["others"] = new_df.iloc[top_n:].sum()
        fig,ax = plt.subplots()
        ax.bar(top_rounds.index,top_rounds.values)
        for labels in ax.get_xticklabels():
            labels.set_rotation(90)
        st.pyplot(fig)
        

    
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Heatmap - Year v/s Month ")
        pt = pd.pivot_table(df,values=["amount"],index=["year"],columns=["month"],aggfunc="sum",fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))        
        sns.heatmap(pt, cmap="YlGnBu", annot=True, fmt=".0f", ax=ax)
        ax.set_title("Funding Heatmap (Year vs Month)")
        st.pyplot(fig)
        
    with col2:
        st.subheader("Heatmap - Top 10 Sectors v/s Year ")
        top_sector = df.groupby("vertical")["amount"].sum().sort_values(ascending=False).head(10).index
        new_df = df[df["vertical"].isin(top_sector)]
        sectorYear_pt = pd.pivot_table(new_df,values=["amount"],columns=["year"],index=["vertical"],aggfunc="sum",fill_value=0)
        fig,ax = plt.subplots(figsize=(10,5))
        sns.heatmap(sectorYear_pt,annot=True,fmt='.0f',cmap="YlOrRd",ax=ax)
        ax.set_title("Funding Heatmap (Sector vs Year)")
        st.pyplot(fig)
                
        