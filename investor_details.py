import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_investor_details(df,investor):
    st.title(investor)
    
    # load the recent 5 investments of the investor
    last5_df = df[df["investors"].str.contains(investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)
    
    col1, col2 = st.columns(2)
    with col1:
    
        # biggest investments
        st.subheader("Biggest Investments")
        big_series = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        big_series = big_series[big_series>0]
        
        if not big_series.empty:           
        
            fig, ax = plt.subplots()
            ax.bar(big_series.index,big_series.values) #type: ignore
            st.pyplot(fig)
        else:
            st.warning("No BIGGEST Investment Available")
    
    
    with col2:
        
        # Sector - wise Investment
        st.subheader("Sectors invested in")
        vertical_series = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        vertical_series = vertical_series[vertical_series>0]
        
        if vertical_series.empty:
            st.warning("No sector data available for this investor")
        else:
            fig1, ax1 = plt.subplots()
            ax1.pie(vertical_series,labels=vertical_series.index,autopct="%1.1f%%") #type: ignore
            st.pyplot(fig1)
        
    col1, col2 = st.columns(2)
    
    with col1:
        # Stage(round) wise Investment
        st.subheader("Round-wise Investing")
        stage_series = df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
        
        stage_series = stage_series[stage_series > 0]
        if stage_series.empty:
            st.warning("No round-wise data available")
            
        else:
            fig3, ax3 = plt.subplots()
            ax3.pie(stage_series,labels=stage_series.index,autopct="%1.1f%%") #type: ignore
            st.pyplot(fig3)
        
    with col2:
        
        # City-wise Investment
        
        st.subheader("City-wise Investing")
        city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        city_series = city_series[city_series>0]
        if city_series.empty:
            st.warning("No city-wise data available")

        else:
            fig3, ax3 = plt.subplots()
            ax3.pie(city_series,labels=city_series.index,autopct="%1.1f%%") #type: ignore
            st.pyplot(fig3)
    
    col1, col2 = st.columns(2)

    with col1:
        # Year wise Investment    
        year_series = df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
        st.subheader("YoY Investment")
        if len(year_series) < 2:
            st.warning("Not enough data for YoY trend")
        else:
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
            
        if len(rows)==0:
            st.warning("No similar Investor exist")
        else:
            similar_investor_df = pd.DataFrame(rows)
            list_investor_df = pd.DataFrame(similar_investor_df.sort_values(by=1,ascending=False)[0].unique()[:5]) #type: ignore
            list_investor_df.rename(columns = {0:"Similar Investor"},inplace=True)
            st.dataframe(list_investor_df)