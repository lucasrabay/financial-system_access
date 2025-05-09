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

        st.markdown("""
            <style>
                .dev-row {
                    display: flex;
                    justify-content: center;
                    gap: 40px;
                    margin-top: 20px;
                }
                .dev-card {
                    text-align: center;
                    font-size: 16px;
                }
                .dev-card img {
                    border-radius: 10px;
                    width: 100px;
                    margin-bottom: 5px;
                }
                .dev-card strong {
                    display: block;
                    margin-top: 5px;
                }
            </style>

            <h4>This is the Financial Worry Model App <br><br>The main result of the final project of the Machine Learning Course in UFPB</h4>
            <h4>Authors:</h4>
            <div class="dev-row">
                <div class="dev-card">
                    <img src="https://avatars.githubusercontent.com/u/141172256?v=4" alt="Pedro Melo">
                    <strong>Pedro Melo</strong>
                </div>
                <div class="dev-card">
                    <img src="https://avatars.githubusercontent.com/u/140542061?v=4" alt="Lucas Rabay">
                    <strong>Lucas Rabay</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("#")
        st.write("#")
        st.write("#")

        col1, col2, col3 = st.columns(3, vertical_alignment="center")

        col1.image(str(static_path / "Brasão_UFPB.png"))
        col2.image(str(static_path / "cdn.png"))
        col3.image(str(static_path / "logo_lema.png"))

        

render_page()