## Programa para deletar connectores kafka
## Sintaxe de uso: python delete_connector.py <nome_conector> <hostname:porta>    ## normalmente porta 8083
## By: Fernando Lino em 26/11/2018
## python delete_connector.py connector-source.properties 172.168.0.1:31083

import json 
import argparse
import requests
import os


# Define os parametros esperados e obrigatorios
parser = argparse.ArgumentParser()
parser.add_argument("nome", help="Informe o nome do conector que deseja excluir")
parser.add_argument("host", help="Informe o nome do host do servidor connect e a porta")
args = parser.parse_args()

# Monta os headers
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}

# Monta a URL considerando o nome do arquivo/schema
url = 'http://%s/connectors/%s' % (args.host,args.nome)

# Print values
print("\nUrl: \n%s" % url)
print("\nConnector: \n%s" % args.nome)
print("\nHeaders: \n%s" % headers)

# Realiza o POST
response = requests.request("DELETE",url, headers=headers)
print("\nResponse:")
print(response.text + '\n\n' + str(response.status_code) + ' - ' + response.reason)
