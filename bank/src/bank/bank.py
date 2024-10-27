from datetime import datetime
import json
import logging
import os
import random
import signal
import sys
import time

from messaging.rabbitmq import RabbitMQConfig, RabbitMQClient
from persistance.mongo import MongoConfig, MongoClient

from fastapi import FastAPI, status
import uvicorn


class BankService:

    def __init__(self):
        self._init_logging()
        self.rabbitmq = self._setup_rabbitmq()
        self.mongodb = self._setup_mongo()
        logging.info("Bank Service Initialized")

    def _init_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s')

    def _setup_rabbitmq(self) -> RabbitMQClient:
        config = RabbitMQConfig(
            host=os.getenv('RABBITMQ_HOST'),
            user=os.getenv('RABBITMQ_USER'),
            password=os.getenv('RABBITMQ_PASSWORD'),
            declare_exchange=True,
            exchange_name='transactions',
            exchange_type='fanout',
            declare_queue=True,
            queue_name='transactions',
            exclusive_queue=False
        )
        return RabbitMQClient(config=config).setup_connection()

    def _setup_mongo(self) -> MongoClient:
        config = MongoConfig(
            host=os.getenv('MONGODB_HOST'),
            replicaset=os.getenv('MONGODB_REPLICASET'),
            user=os.getenv('MONGODB_USER'),
            password=os.getenv('MONGODB_PASSWORD'),
            database="bankdb",
            collection="transactions",
            authSource="admin",
            authMechanism="SCRAM-SHA-256",
        )
        return MongoClient(config=config).setup_connection()

    def check_readiness(self) -> bool:
        """
        Checks if the service is ready by verifying RabbitMQ and MongoDB connections.
        """
        try:
            # Check RabbitMQ connection
            if not self.rabbitmq.connection.is_open:
                return False
            if not self.rabbitmq.channel.is_open:
                return False

            # Check MongoDB connection
            self.mongodb.client.admin.command('ping')

            return True
        except Exception as e:
            logging.error(f"Readiness check failed: {str(e)}")
            return False

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

            transaction_data.update({
                'status': status,
                'processed_at': datetime.now().isoformat()
            })

            result = self.mongodb.collection.insert_one(transaction_data)
            logging.info(
                f"Transaction {transaction_data['transaction_id']} processed with status: {status}")
            return {
                'transaction_id': transaction_data['transaction_id'],
                'status': status,
                'mongo_id': str(result.inserted_id)
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
                # Explicitly acknowledge successful processing
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except json.JSONDecodeError as e:
                logging.error(f"Failed to decode message: {str(e)}")
                # Reject and requeue malformed messages
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            except Exception as e:
                logging.error(f"Error processing message: {str(e)}")
                # Reject and requeue failed messages
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        # Set prefetch count to control how many messages each consumer gets
        self.rabbitmq.channel.basic_qos(prefetch_count=1)
        self.rabbitmq.channel.basic_consume(
            queue=self.rabbitmq.config.queue_name,
            on_message_callback=callback,
            auto_ack=False)

        try:
            self.rabbitmq.channel.start_consuming()
        except Exception as e:
            logging.error(f"Unexpected error in consumer: {str(e)}")


def signal_handler(self, sig, frame):
    logging.info('Gracefully shutting down the Bank Service...')
    self.connection.close()
    sys.exit(0)


if __name__ == '__main__':
    app = FastAPI()
    bank_service = BankService()

    @app.on_event("startup")
    async def startup_event():
        bank_service.run()

    @app.get("/health")
    async def health_check():
        return status.HTTP_200_OK

    @app.get("/ready")
    async def ready_check():
        return (status.HTTP_200_OK
                if bank_service.check_readiness()
                else status.HTTP_503_SERVICE_UNAVAILABLE)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('SERVICE_PORT')))
