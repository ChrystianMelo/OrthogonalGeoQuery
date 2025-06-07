import pandas as pd
import os
import time
import osmnx as ox
import matplotlib.pyplot as plt

# Colunas para criar o endereço formatado
COL_TIPO_LOGRADOURO = 'DESC_LOGRADOURO'
COL_NOME_LOGRADOURO = 'NOME_LOGRADOURO'
COL_NUM_LOGRADOURO = 'NUMERO_IMOVEL'
COL_BAIRRO = 'NOME_BAIRRO'

# Colunas para manter no arquivo final
COL_ID_ATIV_ECON = 'ID_ATIV_ECON_ESTABELECIMENTO'
COL_DATA_INICIO = 'DATA_INICIO_ATIVIDADE'
COL_IND_ALVARA = 'IND_POSSUI_ALVARA'
COL_NOME_FANTASIA = 'NOME_FANTASIA'
COL_GEOMETRIA = 'GEOMETRIA'

# Coluna usada para ser usada na falta de NOME_FANTASIA
COL_NOME = 'NOME' 

COL_CNAE_CODIGO = 'CNAE' 

# Prefixo do código CNAE a ser filtrado
CNAE_CODE_PREFIX_TO_FILTER = '56112'

# Lista final de colunas para o arquivo de saída
FINAL_OUTPUT_COLUMNS_REQUESTED_BY_USER = [
    COL_ID_ATIV_ECON,
    COL_DATA_INICIO,
    COL_IND_ALVARA,
    'ENDERECO', # Criada concatenando as colunas de endereço na função format_address
    COL_NOME,
    'LATITUDE',
    'LONGITUDE'
]

def format_address(row):
    """
    Formata o endereço de saída baseada nas colunas
    """
    try:
        tipo_log = str(row.get(COL_TIPO_LOGRADOURO, '')).strip()
        nome_log = str(row.get(COL_NOME_LOGRADOURO, '')).strip()

        numero = str(row.get(COL_NUM_LOGRADOURO, '')).strip().replace('.0', '') 
        bairro = str(row.get(COL_BAIRRO, '')).strip()

        # Constrói a parte principal do endereço
        address_parts = []
        # Formata AVE para AVENIDA
        if tipo_log.upper() == 'AVE': tipo_log = 'AVENIDA'
        if tipo_log.upper() == 'ROD': tipo_log = 'RODOVIA'
        if tipo_log.upper() == 'PCA': tipo_log = 'PRACA'
        if tipo_log and nome_log:
            address_parts.append(f"{tipo_log} {nome_log}")
        elif nome_log:
            address_parts.append(nome_log)
        elif tipo_log: 
             address_parts.append(tipo_log)

        if numero and numero.upper() != 'NAN' and numero.upper() != 'NA': 
            address_parts.append(numero)
        
        if bairro and pd.notna(bairro) and bairro.upper() != 'NAN' and bairro.upper() != 'NA':
            address_parts.append(f"{bairro}")
        
        address_parts.append(f"Belo Horizonte - MG")
        full_address = ", ".join(filter(None, address_parts))
        return full_address
    except Exception as e:
        print(f"Erro ao formatar endereço para a linha: {row.name} - {e}")
        return ""

def main(INPUT_CSV_FILE, OUTPUT_CSV_FILE):
    # Verifica se o arquivo de entrada existe no diretório
    if not os.path.exists(INPUT_CSV_FILE):
        print(f"Erro: Arquivo de entrada '{INPUT_CSV_FILE}' não encontrado no diretório atual.")
        print("Baixe o conjunto de dados em: https://dados.pbh.gov.br/dataset/atividades-economicas1")
        return

    print(f"Lendo arquivo CSV de entrada: '{INPUT_CSV_FILE}'...")
    try:
        df = pd.read_csv(INPUT_CSV_FILE, sep=';', low_memory=False, dtype=str) 
        print(f"Lidas com sucesso {len(df)} linhas do arquivo de entrada.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return

    print(f"Filtrando estabelecimentos baseados na coluna '{COL_CNAE_CODIGO}' contendo '{CNAE_CODE_PREFIX_TO_FILTER}'")

   
    df[COL_CNAE_CODIGO] = df[COL_CNAE_CODIGO].astype(str).fillna('') 
    
    original_count = len(df)
    
    # Mantém linhas onde COL_CNAE_CODIGO contém CNAE_CODE_PREFIX_TO_FILTER
    df_filtered = df[df[COL_CNAE_CODIGO].str.contains(CNAE_CODE_PREFIX_TO_FILTER, case=False, na=False)].copy()

    print(f"Filtrando os estabelecimentos possuem 'bar' ou 'restaurante' na descrição da CNAE...")

    COL_DESCRICAO_CNAE = 'DESCRICAO_CNAE_PRINCIPAL'
    df_filtered[COL_DESCRICAO_CNAE] = df_filtered[COL_DESCRICAO_CNAE].astype(str).fillna('')
    df_filtered = df_filtered[df_filtered[COL_DESCRICAO_CNAE].str.contains("bar|restaurante", case=False, na=False)].copy()

    filtered_count = len(df_filtered)

    print(f"Filtragem resultou em {filtered_count} estabelecimentos (de {original_count} originais).")

    if filtered_count == 0:
        print(f"Nenhum estabelecimento encontrado com o código CNAE '{CNAE_CODE_PREFIX_TO_FILTER}'.")
    
    # Formatando endereços
    if not df_filtered.empty:
        df_filtered.loc[:, 'ENDERECO'] = df_filtered.apply(format_address, axis=1)
    else:
        df_filtered.loc[:, 'ENDERECO'] = pd.Series(dtype='object')

    # Tratando o nome fantasia 
    if COL_NOME_FANTASIA in df_filtered.columns:
        df_filtered.loc[:, COL_NOME_FANTASIA] = df_filtered[COL_NOME_FANTASIA].astype(str).fillna('')
    else:
        print(f"Aviso: Coluna '{COL_NOME_FANTASIA}' não encontrada. Será criada vazia.")
        df_filtered.loc[:, COL_NOME_FANTASIA] = '' 
        
    if COL_NOME in df_filtered.columns: 
        df_filtered.loc[:, COL_NOME] = df_filtered[COL_NOME].astype(str).fillna('')
    else:
        print(f"Aviso: Coluna '{COL_NOME}' (mapeada para 'NOME' no original) não encontrada para nome alternativo. Apenas '{COL_NOME_FANTASIA}' será usada se existir.")
        df_filtered.loc[:, COL_NOME] = ''

    # Usa uma cópia de NOME_FANTASIA para NOME_FINAL_TEMP.
    df_filtered.loc[:, 'NOME_FINAL_TEMP'] = df_filtered.get(COL_NOME_FANTASIA, pd.Series([''] * len(df_filtered), index=df_filtered.index))

    # Máscara para identificar onde NOME_FINAL_TEMP (que é o NOME_FANTASIA inicial) está efetivamente vazio
    mask_empty_fantasia = df_filtered['NOME_FINAL_TEMP'].str.strip().replace('', pd.NA).isna() | \
                          df_filtered['NOME_FINAL_TEMP'].str.upper().isin(['NAN', 'NA', 'NULL', 'NONE'])
                          
    # Onde NOME_FANTASIA está vazio, usa o valor de COL_NOME (que é a coluna 'NOME' do original)
    fallback_names = df_filtered.get(COL_NOME, pd.Series([''] * len(df_filtered), index=df_filtered.index))
    df_filtered.loc[mask_empty_fantasia, 'NOME_FINAL_TEMP'] = fallback_names[mask_empty_fantasia]
    
    # Atribui este NOME_FINAL_TEMP para a coluna COL_NOME_FANTASIA
    df_filtered.loc[:, COL_NOME_FANTASIA] = df_filtered['NOME_FINAL_TEMP']
    
    print(f"Colunas no output: {FINAL_OUTPUT_COLUMNS_REQUESTED_BY_USER}")
    
    # Cria colunas vazias (com pd.NA) se não existirem, para evitar erro
    output_df_data = {}
    for col in FINAL_OUTPUT_COLUMNS_REQUESTED_BY_USER:
        if col in df_filtered.columns:
            output_df_data[col] = df_filtered[col]
        else:
            print(f"Aviso: Coluna '{col}' não encontrada nos dados filtrados para a saída. Será adicionada como uma coluna vazia.")
            
            output_df_data[col] = pd.Series([pd.NA] * len(df_filtered), index=df_filtered.index, name=col) 

    df_output = pd.DataFrame(output_df_data, columns=FINAL_OUTPUT_COLUMNS_REQUESTED_BY_USER)


    print(f"Escrevendo dados filtrados para '{OUTPUT_CSV_FILE}'...")
    try:
        df_output.to_csv(OUTPUT_CSV_FILE, index=False, sep=';', encoding='utf-8')
        print(f"Escritas com sucesso.")
    except Exception as e:
        print(f"Erro ao escrever o arquivo CSV de saída: {e}")

    print("Processo de filtragem concluído.")

if __name__ == '__main__':
    main()
