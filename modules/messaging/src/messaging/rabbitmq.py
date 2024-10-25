from dataclasses import dataclass
from typing import Optional
import pika

@dataclass
class RabbitMQConfig:
    host: str
    user: str
    password: str
    
    declare_exchange: bool = False
    exchange_name: str = ""
    exchange_type: str = ""
    
    declare_queue: bool = False
    queue_name: str = ""
    exclusive_queue: bool = False

@dataclass 
class RabbitMQClient:
    config: RabbitMQConfig
    connection: Optional[pika.BlockingConnection] = None
    channel: Optional[pika.channel.Channel] = None

    def setup_connection(self) -> RabbitMQConfig:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.config.host,
                # credentials=pika.PlainCredentials(
                #     username=self.config.user,
                #     password=self.config.password
                # )
            )
        )
        self.channel = self.connection.channel()
        
        if self.config.declare_exchange:
            self.channel.exchange_declare(
                exchange=self.config.exchange_name,
                exchange_type=self.config.exchange_type
            )
        
        if self.config.declare_queue:
            # result = self.channel.queue_declare(queue=self.config.queue_name, exclusive=self.config.exclusive_queue)
            # queue_name = result.method.queue
            self.channel.queue_declare(queue=self.config.queue_name, exclusive=self.config.exclusive_queue)
            self.channel.queue_bind(exchange=self.config.exchange_name, queue=self.config.queue_name)

        return self
