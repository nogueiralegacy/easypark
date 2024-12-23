from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
import json
import time
import requests

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_PLACAS_LIDAS = 'placas-lidas'
TOPIC_PLACAS_VALIDADAS = 'placas-validadas'


def criar_topicos():
    admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    topics = [NewTopic(name=TOPIC_PLACAS_LIDAS, num_partitions=1, replication_factor=1),
              NewTopic(name=TOPIC_PLACAS_VALIDADAS, num_partitions=1, replication_factor=1)]

    try:
        admin_client.delete_topics(topics=['placas-lidas', 'placas-validadas'])
        print(f"Tópicos '{TOPIC_PLACAS_LIDAS}' e '{TOPIC_PLACAS_VALIDADAS}' foram excluídos.")
        time.sleep(5)
    except UnknownTopicOrPartitionError:
        print("Tópicos não existiam para exclusão. Continuando...")

    try:
        admin_client.create_topics(new_topics=topics, validate_only=False)
        print(f"Tópicos '{TOPIC_PLACAS_LIDAS}' e '{TOPIC_PLACAS_VALIDADAS}' criados com sucesso.")
    except TopicAlreadyExistsError:
        print("Tópicos já existem.")
    finally:
        admin_client.close()


# Validação simples da mensagem
def validar_formato_padrao_placa(placa):
    # Simples validação: Verifica se é uma string com 7 caracteres (formato padrão ABC1234)
    if isinstance(placa, str) and len(placa) == 7 and placa[:3].isalpha() and placa[3:].isdigit():
        return True
    return False


# Chamar a rota pra checar se a placa é válida
def validar_placa_cadastrada(mensagem):
    print("Validando se a placa está cadastrada")
    url = "http://realbetis.software:8000/placa/verificar"
    body = {
        "placa": mensagem['placa'],
        "hash_sensor": mensagem['hash_sensor'],
    }

    response = requests.post(url, json=body)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("status"):
            print("Sucesso! Mensagem:", response_data.get("msg"))
            return True
        else:
            print("Deu ruim, reprovamo")
            return False


def libera_abertura_cancela():
    print("Simulando abertura da cancela do estacionamento (5s)")
    time.sleep(5)


# Necessário passar a mensagem pra saber de qual sensor veio (hash)
def registrar_banco_dados(mensagem):
    print("Registrando entrada/saída no banco de dados")
    url = "http://realbetis.software:8000/registro/registrar"
    body = {
        "placa": mensagem['placa'],
        "hash_sensor": mensagem['hash_sensor'],
    }

    response = requests.post(url, json=body)
    if response.status_code == 201:
        response_data = response.json()
        msg = response_data.get("msg")
        if 'realizado com sucesso' in msg:
            print("Registro realizado com sucesso!")
    else:
        print("Deu ruim, reprovamo")


def criar_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def criar_consumer():
    return KafkaConsumer(
        TOPIC_PLACAS_LIDAS,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="placas-lidas-consumer",
        enable_auto_commit=False,
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )


# Processo de leitura, validação e envio
def consumir_e_validar():
    consumer = criar_consumer()
    producer = criar_producer()

    print("Consumindo mensagens do tópico 'placas-lidas'...")
    for mensagem in consumer:
        print("------ INICIOU EXECUÇÃO ------")
        mensagem = mensagem.value
        print(f"Mensagem recebida: {mensagem}")

        if validar_formato_padrao_placa(mensagem['placa']):
            if validar_placa_cadastrada(mensagem):
                print(f"Placa válida e cadastrada no sistema: {mensagem['placa']}")

                # Enviar a mesma mensagem para o tópico placas-validadas
                producer.send(TOPIC_PLACAS_VALIDADAS, mensagem)
                print(f"Mensagem enviada para '{TOPIC_PLACAS_VALIDADAS}': {mensagem}")

                # Simula abertura da cancela do estacionamento, possível integração com o sistema do estabelecimento
                libera_abertura_cancela()

                # Registra entrada/saída no banco de dados
                registrar_banco_dados(mensagem)
            else:
                print("O formato da placa é valido, porém ela não está cadastrada!")
        else:
            print(f"Placa inválida: {mensagem['placa']}")

        consumer.commit()  # Confirma que a mensagem foi consumida ("andando com o ponteiro")

        # Simula processamento constante
        print("------ FINALIZOU EXECUÇÃO ------")
        time.sleep(15)


# Função principal
if __name__ == "__main__":
    criar_topicos()
    consumir_e_validar()

