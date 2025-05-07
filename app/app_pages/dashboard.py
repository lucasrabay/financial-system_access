# -*- coding: UTF-8 -*-
"""Import modules"""

import streamlit as st
from streamlit_echarts import st_echarts
from pathlib import Path
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium

class Dashboard:
    """Dashboard app page class"""

    def __init__(self):

        # import local modules

        from graphs import Graphs

        self.graphs = Graphs()

        self.app_path = Path(__file__).resolve().parent.parent
        self.static_path = self.app_path / "static"
        self.models_path = self.app_path.parent / "models"
        self.data_path = self.app_path.parent / "data"

        self.col_dict = {
            "Sex": "female",
            "Age": "age",
            "Income Quantil": "inc_q",
            "Employed": "emp_in",
            "Account Holder": "account",
            "Borrowed Money": "borrowed",
            "Saved Money": "saved",
            "Recieved Wages": "receive_wages",
            "Received Transfers": "receive_transfers",
            "Received Pension": "receive_pension",
            "Payed for Utilities Services": "pay_utilities",
            "Digital Payments": "anydigpayment",
            "Mobile Owner": "mobileowner",
            "Internet Access": "internetaccess",
            "Debit Card Holder": "debit_card",
            "Credit Card Holder": "credit_card",
            "Payed Balance Regularly": "paid_balance_regularly",
            "Financial Worry Index": "financial_worry"
        }


    def __call__(self):
        """Runs the class routine"""

        self.render_page()

    @st.cache_data(show_spinner=False)
    def read_data(_self):

        path = _self.data_path / "cleaned_data.csv"
        df = pd.read_csv(path)

        return df


    @st.cache_data(show_spinner=False)
    def transform_data(_self, df, by: str):
        """Aggregates the cleaned dataframe"""

        df = df.groupby(by)["financial_worry"].median().reset_index()

        return df


    @st.cache_data(show_spinner=False)
    def make_corr_matrix(_self, df):

        numeric_df = df.select_dtypes(include=['int64', 'float64']).copy()
        corr = numeric_df.corr()

        return corr
    
    def add_age_cuts(self, df):

        bins = [0, 20, 40, 60, 80, df["age"].max()]
        labels = ["0-20", "20-40", "40-60", "60-80", ">80"]

        series = pd.cut(df["age"], bins=bins, labels=labels, include_lowest=True)

        return series 


    def make_map(self):

        path = self.static_path / "ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
        world = gpd.read_file(path)
        df = self.read_data()
        agg_df = self.transform_data(df, "economy")

        merged = world.merge(agg_df, how="left", left_on="NAME", right_on="economy")

        map = folium.Map(location=[0, 0], zoom_start=2)

        folium.Choropleth(
            geo_data=merged,
            name="choropleth",
            data=merged,
            columns=["NAME", "financial_worry"],
            key_on="feature.properties.NAME",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Index"
        ).add_to(map)

        map.save(self.static_path / "map.html")


    def research_dash(self):
        """Renders the research 
        data dashboard"""

        df = self.read_data()

        answers = len(df)
        country_num = df["economy"].nunique()

        corr = self.make_corr_matrix(df)

        c1, c2, c3 = st.columns([4, 5, 4])

        with c1.popover("About the Research", icon=":material/info:"):
            st.markdown("""### **About the Global Findex Database 2021**
The Global Findex 2021 is the latest edition of the World Bank's 
flagship database on financial inclusion. Based on surveys of 128,000 adults
across 123 countries during the COVID-19 pandemic, it provides insights into 
how people use financial services—from digital payments to savings and credit—and 
how they manage financial shocks. The report highlights trends since 2011 and 
identifies persistent gaps, especially for women and low-income individuals. The
data support global efforts to track progress toward financial inclusion and the 
UN Sustainable Development Goals.""")
            
        st.markdown(
            """
            <p style='margin-top: 10px;'>&nbsp;</p>
            """, unsafe_allow_html=True)

        # c1, c2, c3 = st.columns([4, 5, 4])

        c3.markdown(
            """
            <p style='margin-top: 8px;'>&nbsp;</p>
            """, unsafe_allow_html=True)

        with c1.container():
            st.html("<span class='probas'></span>")
            st.metric("Total of Respondents", f"{answers:,}".replace(",", "."))
        with c3.container():
            st.html("<span class='probas'></span>")
            st.metric("Total of Countries", country_num)

        c1, c2 = st.columns([4, 8])

        with c2:
            multi_columns = {key: value for key, value in self.col_dict.items() if df[value].nunique() > 2}
            vars = list(multi_columns.keys())
            selected_var = st.selectbox("Select a Variable", vars, index=(len(vars) - 1))
            st.html("<span class='any_container'></span>")
            df_counts = df[[self.col_dict[selected_var]]]
            df_counts.columns = ["values"]
            options = self.graphs.histogram(df_counts, selected_var)

            st_echarts(options, height="460px", theme="dark")

        with st.container():
            st.html("<span class='any_container'></span>")
            options = self.graphs.correlation_heatmap(corr)
            _, col1 = st.columns([0.7, 10])
            with col1:
                st_echarts(options, height="500px", theme="dark")

        with c1:
            binary_cols = {key: value for key, value in self.col_dict.items() if df[value].nunique() <= 2}
            vars = list(binary_cols.keys())
            selected_var = st.selectbox("Select a Variable", vars, index=(len(vars) - 1))
            st.html("<span class='any_container'></span>")
            df_counts = df[[self.col_dict[selected_var]]]
            df_counts.columns = ["values"]
            options = self.graphs.pie_plot(df_counts, selected_var)

            st_echarts(options, height="460px", theme="dark")


    def info_dashboard(self):
        """Renders the real info dashboard"""
        
        df = self.read_data()

        c1, c2, c3 = st.columns(3)
        countries = df["economy"].unique().tolist()
        country_filter = c1.selectbox("Select a Country", ["All"] + countries, index=0)
        country_filter = countries if country_filter == "All" else [country_filter]

        sex_filter = c2.selectbox("Select a Gender", ["All"] + ["Male", "Female"], index=0)
        sex_translator = {
            "Male": 0, "Female": 1
        }
        sex_filter =  [0, 1] if sex_filter == "All" else [sex_translator[sex_filter]]

        ages_cuts = self.add_age_cuts(df)
        df["ages_cut"] = ages_cuts
        ages_filter = c3.selectbox("Select an Age Range", ["All"] + list(ages_cuts), index=0)
        ages_filter = list(ages_cuts) if ages_filter == "All" else [ages_filter]

        df_filtered = df[df["ages_cut"].isin(ages_filter)
                        & df["female"].isin(sex_filter) 
                        & df["economy"].isin(country_filter)]


        c1, c2 = st.columns([4, 6])

        with c1:

            st.html("<span class='any_container'></span>")

            st.markdown("""
                <h5>Financial Worry Map</h5>
                """, unsafe_allow_html=True)

            with open(self.static_path / "map.html", "r", encoding="utf-8") as file:
                html_content = file.read()
            
            st.components.v1.html(html_content, height=540)

        
        with c2:
            visuable_cols = {key: value for key, value in self.col_dict.items() if df[value].nunique() <= 10}
            vars = list(visuable_cols.keys())
            selected_var = st.selectbox("Select a Variable", vars, index=(len(vars) - 1))
            st.html("<span class='any_container'></span>")
            df_agg = df_filtered[[self.col_dict[selected_var], "financial_worry"]].dropna()
            options = self.graphs.boxplot(df_agg, self.col_dict[selected_var], selected_var)

            st_echarts(options, height="500px", theme="dark")


        with st.container():
            st.html("<span class='any_container'></span>")

            
            with st.expander("Options"):
                column1, column2 = st.columns(2)
                sex_check = column1.checkbox("Female", value=True)
                employed_check = column2.checkbox("Employed", value=True)
                saved_money_check = column1.checkbox("Saved Money", value=True)
                account_check = column2.checkbox("Account Holder", value=True)
                cred_card_check = column1.checkbox("Credit Card Holder", value=True)
                phone_check = column2.checkbox("Mobile Phone Owner", value=True)


            df_filtered_v2 = df_filtered[(df_filtered["female"] == int(sex_check))
                & (df_filtered["emp_in"] == int(employed_check))
                & (df_filtered["saved"] == int(saved_money_check))
                & (df_filtered["account"] == int(account_check))
                & (df_filtered["credit_card"] == int(cred_card_check))
                & (df_filtered["mobileowner"] == int(phone_check))]
            
            df_filtered_v2 = self.transform_data(df_filtered_v2, "age").sort_values("age")

            options = self.graphs.echart_dict(df_filtered_v2)

            st_echarts(options, height="500px")



    def render_page(self):

        options = st.radio(" ", ["Information Dashboard", "Research and Sample Dashboard"], 
                           index=0, horizontal=True)

        if options == "Information Dashboard":
            self.info_dashboard()
        elif options == "Research and Sample Dashboard":
            self.research_dash()

if __name__ == "__main__":

    dash = Dashboard()
    dash()