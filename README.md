# Introdução 

A program to read a kafka topic in avro format and publish every message to a index of ElasticSearch on AWS ( Needs authentication )

Programa para ler um topico kafka em formato avro e gravar cada mensagem em um index de um Elasticsearch na AWS com autenticação.

Espero que ajude, qualquer melhoria ou sugestão entre em contato.
https://www.linkedin.com/in/flinox/

Fernando Lino ( Flinox ).

# Pre reqs
```
apt install python 3.6
apt install python3-pip
apt install awscli
pip3 install confluent_kafka
pip3 install javaproperties
pip3 install kafka
pip3 install elasticsearch
pip3 install requests
pip3 install requests-aws4auth
pip3 install boto3

AWS CLI devidamente configurado.
```



# Dados do servidor KAFKA on Premises disponibilizado
```
{
  "hostname": "172.168.0.1",
  "hostname_schema_registry": "172.168.0.1",
  "hostname_kafka_rest": "172.168.0.1",
  "hostname_kafka_connect": "172.168.0.1",
  "port_ksql": "31088",
  "port_schema_registry": "31081",
  "port_kafka_rest": "31082",
  "port_connect": "31083"
}
```

# CONECTOR - Criando o conector de source
```
export source_user=<usuario>
export source_pass=<senha> 
python create_connector.py ./connectors/SOURCE-CONNECTOR.properties 172.168.0.1:31083
```
# CONECTOR - Deletando
```
python delete_connector.py topic-name 172.168.0.1:31083
```

# TOPICO - Criando
```
python crud_topics.py 172.168.0.1:31090 create_topics topic-name 10 3
```
- Onde 10 é o número de partições desejada.
- Onde 3 é o número de replicas.

# TOPICO - Deletando
```
docker exec -it kafka_client bash -c "kafka-topics --zookeeper 172.168.0.1:31181 --delete --topic topic-name"
```

# TOPICO - Consumindo mensagens avro do topico
```
docker exec -it kafka_client bash -c "kafka-avro-console-consumer --bootstrap-server 172.168.0.1:31091 --topic topic-name --timeout-ms 600000 --property print.key=true --property group.id=flinox --property schema.registry.url=http://172.168.0.1:31081 --from-beginning"
```

# KAFKA CLIENT
Disponibilizando um container kafka client para executar linhas de comandos do kafka.

# KAFKA CLIENT - Building
```
docker build -t flinox/kafka_client ./kafka_client/.
```
# KAFKA CLIENT - Running 
```
docker run -it --name kafka_client --hostname kafka_client -v $PWD/kafka_client/app_consumer/:/go/src/app_consumer -v $PWD/kafka_client/app_producer/:/go/src/app_producer -v $PWD/kafka_client/ssl/:/opt/ssl flinox/kafka_client /bin/bash
```

# KAFKA CLIENT - Executando comandos
```
docker exec -it kafka_client bash -c "kafka-topics --zookeeper 172.168.0.1:31181 --list"
```
- Exemplo listando os topicos.


# Aplicativo para realizar o consumo de mensagens em formato avro em um topico do kafka e enviar as mensagens para o ELASTICSEARCH
```
export AWS_ACCESS_KEY_ID=__YOUR_ACCESS_KEY__
export AWS_SECRET_ACCESS_KEY=__YOUR_SECRET_KEY__
export AWS_DEFAULT_REGION=us-east-1

python ./consumer/sink_elasticsearch.py
```

- A Chave usada é a mesma chave do topico kafka.

# Aplicativo para consultar a mensagem gravada no ELASTICSEARCH
```
export AWS_ACCESS_KEY_ID=__YOUR_ACCESS_KEY__
export AWS_SECRET_ACCESS_KEY=__YOUR_SECRET_KEY__
export AWS_DEFAULT_REGION=us-east-1

python ./consumer/check_data_elasticsearch.py
```

# ELASTICSEARCH - Comandos exemplo, você pode adaptar o aplicativo "consulta_elasticsearch" para executar esses comandos abaixo:

# Get document
```
curl -XGET 'hostname-aws-elasticsearch.com/topic-name-ELASTICSEARCH-SINK/_search?pretty'
```

# Put document
```
curl -XPUT 'hostname-aws-elasticsearch.com/index_name/type_name/1?pretty' -d '{ "name": "flinox", "linkedin": "https://www.linkedin.com/in/flinox/" }'
```

# Check the indexes
```
curl 'hostname-aws-elasticsearch.com/_cat/indices?v'
```

# Check the health of cluster
```
curl 'hostname-aws-elasticsearch.com/_cat/health?v'
```

# Check the nodes
```
curl 'hostname-aws-elasticsearch.com/_cat/nodes?v'
```

# Problemas encontrados

- Não foi possível criar um conector de sink da confluent porque ele não está preparado para fazer autenticação AWS para que seja possível realizar o sink em um ElasticSearch que fica na AWS.

- Erro no conector de source quando o campo que será considerado como base de delta de leituras ( Ex.: LAST_UPDATE ) não está definido como "not null" na origem. Para contornar deve-se usar o parametro validate.non.null=false




# Referencias

https://sematext.com/blog/kafka-connect-elasticsearch-how-to/

https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-aws-integrations.html

https://docs.aws.amazon.com/cli/latest/reference/es/describe-elasticsearch-domain.html

https://github.com/joona/aws-es-curl

https://github.com/darenr/python-kafka-elasticsearch/blob/master/elasticsearch_consumer.py

https://docs.aws.amazon.com/pt_br/elasticsearch-service/latest/developerguide/es-gsg.html

https://docs.aws.amazon.com/pt_br/elasticsearch-service/latest/developerguide/es-createupdatedomains.html

https://speakerdeck.com/rmoff/building-streaming-data-pipelines-with-elasticsearch-apache-kafka-and-ksql?slide=33

https://www.confluent.io/blog/the-simplest-useful-kafka-connect-data-pipeline-in-the-world-or-thereabouts-part-2/

https://www.elastic.co/blog/just-enough-kafka-for-the-elastic-stack-part1

https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-indexing.html

https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-gsg-upload-data.html

https://docs.confluent.io/current/connect/kafka-connect-s3/index.html#s3-connector-credentials

https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-ac.html#es-managedomains-signing-service-requests

https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html#sig-v4-examples-get-auth-header

https://github.com/darenr/python-kafka-elasticsearch

https://docs.confluent.io/current/kafka-rest/monitoring.html#endpoints