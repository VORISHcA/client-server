import json
import logging
import sys
import socket
from logs import configuration_server
from utils.decorators import Log

from utils.utils import load_configs, get_message, send_message

CONFIGS = dict()

SERVER_LOGGER = logging.getLogger('server')


@Log()
def handle_message(message, CONFIGS):
    global SERVER_LOGGER
    SERVER_LOGGER.debug(f'Обработка сообщения от клиента : {message}')
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        return {CONFIGS.get('RESPONSE'): 200}
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


def main():
    global CONFIGS, SERVER_LOGGER
    CONFIGS = load_configs()
    listen_port = CONFIGS.get('DEFAULT_PORT')
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        if not 65535 >= listen_port >= 1024:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с некорректного порта {listen_port}.'
                               'Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        SERVER_LOGGER.critical('После \'a\'- необходимо указать адрес.')
        sys.exit(1)

    SERVER_LOGGER.info(f'Сервер запущен на порту: {listen_port}, по адресу: {listen_address}.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        client, client_address = transport.accept()
        try:
            message = get_message(client, CONFIGS)
            response = handle_message(message, CONFIGS)
            send_message(client, response, CONFIGS)
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.critical('Принято некорретное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
