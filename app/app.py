import pandas as pd
from pandas.errors import *
import streamlit as st
from streamlit_echarts import st_echarts
from pathlib import Path
import pickle

app_path = Path(__file__).resolve().parent 
static_path = app_path / "static"
models_path = app_path.parent / "models"
data_path = app_path.parent / "data"


def render_page():
    """Renders current page"""

    st.set_page_config("Financial Worries Predictor", 
                   page_icon="🧠", 
                   layout="wide")

    st.html("static/index.html")

    st.logo(str(static_path / "logo_lema.png"), 
            size="large")

    st.header("Financial Worries Model App 🪙")
    st.markdown(
        """
        <h5 style='color: grey; text-align: left; margin-bottom: 4px'>Predict your financial worry propensity</h5>
        <hr style='border-top: 1px solid #f5770c; margin-top: 4px; margin-bottom: 0'>

        """, unsafe_allow_html=True
    )


    st.markdown(
        """
        <p style='margin-top: 10px;'>&nbsp;</p>
        """, unsafe_allow_html=True)


    dash = st.Page("app_pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)
    simulator = st.Page("app_pages/simulations.py", title="Simulator", icon=":material/speed:")
    about = st.Page("app_pages/info.py", title="About", icon=":material/info:")

    
    pg = st.navigation(
        [dash, simulator, about]
    )

    pg.run()
    col1, col2, col3 = st.columns([3, 2, 2])
    col2.download_button("Technical Report", str(static_path / "relatorio.pdf"), "technical_report.pdf")

    with st.sidebar:
        
        st.logo(str(static_path / "logo_lema.png"), 
                    size="large")
        st.write("#")

        

render_page()