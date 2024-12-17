from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import json
import time

# Configurações
BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_PLACAS_LIDAS = 'placas-lidas'
TOPIC_PLACAS_VALIDADAS = 'placas-validadas'


# Função para criar tópicos
def criar_topicos():
    admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    topics = [NewTopic(name=TOPIC_PLACAS_LIDAS, num_partitions=1, replication_factor=1),
              NewTopic(name=TOPIC_PLACAS_VALIDADAS, num_partitions=1, replication_factor=1)]

    try:
        admin_client.create_topics(new_topics=topics, validate_only=False)
        print(f"Tópicos '{TOPIC_PLACAS_LIDAS}' e '{TOPIC_PLACAS_VALIDADAS}' criados com sucesso.")
    except TopicAlreadyExistsError:
        print("Tópicos já existem.")
    finally:
        admin_client.close()


# Validação simples da mensagem --> todo: LUCAO PASSAR ESSE AQUI PRO CODIGO DA CAMERA
# LUCAS: FEITO o7
def validar_formato_padrao_placa(placa):
    # Simples validação: Verifica se é uma string com 7 caracteres (formato padrão ABC1234)
    if isinstance(placa, str) and len(placa) == 7 and placa[:3].isalpha() and placa[3:].isdigit():
        return True
    return False


# Chamar a rota pra checar se a placa é válida
def validar_placa_cadastrada(placa):
    return True


def libera_abertura_cancela():
    print("Simulando abertura da cancela do estacionamento")
    time.sleep(5)

# Configura o Producer
def criar_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


# Configura o Consumer
def criar_consumer():
    return KafkaConsumer(
        TOPIC_PLACAS_LIDAS,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="placas-lidas-consumer",
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )


# Processo de leitura, validação e envio
def consumir_e_validar():
    consumer = criar_consumer()
    producer = criar_producer()

    print("Consumindo mensagens do tópico 'placas-lidas'...")
    for mensagem in consumer:
        mensagem = mensagem.value
        print(f"Mensagem recebida: {mensagem}")

        # Validação da placa
        if validar_formato_padrao_placa(mensagem['placa']) and validar_placa_cadastrada(mensagem['placa']):
            print(f"Placa válida e cadastrada: {mensagem['placa']}")

            # Enviar a mesma mensagem para o tópico placas-validadas
            producer.send(TOPIC_PLACAS_VALIDADAS, mensagem)
            print(f"Mensagem enviada para '{TOPIC_PLACAS_VALIDADAS}': {mensagem}")

            # Simula abertura da cancela do estacionamento, possível integração com o sistema do estabelecimento
            libera_abertura_cancela()
        else:
            print(f"Placa inválida: {mensagem['placa']}")

        # Simula processamento constante
        time.sleep(1)


# Função principal
if __name__ == "__main__":
    criar_topicos()
    consumir_e_validar()

