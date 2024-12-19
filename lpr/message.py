from kafka import KafkaProducer
import json
import time

HOST_URL = 'localhost:9092'
TOPIC = 'placas-lidas'

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def send_message(plate):
    producer = KafkaProducer(
        bootstrap_servers=[HOST_URL],
        value_serializer=json_serializer
    )
    
    data = {
        "placa": plate,
        "timestamp": time.time(),
        "hash_sensor": "mockHash_7070"
    }
    producer.send(TOPIC, data)
    producer.flush()
    