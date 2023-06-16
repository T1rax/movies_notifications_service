from rabbitmq.client import RabbitMQ
from rabbitmq.settings import settings


credentials = {
    "host": settings.host,
    "port": settings.port,
    "username": settings.username,
    "password": settings.password,
}


def get_queue(name: str, prefix: str = "notifications", delimiter: str = "_"):
    return delimiter.join(filter(None, [prefix, name]))


message_processing_queue = RabbitMQ(
    queue=get_queue(name="message_processing"), **credentials
)

message_sending_queue = RabbitMQ(
    queue=get_queue(name="message_sending"), **credentials
)
