import os
import unittest
from unittest.mock import patch, MagicMock
from src.store.store import StoreService


class TestStoreService(unittest.TestCase):

    @patch('src.store.store.RabbitMQClient')
    def setUp(self, mock_rabbitmq_client):
        # Mock the RabbitMQ client and channel
        self.mock_channel = MagicMock()
        self.mock_client = MagicMock()
        self.mock_client.channel = self.mock_channel

        mock_rabbitmq_client.return_value = self.mock_client
        self.mock_client.setup_connection.return_value = self.mock_client

        # Set test environment variables
        os.environ['RABBITMQ_HOST'] = 'localhost'
        os.environ['RABBITMQ_USER'] = 'guest'
        os.environ['RABBITMQ_PASSWORD'] = 'guest'

        # Instantiate the StoreService
        self.store_service = StoreService()

    def test_generate_transaction(self):
        transaction = self.store_service.generate_transaction()
        self.assertIn('transaction_id', transaction)
        self.assertIn('store_code', transaction)
        self.assertIn('amount', transaction)
        self.assertEqual(transaction['store_code'], 'STORE_001')
        self.assertGreaterEqual(transaction['amount'], 10.0)
        self.assertLessEqual(transaction['amount'], 500.0)

    @patch('json.dumps')
    def test_send_transaction(self, mock_json_dumps):
        mock_json_dumps.return_value = '{"transaction_id": "123", "store_code": "STORE_001", "amount": 100.0}'
        transaction_data = {
            'transaction_id': '123',
            'store_code': 'STORE_001',
            'amount': 100.0
        }
        self.store_service.send_transaction(transaction_data)
        self.mock_client.channel.basic_publish.assert_called_once_with(
            exchange='transactions',
            routing_key='',
            body=mock_json_dumps.return_value.encode('utf-8')
        )


if __name__ == '__main__':
    unittest.main()
