import logging
import random
import time
import uuid
import signal
import sys
import json
import pika
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class StoreService:
    def __init__(self):
        self.rabbitmq_host = os.getenv('RABBITMQ_HOST')
        self.rabbitmq_user = os.getenv('RABBITMQ_USER')
        self.rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbitmq_host,
                credentials=pika.PlainCredentials(
                    username=self.rabbitmq_user, 
                    password=self.rabbitmq_password
                )
            )
        )
        logging.info("RabbitMQ connection established")

        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange="transactions",
            exchange_type="fanout")
        logging.info("Store Service Initialized")

    def generate_transaction(self):
        """
        Generates a new transaction with a random amount.

        Returns:
            dict: A dictionary containing transaction details.
        """
        transaction_data = {
            "transaction_id": str(uuid.uuid4()),
            "store_code": "STORE_001",
            "amount": random.uniform(10.0, 500.0),
        }
        logging.info(
            f"Generated transaction {transaction_data['transaction_id']} with amount: {transaction_data['amount']}"
        )
        return transaction_data

    def send_transaction(self, transaction_data):
        """
        Sends the transaction to the bank.

        Args:
            transaction_data (dict): A dictionary containing the transaction details.
        """
        try:
            message = json.dumps(transaction_data).encode("utf-8")
            self.channel.basic_publish(
                exchange="transactions", routing_key="", body=message
            )
            logging.info(
                f"Sending transaction {transaction_data['transaction_id']} to the bank"
            )
        except Exception as e:
            logging.error(
                f"Failed to send transaction {transaction_data['transaction_id']}: {str(e)}"
            )
            raise

    def run(self):
        """
        Starts the main loop of the Store Service to generate and send transactions.
        """
        logging.info("Store Service is running...")
        while True:
            try:
                transaction_data = self.generate_transaction()
                self.send_transaction(transaction_data)
                time.sleep(random.randint(1, 10))

            except Exception as e:
                logging.error(f"Error in transaction loop: {str(e)}")


def signal_handler(self, sig, frame):
    logging.info("Gracefully shutting down the Store Service...")
    self.connection.close()
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Instantiate the StoreService class and start it
    store_service = StoreService()
    store_service.run()
