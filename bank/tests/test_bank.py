import os
import unittest
from unittest.mock import patch, MagicMock
from src.bank.bank import BankService


class TestBankService(unittest.TestCase):

    @patch('bank.bank.pika.BlockingConnection')
    def setUp(self, mock_connection):
        os.environ['RABBITMQ_HOST'] = 'localhost'
        self.mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = self.mock_channel
        self.bank_service = BankService()

    def test_init(self):
        self.assertIsNotNone(self.bank_service.connection)
        self.assertIsNotNone(self.bank_service.channel)
        self.mock_channel.exchange_declare.assert_called_once()
        self.mock_channel.queue_declare.assert_called_once()
        self.mock_channel.queue_bind.assert_called_once()

    @patch('bank.bank.time.sleep')
    @patch('bank.bank.random.choice')
    def test_process_transaction(self, mock_choice, mock_sleep):
        mock_choice.return_value = 'approved'
        transaction_data = {'transaction_id': '123'}
        result = self.bank_service.process_transaction(transaction_data)
        self.assertEqual(result['transaction_id'], '123')
        self.assertEqual(result['status'], 'approved')
        mock_sleep.assert_called_once()

    def test_handle_incoming_transaction(self):
        with patch.object(self.bank_service, 'process_transaction') as mock_process:
            mock_process.return_value = {
                'transaction_id': '123', 'status': 'approved'}
            self.bank_service.handle_incoming_transaction(
                {'transaction_id': '123'})
            mock_process.assert_called_once_with({'transaction_id': '123'})

    @patch('bank.bank.json.loads')
    def test_run(self, mock_json_loads):
        mock_json_loads.return_value = {'transaction_id': '123'}
        with patch.object(self.bank_service, 'handle_incoming_transaction'):
            self.bank_service.run()
            self.mock_channel.basic_consume.assert_called_once()
            self.mock_channel.start_consuming.assert_called_once()


if __name__ == '__main__':
    unittest.main()
