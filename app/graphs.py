# Utils Functions
import streamlit as st
from datetime import datetime
from streamlit_echarts import st_echarts
import numpy as np

class Graphs:
    """Utils functions"""

    def __init__(self):
        
        self.start = datetime(2000, 1, 1)
        self.end = datetime.today()

    @st.cache_resource(show_spinner=False)
    def echart_dict(_self, data):
        """Renders Java Script Graphics"""


        x_data = data["age"].tolist()
        y_data = [round(item, 3) for item in data["financial_worry"].tolist()]

        options = {
            "grid": {
                "left": "4%", 
                "right": "3.5%", 
            },
            "title": {
                "text": "Financial Worry Index Evolution By Age",
                "textStyle": {"color": "#FFFFFF"}
            },
            "backgroundColor": "#0E1117",
            "tooltip": {
                "trigger": 'axis',
                "axisPointer": {
                    "type": 'cross',
                    "animation": False,
                    "label": {
                        "backgroundColor": '#505765'
                    }
                },
                "formatter": "{c}"
            },
            "toolbox": {
                "feature": {
                    "dataZoom": {"yAxisIndex": 'none'},
                    "dataView": {"readOnly": True},
                    "restore": {},
                }
            },
            "dataZoom": [
                {"show": True, "realtime": True, "start": 0, "end": 100},
                {"type": 'inside', "realtime": True, "start": 0, "end": 100}
            ],
            "xAxis": {
                "name": "Age",
                "type": 'category',
                "data": x_data
            },
            "yAxis": [{
                "type": "value",
                "axisLabel": {"formatter": "{value}"},
            }],
            "series": [
                {
                    "type": "line",
                    "showSymbol": False,
                    "smooth": True,
                    "lineStyle": {
                        "color": "#fba725"
                    },
                    "data": y_data
                }
            ]
        }

        return options


    @st.cache_resource(show_spinner=False)
    def bar_chart_dict(_self, data, title, min_zoom: int = 0, 
                       label_format: str = "%"):
        """Renders Java Script Graphics"""

        x_data = data.index.strftime("%d/%m/%Y").tolist()
        y_data = [round(value, 3) for value in data[data.columns[1]].tolist()]

        if min_value == 0:
            min_value -= 5

        options = {
            "color": _self.config.base_color,
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "shadow"
                },
                "animation": False,
                    "label": {
                        "backgroundColor": '#505765'
                    },
                "formatter": f"{{c}}{label_format}"
            },
            "toolbox": {
                "feature": {
                    "dataZoom": {"yAxisIndex": 'none'},
                    "restore": {},
                    "saveAsImage": {}
                }
            },
            "dataZoom": [
                {"show": True, "realtime": True, "start": min_zoom, "end": 100},
                {"type": 'inside', "realtime": True, "start": min_zoom, "end": 100}
            ],
            "grid": {
                "left": "0%", 
                "right": "5%", 
                "containLabel": True
            },
            "title": {
                "text": title,
                "textStyle": {"color": "#FFFFFF"}
            },
            "backgroundColor": "#0E1117",
            "xAxis": [
                {
                    "type": "category",
                    "boundaryGap": True,
                    "data": x_data,
                    "axisTick": {
                        "alignWithLabel": True
                    }
                }
            ],
            "yAxis": [
                {
                    "type": "value",
                    "axisLabel": {"formatter": f"{{value}}{label_format}"}
                }
            ],
            "series": [
                {
                    "name": "",
                    "type": "bar",
                    "data": y_data[i],
                    "itemStyle": {
                        "barBorderRadius": [6, 6, 0, 0]
                    }
                }
                for i in range(len(y_data))
            ]
        }

        return options


    def correlation_heatmap(self, corr):
    
        mask = np.triu(np.ones_like(corr, dtype=bool))

        data = []
        columns = list(corr.columns)

        for i in range(len(columns)):
            for j in range(len(columns)):
                if not mask[i, j]:
                    data.append([j, i, round(corr.iloc[i, j], 2)])

        option = {
            "tooltip": {
                "position": "top"
            },
            "title": {
                "text": "Correlation Heatmap - Model Numerical Variables",
                "textStyle": {"color": "#FFFFFF"}
            },
            "backgroundColor": "#0E1117",
            "xAxis": {
                "type": "category",
                "data": columns,
                "splitArea": {"show": True},
                "axisLabel": {
                    "rotate": 90,
                    "interval": 0
                }
            },
            "yAxis": {
                "type": "category",
                "data": columns,
                "splitArea": {"show": True}
            },
            "visualMap": {
                "min": -1,
                "max": 1,
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": "15%",
                "inRange": {
                    "color": ["#3b4cc0", "#f7f7f7", "#b40426"]
                }
            },
            "series": [
                {
                    "name": "Correlação",
                    "type": "heatmap",
                    "data": data,
                    "label": {
                        "show": True,
                        "color": "black",
                        "fontSize": 10
                    },
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowColor": "rgba(0, 0, 0, 0.5)"
                        }
                    }
                }
            ]
        }

        return option
    

    def histogram(self, df, var):

        values = df["values"]

        if values.nunique() <= 10 or values.dtype == "object":
            freq = values.value_counts().sort_index()
            x_labels = freq.index.tolist()
            data = freq.tolist()
        else:
            counts, bin_edges = np.histogram(values, bins=20)
            x_labels = [f"{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}" for i in range(len(bin_edges)-1)]
            data = counts.tolist()

        option = {
            "color": "#fba725",
            "tooltip": {"trigger": "axis", 
                        "axisPointer": {
                            "type": "shadow"
                        },},
            "backgroundColor": "#0E1117",
            "toolbox": {
                "feature": {
                    "dataZoom": {"yAxisIndex": 'none'},
                    "restore": {},
                    "saveAsImage": {}
                }
            },
            "dataZoom": [
                {"show": True, "realtime": True, "start": 0, "end": 100},
                {"type": 'inside', "realtime": True, "start": 0, "end": 100}
            ],
            "grid": {
                "left": "0%", 
                "right": "5%", 
                "containLabel": True
            },
            "title": {
                "text": f"Histogram - {var}",
                "textStyle": {"color": "#FFFFFF"}
            },
            "xAxis": {
                "type": "category",
                "data": x_labels,
                "axisLabel": {"rotate": 45}
            },
            "yAxis": {"type": "value"},
            "series": [{
                "data": data,
                "type": "bar",
                "itemStyle": {
                        "barBorderRadius": [6, 6, 0, 0]
                    }
            }]
        }

        return option
    

    def pie_plot(self, df, var):

        freq = df["values"].value_counts().sort_index()
        labels = {0: "No", 1: "Yes"}

        if var == "Sex":
            labels = {0: "Male", 1: "Female"}

        pie_data = [{"value": int(freq[i]), "name": labels[i]} for i in freq.index]

        option = {
            "color": ["#FFFFFF", "#fba725"],
            "backgroundColor": "#0E1117",
            "tooltip": {"trigger": "item"},
            "legend": {
                "top": "5%",
                "left": "center"
            },
            "title": {
                "text": f"Distribution - {var}",
                "textStyle": {"color": "#FFFFFF"}
            },
            "legend": {
                "top": 60,
                "right": 40,
            },
            "series": [
                {
                    "name": var,
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "avoidLabelOverlap": False,
                    "itemStyle": {
                        "borderRadius": 10,
                        "borderColor": "#fff",
                        "borderWidth": 2
                    },
                    "label": {
                        "show": False,
                        "position": "center"
                    },
                    "emphasis": {
                        "label": {
                            "show": True,
                            "fontSize": 30,
                            "fontWeight": "bold"
                        }
                    },
                    "labelLine": {"show": False},
                    "data": pie_data
                }
            ]
        }

        return option


    def boxplot(self, df, var, title_var):

        source = [group["financial_worry"].tolist() for name, group in df.groupby(var)]

        option = {
            "color": "#fba725",
            "backgroundColor": "#0E1117",
            "toolbox": {
                "feature": {
                    "dataZoom": {"yAxisIndex": 'none'},
                    "restore": {},
                    "saveAsImage": {}
                }
            },
            "title": [
                {
                    "text": f"Box Plot - {title_var}",
                },
                {
                    "text": "LS: Q3 + 1.5 * IQR \nLI: Q1 - 1.5 * IQR",
                    "borderColor": "#999",
                    "borderWidth": 0.5,
                    "textStyle": {
                        "fontWeight": "normal",
                        "fontSize": 14,
                        "lineHeight": 20
                    },
                    "left": "40%",
                    "top": "90%"
                }
            ],
            "dataset": [
                {
                    "source": source
                },
                {
                    "transform": {
                        "type": "boxplot",
                        "config": {
                            "itemNameFormatter": "{value}"
                        }
                    }
                },
                {
                    "fromDatasetIndex": 1,
                    "fromTransformResult": 1
                }
            ],
            "tooltip": {
                "trigger": "item",
                "axisPointer": {
                    "type": "shadow"
                }
            },
            "grid": {
                "left": "10%",
                "right": "10%",
                "bottom": "15%"
            },
            "xAxis": {
                "type": "category",
                "boundaryGap": True,
                "nameGap": 30,
                "splitArea": {"show": False},
                "splitLine": {"show": False}
            },
            "yAxis": {
                "type": "value",
                "name": "Financial Worry Index",
                "splitArea": {"show": True}
            },
            "series": [
                {
                    "name": "boxplot",
                    "type": "boxplot",
                    "datasetIndex": 1,
                    "itemStyle": {
                        "color": "#3E4144",
                        "borderColor": "#fba725"
                    }
                },
                {
                    "name": "outlier",
                    "type": "scatter",
                    "datasetIndex": 2
                }
            ]
        }

        return option
    

    def scatter_plot(self, df):

        df = df[["inc_q", "financial_worry"]].fillna(0)
        
        data = [[int(df["inc_q"].iloc[i]), 
                 int(df["financial_worry"].iloc[i])] for i in range(len(df))]

        option = {
            "color": "#fba725",
            "tooltip": {"trigger": "axis", 
                        "axisPointer": {
                            "type": "shadow"
                        },},
            "backgroundColor": "#0E1117",
            "toolbox": {
                "feature": {
                    "dataZoom": {"yAxisIndex": 'none'},
                    "restore": {},
                    "saveAsImage": {}
                }
            },
            "dataZoom": [
                {"show": True, "realtime": True, "start": 0, "end": 100},
                {"type": 'inside', "realtime": True, "start": 0, "end": 100}
            ],
            "grid": {
                "left": "0%", 
                "right": "5%", 
                "containLabel": True
            },
            "title": {
                "text": f"ScatterPlot - Age x Financial Worry Index",
                "textStyle": {"color": "#FFFFFF"}
            },
            "xAxis": {},
            "yAxis": {},
            "series": [
                {
                    "symbolSize": 20,
                    "data": data,
                    "type": "scatter"
                }
            ]
        }

        return option
    
    
    def h_bar_plot(self, params_data):

        option = {
            "backgroundColor": "#0E1117",
            "title": {
                "text": "Top Parameters - Logit Model"
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

        return option