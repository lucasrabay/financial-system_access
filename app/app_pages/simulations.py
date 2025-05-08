# -*- coding: UTF-8 -*-
"""Import Modules"""

import pandas as pd
from pandas.errors import *
import streamlit as st
from streamlit_echarts import st_echarts
from pathlib import Path
import pickle
import numpy as np

import torch
import torch.nn as nn


class Simulator:
    """Model Simulator class"""

    def __init__(self):
        """Initialize Instance"""

        self.app_path = Path(__file__).resolve().parent.parent
        self.static_path = self.app_path / "static"
        self.models_path = self.app_path.parent / "models"
        self.data_path = self.app_path.parent / "data"

        # self.best_model = pickle.load(open(self.models_path/"best_ordinal_nn_model.pkl", "rb"))
        # self.best_model_params = self.best_model["results"]

        self.int_model = pickle.load(open(self.models_path/"basic_logistic_regression.pkl", "rb"))



    def __call__(self):

        self.data_input()


    @st.cache_data(show_spinner=False)
    def read_data(_self, path):
        
        data = pd.read_csv(path, encoding="latin1")

        return data


    # kind of a back end
    def predict_class(_self, _dataframe: pd.DataFrame) -> tuple[int, float]:
        """
        Predicts the class and the probability of financial worries
        Returns the worry class and the probability predicted
        """

        if _dataframe.empty:
            raise EmptyDataError("O DataFrame fornecido para previsão está vazio")

        try:
            pred_class = _self.int_model.predict(_dataframe)
            pred_proba = _self.int_model.predict_proba(_dataframe)

        except Exception as error:
            raise OSError(error) from error

        return pred_class, pred_proba



    def data_input(self):

        data = self.read_data(self.data_path / "micro_world_139countries.csv")
        dummies_data  = pd.get_dummies(data, columns=['economy'], drop_first=True)

        col1, col2, col3 = st.columns([.05, 10, .05])

        col2.subheader("Model Data Input")

        col1, col2, col3 = st.columns([.05, 10, .05])

        with st.form("Features Form", border=False):

            c1, c2 = st.columns(2)

            countries_list = data["economy"].unique().tolist()
            countries_list.remove("China")

            with c1:
                country = st.selectbox("Select your country", countries_list, index=countries_list.index("Brazil"))
                sexo = st.selectbox("Select your sex", ["Male", "Female"], index=0)
                st.markdown(
                    """
                    <p style='margin-top: 0.5px;'>&nbsp;</p>
                    """, unsafe_allow_html=True)
                emp_in = st.checkbox("I'm in the laborial market.", value=True)
                fin_account = st.checkbox("I have a financial account (bank, stock broker).", value=True)
                borrowed = st.checkbox("I have borrowed money with any FI or person in the last year.", value=True)
                saved = st.checkbox("I have made any saving project in the last year.", value=True)
                receive_wages = st.checkbox("I have received salarial payment.", value=True)
                receive_transfers = st.checkbox("I have received any government tranfers.", value=True)
                pension = st.checkbox("I have received benefit from any government pension.", value=True)

            with c2:
                inc_quant = st.selectbox("Select Your Income Quantile", [1, 2, 3, 4, 5], index=2)
                age = st.slider("Select your age", 0, 100, 30)
                st.markdown(
                    """
                    <p style='margin-top: 0.5px;'>&nbsp;</p>
                    """, unsafe_allow_html=True)
                pay_utils = st.checkbox("I have payed utility bills through financial accounts.", value=True)
                digital_payment = st.checkbox("I have received or made any digital payments/transfers in the last year.", value=True)
                mobile_owner = st.checkbox("I'm owner of a mobile phone.", value=True)
                internet_access = st.checkbox("I have internet access.", value=True)
                debit_cards = st.checkbox("I have a debit card or at least have used one in the last year.", value=True)
                credit_cards = st.checkbox("I have a credit card or at least have used one in the last year.", value=True)
                payed_balance = st.checkbox("I have payed my credit card balance in full in the last year.", value=True)

            submitted = c1.form_submit_button("Submit")

            if submitted:

                df = pd.DataFrame(
                    {
                        "female": [1 if sexo == "Female" else 0],
                        "age": [age],
                        "inc_q": [inc_quant],
                        "emp_in": [float(emp_in)],
                        "account": [float(fin_account)],
                        "borrowed": [float(borrowed)],
                        "saved": [float(saved)],
                        "receive_wages": [float(receive_wages)],
                        "receive_transfers": [float(receive_transfers)],
                        "receive_pension": [float(pension)],
                        "pay_utilities": [float(pay_utils)],
                        "anydigpayment": [float(digital_payment)],
                        "mobileowner": [float(mobile_owner)],
                        "internetaccess": [float(internet_access)],
                        "debit_card": [float(debit_cards)],
                        "credit_card": [float(credit_cards)],
                        "paid_balance_regularly": [float(payed_balance)]
                    }
                )

                country_cols = [col for col in dummies_data.columns if "economy" in col.lower()]
                country_cols.remove("economycode")
                country_cols.remove("economy_China")

                col1, col2 = st.columns([5, 8])

                df_temp = (
                    pd.DataFrame({
                        "country_col": country_cols,
                        "country": countries_list[1:]
                        })
                        .assign(
                            chosen_country = lambda x: x["country"].apply(
                                lambda y: 1 if y == country else 0
                                )
                                )
                                .drop(columns="country")
                                ).T
                
                
                df_temp.columns = df_temp.iloc[0, :]
                df_temp = df_temp[1:]
                df_temp.index = [0]
                df_temp = df_temp.rename(columns={"economy_Côte d'Ivoire": "economy_CÃ´te d'Ivoire",
                                        "economy_Türkiye": "economy_TÃ¼rkiye"})

                df = pd.concat([df, df_temp], axis=1)

                class_, proba = self.predict_class(df)

                st.write(class_)
                st.write(proba)

                c1.write("#")


if __name__ == "__main__":
    simulator = Simulator()
    simulator()