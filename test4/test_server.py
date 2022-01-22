#У меня был код без функций
import unittest

from server import handle_message
from utils import load_configs


class TestServer(unittest.TestCase):
    CONFIGS = load_configs(True)

    right_message = {CONFIGS['RESPONSE']: 200}

    error_message = {
        CONFIGS['ERROR']: 'Bad Request',
        CONFIGS['RESPONSE']: 404,
    }

    def test_action(self):
        self.assertEqual(
            handle_message({
                self.CONFIGS['TIME']: '23.21',
                self.CONFIGS['ACTION']: 'Error',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'test'
                }
            },
                self.CONFIGS
            ),
            self.error_message
        )

    def test_user(self):
        self.assertEqual(
            handle_message({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: '23.21',
            },
                self.CONFIGS
            ),
            self.error_message
        )

    def test_user_two(self):
        self.assertEqual(
            handle_message({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['TIME']: '23.21',
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Error'
                }
            },
                self.CONFIGS
            ),
            self.error_message
        )

    def test_time(self):
        self.assertEqual(
            handle_message({
                self.CONFIGS['ACTION']: self.CONFIGS['PRESENCE'],
                self.CONFIGS['USER']: {
                    self.CONFIGS['ACCOUNT_NAME']: 'Guest'
                }
            },
                self.CONFIGS
            ),
            self.error_message
        )


if __name__=='__main__':
    unittest.main()
