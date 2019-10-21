
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
        
        #####################################################
        # CONSUME MESSAGES OF TOPICS
        #####################################################

        consume_topics_endpoint = endpoint + '/consumers/' + consumer_group + '/instances/' + consumer_id + '/records?timeout='+timeout+'&max_bytes='+max_bytes
        consume_topics_header = {'accept' : 'application/vnd.kafka.avro.v2+json'}

        time.sleep(1)
        r = requests.get(consume_topics_endpoint, headers=consume_topics_header)

        print('\n>>>>>>>>>> CONSUME MESSAGES OF TOPICS <<<<<<<<<<')
        print(' Endpoint: ' + consume_topics_endpoint)
        print(' Consumer_id_header: ' + str(consume_topics_header))
        print(' Response code: %d\n' % r.status_code)
        print(r.text+'\n')

        #with open('messages.json', 'w',encoding='utf-8') as json_file:
        #    parsed = json.loads(r.text)
        #    json.dump(parsed, json_file,indent=4, sort_keys=True, ensure_ascii=False)

        if (r.status_code == 200):
            # Ler o objeto json

            print('\n>>>>>>>>>> SINK TO ELASTICSEARCH <<<<<<<<<<')
            print(' Index: '+elasticsearch_index)
            print(' Doc_Type: '+elasticsearch_doc_type)
            for json_object in r.json(): 

                #print(json_object['key'])
                #print(json_object['value'])

                #print(json_object['topic'])
                #print(json_object['partition'])
                #print(json_object['offset'])

                # Publicar a mensagem no ElasticSearch
                
                print(' Key: ' + json.dumps(json_object['key']))
                es.index(index=elasticsearch_index, doc_type=elasticsearch_doc_type, id=json_object['key'], body=json_object['value'])
                time.sleep(1)
                #print(json_object['key']['IDOFERTA'])

                # for (k, v) in json_object.items():
                #     print("Key: " + k)
                #     print("Value: " + str(v))                

                #     print(k['topic'])

            
            # Pegar a mensagem do ElasticSearch
            # print(es.get(index="flinox_teste", doc_type="_doc", id="1"))


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

#####################################################
# ADD CONSUMER ID TO CONSUMER GROUP
#####################################################
consumer_group = 'NOME_CONSUMER_GROUP'
consumer_id = 'consumer-01'
message_format = 'avro'
message_offset = 'earliest' # latest / earliest / smallest
commit_offset = 'true'
topicos = 'TOPIC-NAME'
timeout = '10000' 
max_bytes = '20000'

print(' Consumer_group: ' + consumer_group)
print(' Consumer_id: ' + consumer_id)
print(' Message_format: ' + message_format)
print(' Message_offset: ' + message_offset)
print(' Commit_offset: ' + commit_offset)
print(' Topicos: ' + topicos )
print(' Timeout: ' + timeout )
print(' Max_bytes: ' + max_bytes )

endpoint = "http://172.168.0.1:31082"
consumer_id_endpoint = endpoint + '/consumers/' + consumer_group

consumer_id_header = {'content-type' : 'application/vnd.kafka.v2+json'}

consumer_id_data =  '{'
consumer_id_data +=  '"name": "'+consumer_id+'",'
consumer_id_data +=  '"format": "'+message_format+'",'
consumer_id_data +=  '"auto.offset.reset": "'+message_offset+'",'
consumer_id_data +=  '"auto.commit.enable": "'+commit_offset+'"'
consumer_id_data +=  '}'

r = requests.post(consumer_id_endpoint, data=consumer_id_data, headers=consumer_id_header)

print('\n>>>>>>>>>> ADD CONSUMER ID TO CONSUMER GROUP <<<<<<<<<<')
print(' Endpoint: ' + consumer_id_endpoint)
print(' Consumer_id_header: ' + str(consumer_id_header))
print(' Consumer_id_data: ' + consumer_id_data)
print(' Response code: %d\n' % r.status_code)
print(' ' + r.text+'\n')

# Se houve sucesso ao adicionar o consumer id ao consumer group
if (r.status_code in (200,204)):

    #####################################################
    # SUBSCRIBE TOPICS TO CONSUMER ID OF CONSUMER GROUP
    #####################################################
    subscribe_topics_endpoint = endpoint + '/consumers/' + consumer_group + '/instances/' + consumer_id + '/subscription'
    subscribe_topics_header = {'content-type' : 'application/vnd.kafka.v2+json'}

    subscribe_topics_data =  '{'
    subscribe_topics_data +=  '"topics": ['
    subscribe_topics_data +=  '"'+topicos+'"'
    subscribe_topics_data +=  ']}'    

    time.sleep(2)
    r1 = requests.post(subscribe_topics_endpoint, data=subscribe_topics_data, headers=subscribe_topics_header)

    print('\n>>>>>>>>>> SUBSCRIBE TOPICS TO CONSUMER ID OF CONSUMER GROUP <<<<<<<<<<')
    print(' Endpoint: ' + subscribe_topics_endpoint)
    print(' Consumer_id_header: ' + str(subscribe_topics_header))
    print(' Consumer_id_data: ' + subscribe_topics_data)
    print(' Response code: %d\n' % r.status_code)
    print(r1.text+'\n')

while True:
    task = MyProcessingThread()
    task.start()
    try:
        task.join()
    except KeyboardInterrupt:
        sys.exit()

       