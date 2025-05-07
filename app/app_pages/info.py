import pandas as pd
from pandas.errors import *
import streamlit as st
from streamlit_echarts import st_echarts
from pathlib import Path
import pickle


class About:
    """Model and authors
      info class"""
    
    def __init__(self):

        # import local modules

        from graphs import Graphs
        self.graphs = Graphs()
          
        self.app_path = Path(__file__).resolve().parent.parent
        self.static_path = self.app_path / "static"
        self.models_path = self.app_path.parent / "models"
        self.data_path = self.app_path.parent / "data"

        col1, col2, col3 = st.columns([.05, 10, .05])
        self.column1, self.column2 = col2.columns(2)
            
    
    def __call__(self):

        self.about_app()
        self.about_authors()
        self.about_model()
            
            
    def about_app(self):
         
        with self.column1:
            
            st.html("<span class='any_container'></span>")
            st.markdown("""
                        <h5>About the App</h5>
                        <p style='font-size:18px;'> Hello, user 👋🏽! This is our <span style='font-weight: bold;'> Machine Learning project App</span>, 
                        designed to expose and apply the results of our Financial Worries Model. The referred model allows anyone to measure their propensity to have financial worries,
                        based on some social, economic and demographic features. </p><br>

                        <p style='font-size:18px;'>By the way, two models were chosen to complete the project, to explore both of 
                        the ideas of Machine Learning models:
                        the accuracy and the interpretability. The chosen models were an Ordinal Neural Network, 
                        trying to score the best accuracy and a Logistic Regression, with the intepretability idea in mind. </p><br>

                        <p style='font-size:18px;'>Bellow, by answering the form, you can try our models! The results should be displayed when you submit your answer!
                        Important tip: if you are young, try to put more advanced ages, to see if, maintaining your nowadays habits, 
                        you could have some stress in the future!</p>""", unsafe_allow_html=True)
    
    
    def about_authors(self):
         
        with self.column2:
            st.html("<span class='any_container'></span>")
            st.markdown("""
                    <h5>About the authors</h5>
                    """, unsafe_allow_html=True)

            st.markdown("""
                <style>
                    table, tr, td {
                        border: none !important;
                    }
                </style>

                <table style="width: 100%; border-collapse: collapse; font-size: 16px;">
                <tr>
                    <td style="width: 30%; padding: 10px; vertical-align: top; text-align: center;">
                    <img src="https://avatars.githubusercontent.com/u/140542061?v=4" alt="Dev 1" style="border-radius: 10px; width: 125px;"><br>
                    <strong>Lucas Rabay</strong>
                    </td>
                    <td style="padding: 10px; vertical-align: top;">
                    <p> </p>
                    <ul>
                        <li> Estudante de Ciência de Dados para Negócios - UFPB.</li>
                        <li> Estagiário em Ciência de Dados na V360.</li>
                        <li> Integrante da Liga de Inteligênica Artificial da UFPB - TAIL.</li>
                    </ul>
                    </td>
                </tr>
                <tr>
                    <td style="width: 30%; padding: 10px; vertical-align: top; text-align: center;">
                    <img src="https://avatars.githubusercontent.com/u/141172256?v=4" alt="Dev 2" style="border-radius: 10px; width: 125px;"><br>
                    <strong>Pedro Melo</strong>
                    </td>
                    <td style="padding: 10px; vertical-align: top;">
                    <p> </p>
                    <ul>
                        <li> Estudante de Ciência de Dados para Negócios - UFPB.</li>
                        <li> Estagiário em Ciência de Dados na Sicredi.</li>
                        <li> Integrante da Liga de Mercado Financeiro UFPB - LMF.</li>
                    </ul>
                    </td>
                </tr>
                </table>
            """, unsafe_allow_html=True)


    def about_model(self):

        params_data = pd.read_csv(self.data_path / "logistic_regression_bayes_coef.csv")

        with st.container():
            st.html("<span class='any_container'></span>")
            col1, col2 = st.columns(2)

            with col1:
                options = self.graphs.h_bar_plot(params_data)
                st_echarts(options=options, theme="dark", height="600px", width="100%")

            # with col2:
                # PUT ACCURACY STATS
                


if __name__ == "__main__":
    
    about = About()
    about()