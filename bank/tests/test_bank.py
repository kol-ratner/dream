import os
import unittest
from unittest.mock import patch, MagicMock
from src.bank.bank import BankService


class TestBankService(unittest.TestCase):

    @patch('src.bank.bank.RabbitMQClient')
    @patch('src.bank.bank.MongoClient')
    def setUp(self, mock_mongo_client, mock_rabbitmq_client):
        # Mock RabbitMQ
        self.mock_channel = MagicMock()
        self.mock_rabbitmq = MagicMock()
        self.mock_rabbitmq.channel = self.mock_channel
        mock_rabbitmq_client.return_value = self.mock_rabbitmq
        self.mock_rabbitmq.setup_connection.return_value = self.mock_rabbitmq

        # Mock MongoDB
        self.mock_collection = MagicMock()
        self.mock_mongo = MagicMock()
        self.mock_mongo.collection = self.mock_collection
        mock_mongo_client.return_value = self.mock_mongo
        self.mock_mongo.setup_connection.return_value = self.mock_mongo

        self.bank_service = BankService()

    def test_process_transaction(self):
        transaction_data = {'transaction_id': '123'}
        result = self.bank_service.process_transaction(transaction_data)
        
        self.assertEqual(result['transaction_id'], '123')
        self.assertIn('status', result)
        self.assertIn('mongo_id', result)
        self.mock_collection.insert_one.assert_called_once()

    def test_handle_incoming_transaction(self):
        with patch.object(self.bank_service, 'process_transaction') as mock_process:
            mock_process.return_value = {
                'transaction_id': '123',
                'status': 'approved',
                'mongo_id': 'abc123'
            }
            self.bank_service.handle_incoming_transaction({'transaction_id': '123'})
            mock_process.assert_called_once_with({'transaction_id': '123'})

if __name__ == '__main__':
    unittest.main()
