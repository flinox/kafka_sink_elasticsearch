## Programa para criar connectores kafka
## Sintaxe de uso: python create_connector.py <caminho/nome_arquivo.properties> <hostname:8083>
## Le o arquivo .properties, converte em .json e chama API REST para criar o connector no connect
## By: Fernando Lino em 05/12/2018
## export source_user=bla_bla_name
## export source_pass=bla_bla_pass
## python create_connector.py ./connectors/SOURCE-CONNECTOR.properties 172.168.0.1:31083


import json 
import javaproperties
import argparse
import requests
import textwrap
import os
#import sys
from datetime import datetime

# Define os parametros esperados e obrigatorios
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''\
         Criacao de conectores de SOURCE e SINK para KAFKA ! 
         ----------------------------------------------------------------------------------------
         Created By: Fernando Lino Di Tomazzo Silva ( https://www.linkedin.com/in/flinox )
         Version 1.0 - 2019-08-13 

         Sintaxe: 
         python create_connector.py ./connectors/SOURCE-CONNECTOR.properties 172.168.0.1:31083

         Obs.:
          É preciso informar as variaveis de ambiente source_user e source_pass para acesso ao banco de origem da conexao que será criada.

         '''))

parser.add_argument("arquivo", help="Informe o arquivo .properties do conector que deseja criar")
parser.add_argument("host", help="Informe o nome do host do servidor connect e a porta")
args = parser.parse_args()

# pega o nome e pasta do arquivo .properties
nome_extensao = os.path.basename(args.arquivo)
folder = os.path.dirname(args.arquivo)
nome = os.path.splitext(nome_extensao)[0]

# Verifica se o usuario e senha do source foi localizado nas variaveis de ambiente
try:
    source_user = os.environ['source_user']
    source_pass = os.environ['source_pass']
except:
    #e = sys.exc_info()[0]
    #print("Error: %s" % e)
    print("ERRO: Usuario e senha nao encontrado nas variaveis de ambiente!")
    exit(1)

# converte arquivo .properties para .json para envio no REST
# Read file
try:
    with open(args.arquivo, 'r') as f:
        properties_file = f.read()
except:
    print("ERRO: Não foi possível encontrar o arquivo %s" % args.arquivo)
    exit(2)

# Load properties do json
json_file = javaproperties.loads(properties_file)
json_file['connection.user'] = source_user
json_file['connection.password'] = source_pass
json_file_original = json_file

json_connector = {}
json_connector['name'] = json_file['name']
del json_file['name']

json_connector['config'] = json_file
json_connector_file = json.dumps(json_connector, indent=4, sort_keys=True)
#print(json_connector_file)

# Gera o arquivo json format
new_file = open(folder+'/'+nome+'.json', "w")
new_file.write(json.dumps(json.loads(json_connector_file), indent=4, sort_keys=True))
new_file.close()

arquivo_json = folder+'/'+nome+'.json'

# Le o arquivo e prepara json para o POST
with open(arquivo_json,"r") as f:
    arquivo=json.load(f)

data = json.dumps(arquivo, separators=(',', ':'))

# Monta os headers
headers = {"Accept": "application/json",
        "Content-Type": "application/json"}

# Monta a URL considerando o nome do arquivo/schema
url = ('http://%s/connectors/' % (args.host))

# Print values
print('\n############ Criando connector %s ############' % nome)
print(datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
print("\nUrl: \n%s" % url)
print("\nConnector: \n%s" % args.arquivo)
print("\nHeaders: \n%s" % headers)
print("\nData: \n%s" % " ") #data

# Realiza o POST
response = requests.request("POST",url, data=data, headers=headers)
print("\nResponse:")
print(response.text + '\n\n' + str(response.status_code) + '\n' + response.reason )

# Se conflict tenta atualizar o connector
if response.status_code == 409:
    print("\n\n ###### Tentando atualizar o connector ###### ")
    print(datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))    
    # Load properties do json
    json_file_original = json.dumps(json_file_original, indent=4, sort_keys=True)

    # Gera o arquivo json format
    upd_file = open(folder+'/'+nome+'.json', "w")
    upd_file.write(json.dumps(json.loads(json_file_original), indent=4, sort_keys=True))
    upd_file.close()

    arquivo_json = folder+'/'+nome+'.json'

    # Le o arquivo e prepara json para o POST
    with open(arquivo_json,"r") as f:
        arquivo=json.load(f)

    data = json.dumps(arquivo, separators=(',', ':'))

    # Monta os headers
    headers = {"Accept": "application/json",
            "Content-Type": "application/json"}

    # Monta a URL considerando o nome do arquivo/schema
    url = ('http://%s/connectors/%s/config' % (args.host,nome))

    # Print values
    print("\nUrl: \n%s" % url)
    print("\nConnector: \n%s" % args.arquivo)
    print("\nHeaders: \n%s" % headers)
    print("\nData: \n%s" % data)

    # Realiza o POST
    response = requests.request("PUT",url, data=data, headers=headers)
    print("\nResponse:")
    print(response.text + '\n\n' + str(response.status_code) + ' - ' + response.reason)

# delete file
# arquivo_json = folder+'/'+nome+'.json'

