
import sys, os, base64, datetime, hashlib, hmac 
import requests, time, json, threading
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3


# Processamento das mensagens
class MyProcessingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        
        print('\n>>>>>>>>>> READING FROM ELASTICSEARCH <<<<<<<<<<')
        print(' Index: '+elasticsearch_index)
        print(' Doc_Type: '+elasticsearch_doc_type)

        # Pegar a mensagem do ElasticSearch
        print(es.get(index=elasticsearch_index, doc_type=elasticsearch_doc_type, id=key))
        time.sleep(1)

#####################################################
# ELASTICSEARCH 
#####################################################
            
elasticsearch_hostname = 'hostname-aws.com'
elasticsearch_region = 'us-east-1'
elasticsearch_service = 'es'
elasticsearch_index = "nome_do_index_elasticsearch"
elasticsearch_doc_type = "nome_doc_type_elasticsearch"


credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, elasticsearch_region, elasticsearch_service, session_token=credentials.token)

es = Elasticsearch(
    hosts = [{'host': elasticsearch_hostname, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)


# SAMPLE LIST OF MESSAGES KEYS TO LIST
keys = []
keys.append({"ID": "2467811-51156918-4607224-67110-1900521-3-12"})
keys.append({"ID": "2467810-51155907-4617712-67110-1900521-3-12"})
keys.append({"ID": "2467341-51143412-4624594-67110-1900521-8-12"})
keys.append({"ID": "2466272-51144685-4621148-67110-1900521-8-12"})
keys.append({"ID": "2466271-51144367-4624595-67110-1900521-8-12"})
keys.append({"ID": "2466270-51142387-4621149-67110-1900521-8-12"})
keys.append({"ID": "2466269-51143731-4627967-67110-1900521-8-12"})
keys.append({"ID": "2466267-51143023-4617716-67110-1900521-2-12"})
keys.append({"ID": "2466266-51142705-4617715-67110-1900521-8-12"})
keys.append({"ID": "2466265-51144049-4617717-67110-1900521-8-12"})
keys.append({"ID": "2466264-51142069-4624596-67110-1900521-8-12"})
keys.append({"ID": "2466263-51141751-4624597-67110-1900521-8-12"})
keys.append({"ID": "2466262-51141432-4603685-67110-1900521-8-12"})


for i, key in enumerate(keys):

    task = MyProcessingThread()
    task.start()
    try:
        task.join()
    except KeyboardInterrupt:
        sys.exit()

       