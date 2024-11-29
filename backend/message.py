from kafka import KafkaConsumer
import json
import threading

KAFKA_URL = 'localhost:9092'
TOPIC = 'placas'

messages = []

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

consumer = KafkaConsumer(TOPIC, bootstrap_servers=KAFKA_URL, group_id='my_group', value_deserializer=json_deserializer)

def init_consumer():
    for message in consumer:
        messages.append(f'{message.key}: {message.value}')

def get_messages():
    return messages