import json
import logging
import os
import random
import signal
import sys
import time
from messaging.rabbitmq import RabbitMQConfig, RabbitMQClient


class BankService:

    def __init__(self):
        self._init_logging()
        self.rabbitmq = self._setup_rabbitmq()        
        # self._init_postgres()
        logging.info("Bank Service Initialized")

    def _init_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s')

    def _setup_rabbitmq(self) -> RabbitMQClient:
        config = RabbitMQConfig(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            user=os.getenv('RABBITMQ_USER', 'guest'),
            password=os.getenv('RABBITMQ_PASSWORD', 'guest'),
            declare_exchange=True,
            exchange_name='transactions',
            exchange_type='fanout',
            declare_queue=True,
            queue_name='transactions',
            exclusive_queue=True
        )
        return RabbitMQClient(config=config).setup_connection()

    def process_transaction(self, transaction_data):
        """
        Simulates processing a transaction by the bank.

        Args:
            transaction_data (dict): A dictionary containing the transaction details.

        Returns:
            dict: Processed transaction result with status.
        """
        try:
            # Simulate processing time
            time.sleep(random.uniform(0.5, 2.0))

            # Randomly determine if the transaction is successful
            status = random.choice(['approved', 'declined'])

            logging.info(
                f"Transaction {transaction_data['transaction_id']} processed with status: {status}")

            # TODO: Insert transaction result into the database

            return {
                'transaction_id': transaction_data['transaction_id'],
                'status': status
            }

        except Exception as e:
            logging.error(
                f"Error processing transaction {transaction_data['transaction_id']}: {str(e)}")
            raise

    def handle_incoming_transaction(self, transaction_data):
        """
        Handles the incoming transaction by processing it and sending a response.

        Args:
            transaction_data (dict): A dictionary containing the transaction details.
        """
        try:
            response = self.process_transaction(transaction_data)
            logging.info(
                f"Processed transaction: {response['transaction_id']} with status: {response['status']}")
        except Exception as e:
            logging.error(f"Failed to handle incoming transaction: {str(e)}")

    def run(self):
        """
        Starts the main loop of the Bank Service to handle incoming transactions.
        """
        logging.info("Bank Service is running...")

        def callback(ch, method, properties, body):
            try:
                transaction_data = json.loads(body)
                self.handle_incoming_transaction(transaction_data)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode message: {str(e)}")
            except Exception as e:
                logging.error(f"Error processing message: {str(e)}")

        self.rabbitmq.channel.basic_consume(
            queue=self.rabbitmq.config.queue_name,
            on_message_callback=callback,
            auto_ack=True)

        try:
            self.rabbitmq.channel.start_consuming()
        except Exception as e:
            logging.error(f"Unexpected error in consumer: {str(e)}")


def signal_handler(self, sig, frame):
    logging.info('Gracefully shutting down the Bank Service...')
    self.connection.close()
    sys.exit(0)


if __name__ == '__main__':
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Instantiate the BankService class and start it
    bank_service = BankService()
    bank_service.run()
