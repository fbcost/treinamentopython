# -*- coding: utf-8 -*-
import requests
import sys
import json
import pandas as pd

# Função para chamar a API com base no ID da assinatura
def chamar_api(id_assinatura):
    url = f'http://172.20.230.253:8280/services/odin_ba/subscription/{id_assinatura}/resources'
    # Faça a chamada para a API
    response = requests.get(url)
    
    # Verifique se a resposta foi bem-sucedida
    if response.status_code == 200:
        # Retorne os dados desejados da resposta da API
        data = response.json()
        return data
    else:
        # Em caso de falha, imprima uma mensagem de erro
        print(f'Erro ao chamar API para assinatura {id_assinatura}')
        return None

# Função para ler os IDs de assinatura de um arquivo
def ler_ids_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        ids = [line.strip() for line in file if line.strip()]
    return ids

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script_call_api.py arquivo_ids_assinaturas.txt")
        sys.exit(1)
 
    nome_arquivo = sys.argv[1]
 
    # Lista de IDs de assinaturas lidos do arquivo
    lista_ids_assinaturas = ler_ids_de_arquivo(nome_arquivo)

    # Lista para armazenar os dados
    dados = []

    # Loop através dos IDs de assinaturas e chamar a API para cada um
    for id_assinatura in lista_ids_assinaturas:
        resultado = chamar_api(id_assinatura)
        if resultado:
            for resource in resultado['result']['resources']:
                dados.append({
                    'SubscriptionID': id_assinatura,
                    'ResourceID': resource['ResourceID'],
                    'ResourceName': resource['ResourceName'],
                    'IncludedAmount': resource['IncludedAmount'],
                    'AdditionalAmount': resource['AdditionalAmount'],
                    'OrderedAmount': resource['OrderedAmount'],
                    'RecurringFee': resource['RecurringFee'],
                    'OveruseFee': resource['OveruseFee']
                })

    # Converter a lista de dicionários para DataFrame do pandas
    df = pd.DataFrame(dados)

    # Escrever os dados para um arquivo Excel
    excel_file = 'dados_assinaturas.xlsx'
    df.to_excel(excel_file, index=False)

    print(f'Dados gravados com sucesso em {excel_file}')
