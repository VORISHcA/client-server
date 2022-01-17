import json
import logging
import sys
import socket
import time
from logs import configuration_client
from utils.decorators import Log

from utils.utils import load_configs, send_message, get_message

CONFIGS = dict()
SERVER_LOGGER = logging.getLogger('client')


@Log()
def create_presence_message(account_name, CONFIGS):
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    SERVER_LOGGER.info('Создание сообщения для отпарвки на сервер.')
    return message


@Log()
def handle_response(message, CONFIGS):
    SERVER_LOGGER.info('Обработка сообщения от сервера.')
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            SERVER_LOGGER.info('Успешная обработка сообшения от сервера.')
            return '200 : OK'
        SERVER_LOGGER.critical('Обработка сообщения от сервера провалилась.')
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except IndexError:
        server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_PORT')
    except ValueError:
        SERVER_LOGGER.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    presence_message = create_presence_message('Guest', CONFIGS)
    SERVER_LOGGER.info(f'Отправка сообшения серверу.')
    send_message(transport, presence_message, CONFIGS)
    try:
        response = get_message(transport, CONFIGS)
        hanlded_response = handle_response(response, CONFIGS)
        SERVER_LOGGER.debug(f'Ответ от сервера: {response}')
        SERVER_LOGGER.info(f'Обработанный ответ от сервера: {hanlded_response}')
    except (ValueError, json.JSONDecodeError):
        SERVER_LOGGER.critical('Ошибка декодирования сообщения')


if __name__ == '__main__':
    main()
