import pandas as pd
import dash
from dash import html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from services.data_loader import load_positions_and_salaries
import plotly.express as px
import numpy as np
from tabulate import tabulate

try:
    df = load_positions_and_salaries()
except OSError as error:
    print("Erro ao importar a base de dados!")
    print(f"Erro: {error}")

#Ano
years = df["ano_trabalho"].sort_values().unique()
years_options = [
    {"label": year, "value": year} 
    for year in years
]

#Nível de Experiência
level_experience_options = [
    {"label": level, "value": level}
    for level in df["nivel_experiencia"].unique()
]

#Cargo
positions_options = [
    {"label": position, "value": position}
    for position in df["cargo"].unique()
]

#Tipo de Contratação
type_contract_options = [
    {"label": contract, "value": contract}
    for contract in df["tipo_contratacao"].unique()
]

#Tipo de trabalho (remoto)
remote_map = {
    0: "Presencial",
    50: "Híbrido",
    100: "Remoto"
}

df["modelo_trabalho"] = (
    df["proporcao_remoto"]
    .map(remote_map)
    .fillna("Não informado")
)

remote_options = [
    {"label": value, "value": value}
    for value in df["modelo_trabalho"].unique()
]

#Porte da Empresa
companies_options = [
    {"label": company, "value": company}
    for company in df["porte_empresa"].sort_values(ascending = False).unique()
]

#Residência do Empregado
residence_employee_options = [
    {"label": residence, "value": residence}
    for residence in df["residencia_empregado"].unique()
]

#Local da Empresa
company_place_options = [
    {"label": place, "value": place}
    for place in df["local_empresa"].unique()
]

#Cálculo da média salarial
print(f"{list(df.columns)}\n")
#avg_salaries = df["salario_usd"].mean().round(2)

#Cálculo da mediana salarial
#median_salaries = df["salario_usd"].round(2).median()

#Cálculo do desvio padrão
#stdev_salaries = df["salario_usd"].round(2).std()

#Cálculo do total de registros
#total = len(df)

#Cálculo do maior salário
#max_salary = df["salario_usd"].round(2).max()

#Cálculo do menor salário
#min_salary = df["salario_usd"].round(2).min()

#Registro da página Home
dash.register_page(
    __name__, 
    path="/", 
    title = "Dashboard de cargos e salários na área de dados"
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className = "sidebar p-5",
                        children = [
                            html.H2(
                                "Ano", 
                                className = "text-center text-white"
                            ),
                            dbc.Checklist(
                                id = "select_years",
                                className = "text-white",
                                options = years_options,
                                value = [],
                                inline = True
                            ),
                            html.H2(
                                "Nível de Experiência", 
                                className = "text-center text-white mt-5"
                            ),
                            dbc.Select(
                                id = "select_level_experience",
                                options = level_experience_options,
                                value = None,
                                placeholder = "" 
                            ),
                            html.H2(
                                "Cargo",
                                className = "text-center text-white mt-5"
                            ),
                            dbc.Select(
                                id = "select_position",
                                options = positions_options,
                                value = None,
                                placeholder = ""
                            ),
                            html.H2(
                                "Tipo de Contratação",
                                className = "text-center text-white mt-5"
                            ),
                            dbc.Checklist(
                                id = "select_type_contract",
                                options = type_contract_options,
                                value = [],
                                className = "text-white",
                            ),
                            html.H2(
                                "Tipo de trabalho",
                                className = "text-center text-white mt-5"
                            ),
                            dbc.Select(
                                id = "select_type_work",
                                options = remote_options,
                                value = None,
                                placeholder = ""
                            ),
                            html.H2(
                                "Porte da Empresa",
                                className = "text-center text-white mt-5"
                            ),
                            dbc.Checklist(
                                id = "select_type_company",
                                className = "text-white",
                                options = companies_options,
                                value = [],
                                inline = True
                            ),
                            html.H2(
                                "Residência do Empregado",
                                className = "text-center text-white mt-5"
                            ),
                            dbc.Select(
                                id = "select_residence_employee",
                                options = residence_employee_options,
                                value = None,
                                placeholder = ""
                            ),
                            html.H2(
                                "Local da Empresa",
                                className = "text-center text-white mt-5"
                            ),
                            dbc.Select(
                                id = "select_company_place",
                                options = company_place_options,
                                value = None,
                                placeholder = ""
                            )
                        ]
                    ),
                    width = 3,
                ),
                dbc.Col(
                    html.Div(
                        className = "graphs p-5 container",
                        children = [
                            dbc.Row(
                                className = "m-3",
                                children = [
                                    dbc.Col(
                                        width = 4,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-2",
                                                children = [
                                                    html.H3(
                                                        "Média Salarial",
                                                    ),
                                                    html.Span(
                                                        id = "kpi_average",
                                                        className = "text-bold"
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    dbc.Col(
                                        width = 4,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-2",
                                                children = [
                                                    html.H3(
                                                        "Mediana",
                                                    ),
                                                    html.Span(
                                                        id = "kpi_median",
                                                        className = "text-bold"
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                        width = 4,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-2",
                                                children = [
                                                    html.H3(
                                                        "Desvio padrão",
                                                    ),
                                                    html.Span(
                                                        id = "kpi_stdev",
                                                        className = "text-bold"
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            dbc.Row(
                                className = "m-3",
                                children = [
                                    dbc.Col(
                                        width = 4,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-2",
                                                children = [
                                                    html.H3(
                                                        "Total de Registros",
                                                    ),
                                                    html.Span(
                                                        id = "kpi_total",
                                                        className = "text-bold"
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    dbc.Col(
                                        width = 4,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-2",
                                                children = [
                                                    html.H3(
                                                        "Maior Salário",
                                                    ),
                                                    html.Span(
                                                        id = "kpi_max",
                                                        className = "text-bold"
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    dbc.Col(
                                        width = 4,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-2",
                                                children = [
                                                    html.H3(
                                                        "Menor Salário",
                                                    ),
                                                    html.Span(
                                                        id = "kpi_min",
                                                        className = "text-bold"
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            dbc.Row(
                                className = "p-5",
                                children = [
                                    dbc.Col(
                                        width = 6,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-3",
                                                children = [
                                                    html.H3(
                                                        "Gráfico dos 10 maiores salários por país",
                                                    ),
                                                    dcc.Graph(
                                                        id = "graph_top_10_salaries_by_country",
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                        width = 6,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-3",
                                                children = [
                                                    html.H3(
                                                        "Tabela dos 10 países que pagam os maiores salários",
                                                    ),
                                                    dash_table.DataTable(
                                                        id = "table_10_countries_pay_max_salaries",
                                                        columns = [
                                                            {"name": "País", "id": "residencia_empregado"},
                                                            {"name": "Média Salarial (USD)", "id": "average"},
                                                            {"name": "Mediana Salarial (USD)", "id": "median"},
                                                            {"name": "Total de Registros", "id": "total"}                                                            
                                                        ],
                                                        style_table = {
                                                            "overflowX": "auto",
                                                            "width": "100%"
                                                        },
                                                        style_cell = {
                                                            "textAlign": "center",
                                                            "padding": "8px",
                                                            "fontFamily": "inherit",
                                                            "fontSize": "14px"
                                                        },
                                                        style_header = {
                                                            "backgroundColor": "white",
                                                            "color": "black",
                                                            "fontWeight": "bold",
                                                            "textAlign": "center"
                                                        },
                                                        style_data = {
                                                            "backgroundColor": "white",
                                                            "color": "black"
                                                        },
                                                        style_as_list_view = True
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dbc.Row(
                                className = "p-5",
                                children = [
                                    dbc.Col(
                                        width = 6,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-3",
                                                children = [
                                                    html.H3(
                                                        "Média salarial por Nível de Experiência"
                                                    ),
                                                    dcc.Graph(
                                                        id = "graph_salaries_by_level_experience",
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                        width = 6,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-3",
                                                children = [
                                                    html.H3(
                                                        "Média Salarial por Tipo de Contratação"
                                                    ),
                                                    dcc.Graph(
                                                        id = "graph_salaries_by_type_contract"
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            dbc.Row(
                                className = "p-5",
                                children = [
                                    dbc.Col(
                                        width = 12,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-3",
                                                children = [
                                                    html.H3(
                                                        "Média Salarial por Porte da Empresa"
                                                    ),
                                                    dcc.Graph(
                                                        id = "graph_salaries_by_company_type"
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dbc.Row(
                                className = "p-5",
                                children = [
                                    dbc.Col(
                                        width = 6,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-3",
                                                children = [
                                                    html.H3(
                                                        "Percentual de trabalhadores por tipo de contratação"
                                                    ),
                                                    dcc.Graph(
                                                        id = "graph_percentual_workers_by_type_contract"
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                        width = 6,
                                        children = [
                                            dbc.Card(
                                                className = "text-center p-3",
                                                children = [
                                                    html.H3(
                                                        "Evolução Salarial Anual"
                                                    ),
                                                    dcc.Graph(
                                                        id = "graph_evolution_salaries_by_year"
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width = 9
                )
            ], 
            className = "g-0"
        )
    ]
)

#Função central de Filtragem
def apply_filters(
    df,
    years,
    level_experience,
    position,
    contracts,
    work_type,
    company_size,
    residence,
    company_place
):
    """
    Função responsável por aplicar todos os filtros da sidebar
    sobre o DataFrame original.

    Essa função representa a camada de lógica de negócio do dashboard.
    Ela recebe os estados da interface (inputs) e devolve
    um DataFrame filtrado pronto para análise e visualização.
    """

    # Trabalhamos sempre com cópia para evitar modificar o df original
    df_filtered = df.copy()

    #Filtro por ano (múltipla escolha)
    if(years):
        df_filtered = df_filtered[
            df_filtered["ano_trabalho"].isin(years)
        ]
    
    #Filtro por Nível de Experiência (Único)
    if(level_experience):
        df_filtered = df_filtered[
            df_filtered["nivel_experiencia"] == level_experience
        ]

    #Filtro por cargo (Único)
    if(position):
        df_filtered = df_filtered[
            df_filtered["cargo"] == position
        ]

    #Filtro por tipo de contratação (Múltipla Escolha)
    if(contracts):
        df_filtered = df_filtered[
            df_filtered["tipo_contratacao"].isin(contracts)
        ]

    #Filtro por Tipo de Trabalho (Único)
    if(work_type):
        df_filtered = df_filtered[
            df_filtered["modelo_trabalho"] == work_type
        ]

    #Filtro por Porte da Empresa (Múltipla Escolha)
    if(company_size):
        df_filtered = df_filtered[
            df_filtered["porte_empresa"].isin(company_size)
        ]

    #Filtro por Residência do Empregado (Único)
    if(residence):
        df_filtered = df_filtered[
            df_filtered["residencia_empregado"] == residence
        ]

    #Filtro por Local da Empresa (Único)
    if(company_place):
        df_filtered = df_filtered[
            df_filtered["local_empresa"] == company_place
        ]
    return df_filtered 

@callback(
    #Outputs
    [
        #KPIS
        Output("kpi_average", "children"),
        Output("kpi_median", "children"),
        Output("kpi_stdev", "children"),
        Output("kpi_total", "children"),
        Output("kpi_max", "children"),
        Output("kpi_min", "children"),

        #Gráficos
        Output("graph_top_10_salaries_by_country", "figure"),
        Output("graph_salaries_by_level_experience", "figure"),
        Output("graph_salaries_by_type_contract", "figure"),
        Output("graph_salaries_by_company_type", "figure"),
        Output("graph_percentual_workers_by_type_contract", "figure"),
        Output("graph_evolution_salaries_by_year", "figure"),

        #Tabela
        Output("table_10_countries_pay_max_salaries", "data")
    ],
    #Inputs
    [
        Input("select_years", "value"),
        Input("select_level_experience", "value"),
        Input("select_position", "value"),
        Input("select_type_contract", "value"),
        Input("select_type_work", "value"),
        Input("select_type_company", "value"),
        Input("select_residence_employee", "value"),
        Input("select_company_place", "value")
    ]
)

def update_kpis(
    years,
    level_experience,
    position,
    contracts,
    work_type,
    company_size,
    residence,
    company_place
):
    df_filtered = apply_filters(
        df,
        years,
        level_experience,
        position,
        contracts,
        work_type,
        company_size,
        residence,
        company_place
    )

    if(df_filtered.empty):
        empty_fig = px.bar(title = "Nenhum dado encontrado!")
        return (
            "-", "-", "-", "0", "-", "-",
            empty_fig,
            empty_fig,
            empty_fig,
            []
        )
    
    average = round(df_filtered["salario_usd"].mean(), 2)
    median = round(df_filtered["salario_usd"].median(), 2)
    stdev = round(df_filtered["salario_usd"].std(), 2)
    total = len(df_filtered)
    max_salary = round(df_filtered["salario_usd"].max(), 2)
    min_salary = round(df_filtered["salario_usd"].min(), 2)

    df_top10 = (
        df_filtered
        .groupby("residencia_empregado")
        .agg(
            average = ("salario_usd", "mean"),
            median = ("salario_usd", "median"),
            total = ("salario_usd", "count")
        )
        .reset_index()
        .sort_values(by = "average", ascending = False)
        .head(10)
    )

    df_top10_transformed_long = df_top10.melt(
        id_vars = ["residencia_empregado", "total"],
        value_vars = ["average", "median"],
        var_name = "metric",
        value_name = "salary"
    )
    df_top10_transformed_long["metric"] = df_top10_transformed_long["metric"].replace({
        "average": "Média",
        "median": "Mediana"
    })

    fig_top10 = px.bar(
        df_top10_transformed_long,
        x = "residencia_empregado",
        y = "salary",
        title = "Top 10 Países por Média Salarial (USD)",
        labels = {
            "residencia_empregado": "País",
            "salary": "Salário (USD)",
            "metric": "Métrica"
        },
        barmode = "group",
        color = "metric",
        template = "plotly"
    )
    fig_top10.update_layout(xaxis_tickangle = -45)

    df_top10["average"] = round(df_top10["average"], 2)
    df_top10["median"] = round(df_top10["median"], 2)
    table_data = df_top10.to_dict("records")

    df_experience = (
        df_filtered
        .groupby("nivel_experiencia")
        .agg(
            average_salary = ("salario_usd", "mean"),
            median_salary = ("salario_usd", "median"),
            total = ("salario_usd", "count")
        )
        .reset_index()
    )
    order = ["Júnior", "Pleno", "Senior", "Executivo"]
    df_experience["nivel_experiencia"] = pd.Categorical(
        df_experience["nivel_experiencia"],
        categories = order,
        ordered = True
    )
    df_experience = df_experience.sort_values("nivel_experiencia")
    df_experience_transformed_long = df_experience.melt(
        id_vars = "nivel_experiencia",
        value_vars = ["average_salary", "median_salary"],
        var_name = "metric",
        value_name = "salary"
    )
    df_experience_transformed_long["metric"] = df_experience_transformed_long["metric"].replace({
        "average_salary": "Média",
        "median_salary": "Mediana"
    })
    fig_experience = px.bar(
        df_experience_transformed_long,
        x = "nivel_experiencia",
        y = "salary",
        color = "metric",
        barmode = "group",
        labels = {
            "nivel_experiencia": "Nível de Experiência",
            "salary": "Salário (USD)",
            "metric": "Métrica"
        },
        template = "plotly",
    )
    fig_experience.update_traces(
        textposition = "outside"
    )

    df_contract = (
        df_filtered
        .groupby("tipo_contratacao")
        .agg(
            average_salary = ("salario_usd", "mean"),
            median_salary = ("salario_usd", "median"),
            total = ("salario_usd", "count")
        )
        .reset_index()
        .sort_values(by = "average_salary", ascending = False)
    )
    df_contract_transformed_long = df_contract.melt(
        id_vars = "tipo_contratacao",
        value_vars = ["average_salary", "median_salary"],
        var_name = "metric",
        value_name = "salary",
    )
    df_contract_transformed_long["metric"] = df_contract_transformed_long["metric"].replace({
        "average_salary": "Média",
        "median_salary": "Mediana"
    })
    
    fig_contract = px.bar(
        df_contract_transformed_long,
        x = "tipo_contratacao",
        y = "salary",
        color = "metric",
        barmode = "group",
        labels = {
            "tipo_contratacao": "Tipo de Contratação",
            "salary": "Salário (USD)",
            "metric": "Métrica"
        },
        template = "plotly"
    )
    fig_contract.update_traces(
        textposition = "outside"
    )

    df_company_size = (
        df_filtered
        .groupby("porte_empresa")
        .agg(
            average_salary = ("salario_usd", "mean"),
            median_salary = ("salario_usd", "median"),
            total = ("salario_usd", "count")
        )
        .reset_index()
        .sort_values(by = "average_salary", ascending = False)
    )
    df_company_size_transformed_long = df_company_size.melt(
        id_vars = "porte_empresa",
        value_vars = ["average_salary", "median_salary"],
        var_name = "metric",
        value_name = "salary"
    )
    df_company_size_transformed_long["metric"] = df_company_size_transformed_long["metric"].replace({
        "average_salary": "Média",
        "median_salary": "Mediana"
    })
    
    fig_company_size = px.bar(
        df_company_size_transformed_long,
        x = "porte_empresa",
        y = "salary",
        color = "metric",
        barmode = "group",
        labels = {
            "porte_empresa": "Porte da Empresa",
            "average_salary": "Média Salarial (USD)",
            "metric": "Métrica"
        },
        template = "plotly"
    )
    fig_company_size.update_traces(textposition = "outside")

    df_remote = (
        df_filtered
        .groupby("modelo_trabalho")
        .agg(
            total = ("salario_usd", "count")
        )
        .reset_index()
    )
    df_remote["percentual"] = (
        (df_remote["total"] / df_remote["total"].sum()) * 100
    )

    fig_remote = px.pie(
        df_remote,
        names = "modelo_trabalho",
        values = "total",
        hole = 0.5,
        template = "plotly"
    )
    fig_remote.update_traces(textinfo = "percent+label")

    df_evolution = (
        df_filtered
        .groupby("ano_trabalho")
        .agg(
            average_salary = ("salario_usd", "mean"),
            median_salary = ("salario_usd", "median"),
            total = ("salario_usd", "count")
        )
        .reset_index()
        .sort_values("ano_trabalho")
    )
    df_evolution_transformed_long = df_evolution.melt(
        id_vars = "ano_trabalho",
        value_vars = ["average_salary", "median_salary"],
        var_name = "metric",
        value_name = "salary"
    )
    df_evolution_transformed_long["metric"] = df_evolution_transformed_long["metric"].replace({
        "average_salary": "Média",
        "median_salary": "Mediana",
        "metric": "Métrica"
    })

    fig_evolution = px.line(
        df_evolution_transformed_long,
        x = "ano_trabalho",
        y = "salary",
        color = "metric",
        markers = True,
        template = "plotly",
        labels = {
            "ano_trabalho": "Ano",
            "average_salary": "Média Salarial (USD)",
            "metric": "Métrica"
        }
    )

    return(
        f"{average:.2f}\n",
        f"{median:.2f}\n",
        f"{stdev:.2f}\n",
        f"{total}\n",
        f"{max_salary:.2f}\n",
        f"{min_salary:.2f}\n",
        fig_top10,
        fig_experience,
        fig_contract,
        fig_company_size,
        fig_remote,
        fig_evolution,
        table_data
    )