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

# best_model = pickle.load(open(models_path/"best_ordinal_nn_model.pkl", "rb"))
# best_model_params = best_model["results"]

# int_model = pickle.load(open(models_path/"basic_logistic_regression.pkl", "rb"))
# int_model_params = int_model["results"]
# print(int_model)

data = pd.read_csv(data_path / "micro_world_139countries.csv", encoding="latin1")
params_data = pd.read_csv(data_path / "logistic_regression_bayes_coef.csv")



# kind of a back end
def predict_class(dataframe: pd.DataFrame, params) -> tuple[int, float]:
    """
    Predicts the class and the probability of financial worries
    Returns the worry class and the probability predicted

    Params:
    dataframe: the pd.DataFrame containing the features to be predicted
    params: the params of the model used to predict the final class/proba
    """

    if dataframe.empty:
        raise EmptyDataError("O Dataframe fornecido para previsão está vazio")

    try:
        pred_class = params.predict(dataframe), 
        pred_proba = params.predict_proba(dataframe)

    except Exception as error:
        raise OSError(error) from error

    return pred_class, pred_proba


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


col1, col2, col3 = st.columns([.05, 10, .05])
column1, column2 = col2.columns(2)

with column1.container():
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
    
with column2.container():
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

col2.markdown(
    """
    <p style='margin-top: 0.5px;'>&nbsp;</p>
    """, unsafe_allow_html=True)

col2.subheader("\tModel Data Input")

col1, col2, col3 = st.columns([.05, 10, .05])
with col2.expander("Expand Form"):

    with st.form("Features Form", border=False):

        c1, c2 = st.columns(2)

        countries_list = data["economy"].unique().tolist()

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
            feceive_transfers = st.checkbox("I have received any government tranfers.", value=True)
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
            debit_cards = st.checkbox("I have a debit card or aty least have used one in the last year.", value=True)
            debit_cards = st.checkbox("I have a credit card or aty least have used one in the last year.", value=True)

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
                    "saved": [float(borrowed)],
                    "receive_wages": [float(borrowed)],
                    "receive_transfers": [float(borrowed)],
                    "receive_pension": [float(borrowed)],
                    "pay_utilities": [float(borrowed)],
                    "anydigpayment": [float(borrowed)],
                    "mobileowner": [float(borrowed)],
                    "internetaccess": [float(borrowed)],
                    "debit_card": [float(borrowed)],
                    "credit_card": [float(borrowed)],
                    "paid_balance_regularly": [float(borrowed)]
                }
            )

            # df_temp = {
            #     "country_col": ,
            #     "country": countries_list
            # }


            option = {
                "backgroundColor": "#0E1117",
                "title": {
                    "text": "Top Parameters Dimensions - Logistic Regression Model"
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {
                        "type": "shadow"
                    }
                },

                "toolbox": {
                "feature": {
                    "dataZoom": {"yAxisIndex": 'none'},
                    "restore": {},
                    "saveAsImage": {}
                }
                },
                "dataZoom": [
                    {
                        "type": "slider",
                        "show": True,
                        "realtime": True,
                        "start": 0,
                        "end": 100,
                        "orient": "vertical",
                        "bottom": 20            
                    },
                    {
                        "type": "inside",   
                        "realtime": True,
                        "start": 0,
                        "end": 100
                    }
                ],
                "grid": {
                    "top": 80,
                    "bottom": 30
                },
                "xAxis": {
                    "type": "value",
                    "position": "top",
                    "splitLine": {
                        "lineStyle": {
                            "type": "dashed"
                        }
                    }
                },
                "yAxis": {
                    "type": "category",
                    "axisLine": { "show": False },
                    "axisLabel": { "show": False },
                    "axisTick": { "show": False },
                    "splitLine": { "show": False },
                    "data": params_data["Feature"].tolist()
                },
                "series": [
                    {
                        "name": "Valor",
                        "type": "bar",
                        "stack": "Total",
                        "label": {
                            "show": True,
                            "formatter": "{b}",
                            "position": "right"
                        },
                        "data": [
                            {"value": v, "label": {"position": "right"} if v < 0 else {}} for v in params_data["Coefficient"]
                        ]
                    }
                ]
            }

            c1.write("#")

            with c1:

                st_echarts(options=option, theme="dark", height="600px", width="100%" )


col1, col2, col3 = st.columns([6, 2, 6])

col2.download_button("Technical Report", str(static_path / "relatorio.pdf"), "technical_report.pdf")