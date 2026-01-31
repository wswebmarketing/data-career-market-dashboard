import streamlit as st
import pandas as pd
import plotly.express as px

try:
    # Define a configuração da página em título, ícone e layout
    st.set_page_config(
        page_title = "Dashboard de Salários na Área de Dados",
        page_icon = ":bar_chart:",
        layout = "wide"
    )

    #Carregamento da base de dados via Pandas
    csv = "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
    df = pd.read_csv(csv)

    #Exibição do nome das colunas da tabela - UTILIZAÇÃO APENAS PARA DESENVOLVIMENTO (DEBUG)
    #columns = df.shape[1]
    #print(f"Nome das colunas da tabela: {df.columns.tolist()}\n")

    #Título da sidebar (barra lateral)
    st.sidebar.header("Filtros")

    #Filtragem por ano
    years = sorted(df["ano"].unique())
    #print(f"Anos disponíveis na base de dados: {years}")
    selected_year = st.sidebar.multiselect(
        "Ano",
        years
    )
    #print(f"Ano selecionado: {selected_year}")

    #Filtragem por Nível de Experiência
    experience_levels = sorted(df["senioridade"].unique())
    #print(f"Níveis de experiência disponíveis na base de dados: {experience_levels}\n")
    selected_level_experience = st.sidebar.multiselect(
        "Nível de Experiência",
        experience_levels
    )
    #print(f"Nível de experiência selecionado: {selected_level_experience}\n")

    #Filtragem por Tipo de Contrato
    contract_types = sorted(df["contrato"].unique())
    #print(f"Tipos de contrato disponíveis: {contract_types}\n")
    selected_contract_type = st.sidebar.multiselect(
        "Tipo de Contrato",
        contract_types
    )
    #print(f"Tipo de contrato selecionado: {selected_contract_type}")

    #Filtragem por Tamanho da Empresa
    company_size = sorted(df["tamanho_empresa"].unique())
    #print(f"Porte das empresas disponiveis: {company_size}\n")
    selected_company_size = st.sidebar.multiselect(
        "Porte da Empresa",
        company_size
    )
    #print(f"Porte da empresa selecionado: {selected_company_size}")

    #Criação do dataframe com os dados filtrados
    df_filtered = df[
        (df["ano"].isin(selected_year)) &
        (df["senioridade"].isin(selected_level_experience)) &
        (df["contrato"].isin(selected_contract_type)) &
        (df["tamanho_empresa"].isin(selected_company_size))
    ]
    
    #Textos principais do Dashboard
    st.title("Dashboard de Análise de Salários na Área de Dados")
    st.markdown("Explore os dados salariais na área de dados dos últimos anos com filtros interativos. Utilize os filtros à esquerda.")

    #Principais KPIs
    st.subheader("Métricas gerais (Salário Anual em USD)")

    #verificação se o dataframe filtrado não está vazio
    if not df_filtered.empty:
        avg_salary = df_filtered["usd"].mean()
        #print(f"Média Salarial: ${avg_salary:.2f}")
        max_salary = df_filtered["usd"].max()
        #print(f"Maior Salário: ${max_salary:.2f}")
        total_records = df_filtered.shape[0]
        #print(f"Número total de registros: {total_records}")
        mode_position = df_filtered["cargo"].mode()[0]
        #print(f"Cargo mais frequente: {mode_position}")
    else:
        avg_salary = 0
        max_salary = 0 
        total_records = 0 
        mode_position = ""
        #print("Dataframe vazio!".upper())
    
    #Exibição dos KPIs no Dashboard em 4 colunas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Salário Médio: ", f"${avg_salary:,.2f}")
    col2.metric("Maior Salário: ", f"${max_salary:,.2f}")
    col3.metric("Total de Registros: ", f"{total_records}")
    col4.metric("Cargo mais frequente: ", f"{mode_position}")

    #Criação dos gráficos
    st.subheader("Gráficos")

    #Criação do gráfico de barras para exibição dos maiores salários médios por cargo
    #criação de duas colunas
    col1, col2 = st.columns(2)
    with col1:
        if not df_filtered.empty:
            df_top_positions = df_filtered.groupby("cargo")["usd"].mean().round(2).nlargest(10).sort_values(ascending = True).reset_index()
            graph_top_positions = px.bar(
                df_top_positions,
                x = "usd",
                y = "cargo",
                title = "Top 10 cargos por salário médio",
                labels = {"usd": "Salário Médio (USD)", "cargo": "Cargo"}
            )
            graph_top_positions.update_layout(title_x = 0.2, yaxis = {"categoryorder": "total ascending"})
            st.plotly_chart(graph_top_positions, use_container_width = True)
        else:
            st.warning("Não há dados a serem exibidos para este gráfico!".upper())

    with col2:
        if not df_filtered.empty:
            graph_salaries_by_year = px.histogram(
                df_filtered,
                x = "usd",
                nbins = 30,
                title = "Distribuição Salarial Anual",
                labels = {"usd": "Faixa Salarial (USD)", "count": ""}
            )
            graph_salaries_by_year.update_layout(title_x = 0.2)
            st.plotly_chart(graph_salaries_by_year, use_container_width = True)
        else:
            st.warning("Não há dados a serem exibidos para este gráfico!".upper())
    
    #criação das colunas 3 e 4 na linha seguinte para abrigar mais dois gráficos
    col3, col4 = st.columns(2)
    with col3:
        if not df_filtered.empty:
            count_remote_work = df_filtered["remoto"].value_counts().reset_index()
            count_remote_work.columns = ["modalidade", "quantidade"]
            graph_remote_work = px.pie(
                count_remote_work,
                names = "modalidade",
                values = "quantidade",
                title = "Proporção dos tipos de trabalho",
                hole = 0.5
            )
            graph_remote_work.update_traces(textinfo = "percent+label")
            graph_remote_work.update_layout(title_x = 0.2)
            st.plotly_chart(graph_remote_work, use_container_width = True)
        else:
            st.warning("Não há dados a serem exibidos para este gráfico!".upper())
    
    with col4:
        if not df_filtered.empty:
            df_filtered_by_data_scientist = df_filtered[df_filtered["cargo"] == "Data Scientist"]
            #print(f"{df_filtered_by_data_scientist}\n")
            avg_salary_data_scientist_by_countries = df_filtered_by_data_scientist.groupby("residencia_iso3")["usd"].mean().round(2).reset_index()
            #print(f"Média salarial de Cientistas de Dados por país:\n {avg_salary_data_scientist_by_countries}")
            graph_data_scientist_by_countries = px.choropleth(
                avg_salary_data_scientist_by_countries,
                locations = "residencia_iso3",
                color = "usd",
                color_continuous_scale = "rdylgn",
                title = "Média Salarial de Cientistas de Dados por País",
                labels = {"usd": "Salário Médio (USD)", "residencia_iso3": "País"}
            )
            graph_data_scientist_by_countries.update_layout(title_x = 0.2)
            st.plotly_chart(graph_data_scientist_by_countries, use_container_width = True)
        else:
            st.warning("Não há dados a serem exibidos para este gráfico!".upper())
    
    #Exibição da tabela
    st.subheader("Dados detalhados:")
    st.dataframe(df_filtered)

except OSError as error:
    print("Erro ao importar base de dados!\n".upper())
    print(f"Detalhes: {error}".upper())