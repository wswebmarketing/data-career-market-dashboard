"""import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output

try:
    csv = "https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv"
    df = pd.read_csv(csv)
    '''columns = df.columns.to_list()
    print(f"{df.head(20)}\n")
    print(f"Colunas da base de dados: {columns}")'''

    # Mapeamento de colunas (ajuste conforme necessário)
    translations = {
        'work_year': 'ano_trabalho',
        'experience_level': 'nivel_experiencia',
        'employment_type': 'tipo_contratacao',
        'job_title': 'cargo',
        'salary': 'salario',
        'salary_currency': 'moeda_salario',
        'salary_in_usd': 'salario_usd',
        'company_location': 'local_empresa',
        'company_size': 'porte_empresa',
        'employee_residence': 'residencia_empregado',
        'remote_ratio': 'proporcao_remoto',
        'company': 'empresa'
    }

    # Renomeia apenas as colunas presentes no DataFrame
    existent_translations = {k: v for k, v in translations.items() if k in df.columns}
    df.rename(columns=existent_translations, inplace=True)

    #print(f"Colunas (traduzidas quando aplicável): {df.columns.to_list()}")
    #print(df.head(10))
    #print(df.columns.to_list())

    # Mapeamento de valores do nível de experiência
    exp_map = {
        'EN': 'Júnior',         # Entry
        'MI': 'Pleno',         # Mid
        'SE': 'Senior',        # Senior
        'EX': 'Executivo',     # Executive
        'JUNIOR': 'Júnior',
        'MID': 'Pleno',
        'SENIOR': 'Senior',
        'EXECUTIVE': 'Executivo'
    }

    # Identifica coluna (aplica tanto antes quanto depois da tradução de nomes)
    if 'nivel_experiencia' in df.columns:
        col = 'nivel_experiencia'
    elif 'experience_level' in df.columns:
        col = 'experience_level'
    else:
        col = None

    if col:
        df[col] = df[col].apply(lambda x: exp_map.get(str(x).strip().upper(), x))

    # Verificação rápida
    #print(df[col].value_counts())
    
    # Mapeamento de valores da coluna 'tipo_contratacao'
    contratacao_map = {
        'FT': 'Tempo Integral',
        'CT': 'Contrato',
        'PT': 'Meio Período',
        'FL': 'Freelancer'
    }

    if 'tipo_contratacao' in df.columns:
        df['tipo_contratacao'] = df['tipo_contratacao'].apply(lambda x: contratacao_map.get(str(x).strip().upper(), x))
    
    # Mapeamento de valores da coluna 'residencia_empregado' (códigos de países para português)
    residencia_map = {
        'US': 'Estados Unidos',
        'CA': 'Canadá',
        'GB': 'Reino Unido',
        'DE': 'Alemanha',
        'FR': 'França',
        'ES': 'Espanha',
        'IT': 'Itália',
        'NL': 'Países Baixos',
        'AU': 'Austrália',
        'BR': 'Brasil',
        'IN': 'Índia',
        'CN': 'China',
        'JP': 'Japão',
        'KR': 'Coreia do Sul',
        'RU': 'Rússia',
        'MX': 'México',
        'AR': 'Argentina',
        'CL': 'Chile',
        'CO': 'Colômbia',
        'PE': 'Peru',
        'PT': 'Portugal',
        'SE': 'Suécia',
        'NO': 'Noruega',
        'DK': 'Dinamarca',
        'FI': 'Finlândia',
        'PL': 'Polônia',
        'CZ': 'República Tcheca',
        'HU': 'Hungria',
        'TR': 'Turquia',
        'ZA': 'África do Sul',
        'EG': 'Egito',
        'NG': 'Nigéria',
        'KE': 'Quênia',
        'SG': 'Singapura',
        'MY': 'Malásia',
        'TH': 'Tailândia',
        'PH': 'Filipinas',
        'VN': 'Vietnã',
        'ID': 'Indonésia',
        'PK': 'Paquistão',
        'BD': 'Bangladesh',
        'UA': 'Ucrânia',
        'RO': 'Romênia',
        'BG': 'Bulgária',
        'HR': 'Croácia',
        'SI': 'Eslovênia',
        'SK': 'Eslováquia',
        'EE': 'Estônia',
        'LV': 'Letônia',
        'LT': 'Lituânia',
        'GR': 'Grécia',
        'IE': 'Irlanda',
        'BE': 'Bélgica',
        'AT': 'Áustria',
        'CH': 'Suíça',
        'LU': 'Luxemburgo',
        'MT': 'Malta',
        'CY': 'Chipre',
        'IS': 'Islândia',
        'NZ': 'Nova Zelândia',
        'HK': 'Hong Kong',
        'TW': 'Taiwan',
        'IL': 'Israel',
        'AE': 'Emirados Árabes Unidos',
        'SA': 'Arábia Saudita',
        'QA': 'Catar',
        'KW': 'Kuwait',
        'BH': 'Bahrein',
        'OM': 'Omã',
        'JO': 'Jordânia',
        'LB': 'Líbano',
        'IQ': 'Iraque',
        'IR': 'Irã',
        'SY': 'Síria',
        'YE': 'Iêmen',
        'AM': 'Armênia',
        'GE': 'Geórgia',
        'AZ': 'Azerbaijão',
        'KZ': 'Cazaquistão',
        'UZ': 'Uzbequistão',
        'TM': 'Turcomenistão',
        'TJ': 'Tajiquistão',
        'KG': 'Quirguistão',
        'MN': 'Mongólia',
        'NP': 'Nepal',
        'LK': 'Sri Lanka',
        'MM': 'Mianmar',
        'KH': 'Camboja',
        'LA': 'Laos',
        'BN': 'Brunei',
        'TL': 'Timor-Leste',
        'PG': 'Papua-Nova Guiné',
        'FJ': 'Fiji',
        'WS': 'Samoa',
        'TO': 'Tonga',
        'VU': 'Vanuatu',
        'SB': 'Ilhas Salomão',
        'KI': 'Kiribati',
        'TV': 'Tuvalu',
        'MH': 'Ilhas Marshall',
        'FM': 'Micronésia',
        'PW': 'Palau',
        'NR': 'Nauru',
        'TV': 'Tuvalu',
        'CK': 'Ilhas Cook',
        'NU': 'Niue',
        'AS': 'Samoa Americana',
        'GU': 'Guam',
        'MP': 'Ilhas Marianas do Norte',
        'PR': 'Porto Rico',
        'VI': 'Ilhas Virgens Americanas',
        'UM': 'Ilhas Menores Distantes dos Estados Unidos',
        'IO': 'Território Britânico do Oceano Índico',
        'SH': 'Santa Helena',
        'AC': 'Ilha de Ascensão',
        'TA': 'Tristão da Cunha',
        'GS': 'Geórgia do Sul e Ilhas Sandwich do Sul',
        'FK': 'Ilhas Falkland',
        'AQ': 'Antártida',
        'BV': 'Ilha Bouvet',
        'HM': 'Ilha Heard e Ilhas McDonald',
        'TF': 'Terras Austrais e Antárticas Francesas',
        'PF': 'Polinésia Francesa',
        'NC': 'Nova Caledônia',
        'WF': 'Wallis e Futuna',
        'TK': 'Tokelau',
        'CC': 'Ilhas Cocos',
        'CX': 'Ilha Christmas',
        'NF': 'Ilha Norfolk',
        'RE': 'Reunião',
        'YT': 'Mayotte',
        'GP': 'Guadalupe',
        'MQ': 'Martinica',
        'GF': 'Guiana Francesa',
        'PM': 'São Pedro e Miquelão',
        'BL': 'São Bartolomeu',
        'MF': 'São Martinho',
        'SX': 'Sint Maarten',
        'AW': 'Aruba',
        'CW': 'Curaçao',
        'BQ': 'Países Baixos Caribenhos',
        'SX': 'Sint Maarten',
        'TT': 'Trinidad e Tobago',
        'JM': 'Jamaica',
        'HT': 'Haiti',
        'DO': 'República Dominicana',
        'CU': 'Cuba',
        'BS': 'Bahamas',
        'BB': 'Barbados',
        'LC': 'Santa Lúcia',
        'VC': 'São Vicente e Granadinas',
        'GD': 'Granada',
        'AG': 'Antígua e Barbuda',
        'DM': 'Dominica',
        'KN': 'São Cristóvão e Névis',
        'MS': 'Montserrat',
        'VG': 'Ilhas Virgens Britânicas',
        'TC': 'Ilhas Turcas e Caicos',
        'KY': 'Ilhas Cayman',
        'BM': 'Bermudas',
        'GL': 'Groenlândia',
        'FO': 'Ilhas Faroé',
        'SJ': 'Svalbard e Jan Mayen',
        'AX': 'Ilhas Åland',
        'GG': 'Guernsey',
        'JE': 'Jersey',
        'IM': 'Ilha de Man',
        'GI': 'Gibraltar',
        'PT': 'Portugal',
        'AD': 'Andorra',
        'MC': 'Mônaco',
        'SM': 'San Marino',
        'VA': 'Cidade do Vaticano',
        'LI': 'Liechtenstein',
        'BY': 'Bielorrússia',
        'MD': 'Moldávia',
        'AL': 'Albânia',
        'MK': 'Macedônia do Norte',
        'ME': 'Montenegro',
        'RS': 'Sérvia',
        'BA': 'Bósnia e Herzegovina',
        'XK': 'Kosovo',
        'TN': 'Tunísia',
        'DZ': 'Argélia',
        'MA': 'Marrocos',
        'LY': 'Líbia',
        'SD': 'Sudão',
        'SS': 'Sudão do Sul',
        'ET': 'Etiópia',
        'SO': 'Somália',
        'DJ': 'Djibouti',
        'ER': 'Eritreia',
        'UG': 'Uganda',
        'RW': 'Ruanda',
        'BI': 'Burundi',
        'TZ': 'Tanzânia',
        'MZ': 'Moçambique',
        'ZW': 'Zimbábue',
        'BW': 'Botsuana',
        'NA': 'Namíbia',
        'ZM': 'Zâmbia',
        'MW': 'Malawi',
        'AO': 'Angola',
        'CD': 'República Democrática do Congo',
        'CG': 'República do Congo',
        'GA': 'Gabão',
        'CM': 'Camarões',
        'TD': 'Chade',
        'CF': 'República Centro-Africana',
        'GQ': 'Guiné Equatorial',
        'ST': 'São Tomé e Príncipe',
        'CV': 'Cabo Verde',
        'GW': 'Guiné-Bissau',
        'GN': 'Guiné',
        'SL': 'Serra Leoa',
        'LR': 'Libéria',
        'CI': 'Costa do Marfim',
        'GH': 'Gana',
        'TG': 'Togo',
        'BJ': 'Benin',
        'NE': 'Níger',
        'BF': 'Burkina Faso',
        'ML': 'Mali',
        'SN': 'Senegal',
        'GM': 'Gâmbia',
        'MR': 'Mauritânia',
        'EH': 'Saara Ocidental',
        'SZ': 'Essuatíni',
        'LS': 'Lesoto',
        'BT': 'Butão',
        'AF': 'Afeganistão',
        'TJ': 'Tajiquistão',
        'KG': 'Quirguistão',
        'UZ': 'Uzbequistão',
        'TM': 'Turcomenistão',
        'KZ': 'Cazaquistão',
        'MN': 'Mongólia',
        'KP': 'Coreia do Norte',
        'KR': 'Coreia do Sul',
        'JP': 'Japão',
        'CN': 'China',
        'TW': 'Taiwan',
        'HK': 'Hong Kong',
        'MO': 'Macau',
        'VN': 'Vietnã',
        'LA': 'Laos',
        'KH': 'Camboja',
        'TH': 'Tailândia',
        'MY': 'Malásia',
        'SG': 'Singapura',
        'ID': 'Indonésia',
        'PH': 'Filipinas',
        'BN': 'Brunei',
        'TL': 'Timor-Leste',
        'PG': 'Papua-Nova Guiné',
        'SB': 'Ilhas Salomão',
        'VU': 'Vanuatu',
        'NC': 'Nova Caledônia',
        'FJ': 'Fiji',
        'TO': 'Tonga',
        'WS': 'Samoa',
        'KI': 'Kiribati',
        'MH': 'Ilhas Marshall',
        'FM': 'Estados Federados da Micronésia',
        'PW': 'Palau',
        'NR': 'Nauru',
        'TV': 'Tuvalu',
        'CK': 'Ilhas Cook',
        'NU': 'Niue',
        'PF': 'Polinésia Francesa',
        'WF': 'Wallis e Futuna',
        'NC': 'Nova Caledônia',
        'TK': 'Tokelau',
        'AS': 'Samoa Americana',
        'GU': 'Guam',
        'MP': 'Ilhas Marianas do Norte',
        'PR': 'Porto Rico',
        'VI': 'Ilhas Virgens Americanas',
        'UM': 'Ilhas Menores Distantes dos Estados Unidos',
        'IO': 'Território Britânico do Oceano Índico',
        'SH': 'Santa Helena',
        'AC': 'Ilha de Ascensão',
        'TA': 'Tristão da Cunha',
        'GS': 'Geórgia do Sul e Ilhas Sandwich do Sul',
        'FK': 'Ilhas Falkland',
        'AQ': 'Antártida',
        'BV': 'Ilha Bouvet',
        'HM': 'Ilha Heard e Ilhas McDonald',
        'TF': 'Terras Austrais e Antárticas Francesas',
        'CC': 'Ilhas Cocos',
        'CX': 'Ilha Christmas',
        'NF': 'Ilha Norfolk',
        'RE': 'Reunião',
        'YT': 'Mayotte',
        'GP': 'Guadalupe',
        'MQ': 'Martinica',
        'GF': 'Guiana Francesa',
        'PM': 'São Pedro e Miquelão',
        'BL': 'São Bartolomeu',
        'MF': 'São Martinho',
        'SX': 'Sint Maarten',
        'AW': 'Aruba',
        'CW': 'Curaçao',
        'BQ': 'Países Baixos Caribenhos',
        'TT': 'Trinidad e Tobago',
        'JM': 'Jamaica',
        'HT': 'Haiti',
        'DO': 'República Dominicana',
        'CU': 'Cuba',
        'BS': 'Bahamas',
        'BB': 'Barbados',
        'LC': 'Santa Lúcia',
        'VC': 'São Vicente e Granadinas',
        'GD': 'Granada',
        'AG': 'Antígua e Barbuda',
        'DM': 'Dominica',
        'KN': 'São Cristóvão e Névis',
        'MS': 'Montserrat',
        'VG': 'Ilhas Virgens Britânicas',
        'TC': 'Ilhas Turcas e Caicos',
        'KY': 'Ilhas Cayman',
        'BM': 'Bermudas',
        'GL': 'Groenlândia',
        'FO': 'Ilhas Faroé',
        'SJ': 'Svalbard e Jan Mayen',
        'AX': 'Ilhas Åland',
        'GG': 'Guernsey',
        'JE': 'Jersey',
        'IM': 'Ilha de Man',
        'GI': 'Gibraltar',
        'AD': 'Andorra',
        'MC': 'Mônaco',
        'SM': 'San Marino',
        'VA': 'Cidade do Vaticano',
        'LI': 'Liechtenstein',
        'BY': 'Bielorrússia',
        'MD': 'Moldávia',
        'AL': 'Albânia',
        'MK': 'Macedônia do Norte',
        'ME': 'Montenegro',
        'RS': 'Sérvia',
        'BA': 'Bósnia e Herzegovina',
        'XK': 'Kosovo',
        'TN': 'Tunísia',
        'DZ': 'Argélia',
        'MA': 'Marrocos',
        'LY': 'Líbia',
        'SD': 'Sudão',
        'SS': 'Sudão do Sul',
        'ET': 'Etiópia',
        'SO': 'Somália',
        'DJ': 'Djibouti',
        'ER': 'Eritreia',
        'UG': 'Uganda',
        'RW': 'Ruanda',
        'BI': 'Burundi',
        'TZ': 'Tanzânia',
        'MZ': 'Moçambique',
        'ZW': 'Zimbábue',
        'BW': 'Botsuana',
        'NA': 'Namíbia',
        'ZM': 'Zâmbia',
        'MW': 'Malawi',
        'AO': 'Angola',
        'CD': 'República Democrática do Congo',
        'CG': 'República do Congo',
        'GA': 'Gabão',
        'CM': 'Camarões',
        'TD': 'Chade',
        'CF': 'República Centro-Africana',
        'GQ': 'Guiné Equatorial',
        'ST': 'São Tomé e Príncipe',
        'CV': 'Cabo Verde',
        'GW': 'Guiné-Bissau',
        'GN': 'Guiné',
        'SL': 'Serra Leoa',
        'LR': 'Libéria',
        'CI': 'Costa do Marfim',
        'GH': 'Gana',
        'TG': 'Togo',
        'BJ': 'Benin',
        'NE': 'Níger',
        'BF': 'Burkina Faso',
        'ML': 'Mali',
        'SN': 'Senegal',
        'GM': 'Gâmbia',
        'MR': 'Mauritânia',
        'EH': 'Saara Ocidental',
        'SZ': 'Essuatíni',
        'LS': 'Lesoto',
        'BT': 'Butão',
        'AF': 'Afeganistão'
    }

    if 'residencia_empregado' in df.columns:
        df['residencia_empregado'] = df['residencia_empregado'].apply(lambda x: residencia_map.get(str(x).strip().upper(), x))
    
    if 'local_empresa' in df.columns:
        df['local_empresa'] = df['local_empresa'].apply(lambda x: residencia_map.get(str(x).strip().upper(), x))
    
    # Mapeamento de valores da coluna 'porte_empresa'
    tamanho_map = {
        'M': 'Médio',
        'L': 'Pequeno',
        'S': 'Grande'
    }

    if 'porte_empresa' in df.columns:
        df['porte_empresa'] = df['porte_empresa'].apply(lambda x: tamanho_map.get(str(x).strip().upper(), x))
    
    # Tradução de valores da coluna 'cargo'
    job_keywords = {
        'data scientist': 'cientista de dados',
        'data engineer': 'engenheiro de dados',
        'data analyst': 'analista de dados',
        'machine learning engineer': 'engenheiro de machine learning',
        'machine learning': 'aprendizado de máquina',
        'ml engineer': 'engenheiro de ml',
        'software engineer': 'engenheiro de software',
        'backend engineer': 'engenheiro backend',
        'frontend engineer': 'engenheiro front-end',
        'front end engineer': 'engenheiro front-end',
        'full stack engineer': 'engenheiro full-stack',
        'devops engineer': 'engenheiro de devops',
        'data architect': 'arquiteto de dados',
        'research engineer': 'engenheiro de pesquisa',
        'research scientist': 'cientista de pesquisa',
        'product manager': 'gerente de produto',
        'manager': 'gerente',
        'director': 'diretor',
        'analyst': 'analista',
        'scientist': 'cientista',
        'consultant': 'consultor'
    }

    def translate_job_title(title):
        if pd.isna(title):
            return title
        s = str(title).lower()
        for k, v in job_keywords.items():
            s = s.replace(k, v)
        s = ' '.join(s.split())
        return s.title()

    if 'cargo' in df.columns:
        df['cargo'] = df['cargo'].apply(translate_job_title)
    
    print(df)
    print(f"{df.columns.to_list()}\n")
    print(df["porte_empresa"].unique())
    print(f"{df[df["ano_trabalho"].isnull()]}\n")

    df_new = df.dropna()
    df_new["ano_trabalho"] = df_new["ano_trabalho"].astype("int64")
    df_new["salario"] = df_new["salario"].astype("float64").round(2)
    df_new["salario_usd"] = df_new["salario_usd"].astype("float64").round(2)

    #print(df_new)
    df_new.to_csv("cargos-e-salarios-atualizados.csv", index = False)
    
except OSError as error:
    print("Erro ao importar a base de dados!".upper())
    print(f"Detalhes do erro: {error}".upper())"""

import dash
from dash import Dash, html, callback, Input, Output

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"

app = Dash(
    __name__, 
    use_pages = True, 
    suppress_callback_exceptions = True,
    external_stylesheets = [BS]
)

app.layout = html.Div([
    dash.page_container
])

if(__name__ == "__main__"):
    app.run(debug = True)