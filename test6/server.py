import json
import logging
import sys
import socket
import time
from utils.decorators import Log
import argparse
import select

from utils.utils import load_configs, get_message, send_message

CONFIGS = dict()

SERVER_LOGGER = logging.getLogger('server')



@Log()
def arg_parser(CONFIGS):
    global SERVER_LOGGER
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    server_port = namespace.port
    return listen_address, listen_port


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
    listen_address, listen_port = arg_parser(CONFIGS)
    if not 1023 < listen_port < 65536:
        print(f'{listen_port} не входит в диапозон от 1023 до 65536')
        sys.exit(0)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))
    clients = []
    messages = []

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

        try:
            client, client_address = transport.accept()
            SERVER_LOGGER.info(f'{client_address} соединение')
            clients.append(client)
        except OSError:
            pass
        input_list = []
        send_list = []
        err_list = []
        try:
            if clients:
                input_list, send_list, err_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if input_list:
            for client in input_list:
                try:
                    handle_message(get_message(client, CONFIGS), messages, client, CONFIGS)
                except:
                    clients.remove(client)

        if messages and send_list:
            message = {
                CONFIGS['MESSAGE_TEXT']: messages[0][1],
                CONFIGS['SENDER']: messages[0][0],
                CONFIGS['ACTION']: CONFIGS['MESSAGE'],
                CONFIGS['TIME']: time.time(),
            }
            del messages[0]
            for waiting_client in send_list:
                send_message(waiting_client, message, CONFIGS)


if __name__ == '__main__':
    main()
