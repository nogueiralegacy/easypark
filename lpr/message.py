from kafka import KafkaProducer
import json

HOST_URL = 'localhost:9092'
TOPIC = 'placas'

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def send_message(plates):
    producer = KafkaProducer(
        bootstrap_servers=[HOST_URL],
        value_serializer=json_serializer
    )
    
    for p in plates:
        data = {
            "placa" : p
        }
        producer.send(TOPIC, data)
        producer.flush()