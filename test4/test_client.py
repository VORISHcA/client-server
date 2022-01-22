import os
import sys
import unittest
from utils import load_configs
from client import handle_response

sys.path.append(os.path.join(os.getcwd(), '..'))


class TestClass(unittest.TestCase):
    CONFIGS = load_configs()

    def test_right_answer(self):
        self.assertEqual(
            handle_response({self.CONFIGS['RESPONSE']: 200}, self.CONFIGS),
            '200:ok'
        )

    def test_response(self):
        self.assertRaises(
            ValueError,
            handle_response,
            {self.CONFIGS['ERROR']: 'Bad Request'},
            self.CONFIGS
        )


if __name__=='__main__':
    unittest.main()
