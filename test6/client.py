import json
import logging
import sys
import socket
import time
import threading
import argparse
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


def create_message(sock, account_name='Guest'):
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    if message != '0':
        message_dict = {
            CONFIGS['ACTION']: CONFIGS['MESSAGE'],
            CONFIGS['SENDER']: account_name,
            CONFIGS['DESTINATION']: to_user,
            CONFIGS['TIME']: time.time(),
            CONFIGS['MESSAGE_TEXT']: message
        }
        SERVER_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(sock, message_dict, CONFIGS)
            SERVER_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
        except:
            SERVER_LOGGER.critical('Потеряно соединение с сервером.')
            sys.exit(1)
    else:
        send_message(sock, create_exit_message(account_name), CONFIGS)
        SERVER_LOGGER.info('Завершение работы по команде пользователя.')


@Log()
def create_exit_message(account_name):
    return {
        CONFIGS['ACTION']: CONFIGS['EXIT'],
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name
    }


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


@Log()
def arg_parser(CONFIGS):
    parser = argparse.ArgumentParser()
    parser.add_argument('addr',default=CONFIGS['DEFAULT_IP_ADDRESS'], nargs='?')
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('-m', '--type', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    client_type = namespace.type
    server_address = namespace.addr
    server_port = namespace.port
    return server_address, server_port, client_type


def get_user_message(sock, CONFIGS, account_name='Guest'):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        SERVER_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        CONFIGS['ACTION']: CONFIGS['MESSAGE'],
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name,
        CONFIGS['MESSAGE_TEXT']: message
    }
    SERVER_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    try:
        server_address, server_port, client_type = arg_parser(CONFIGS)
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except ValueError:
        SERVER_LOGGER.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        take_message = input('Введите 0 для выхода')

        if take_message == 0:
            transport.close()
            sys.exit(0)
        presence_message = create_presence_message('Guest', CONFIGS)
        SERVER_LOGGER.info(f'Отправка сообшения серверу.')
        send_message(transport, presence_message, CONFIGS)
        if client_type == 'send':
            print('Отправка сообщений')
        if client_type == 'listen':
            print('Прием сообщений')
    except OSError:
        sys.exit(1)
    else:
        client_name = ''
        receiver = threading.Thread(target=get_message, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()
        time.sleep(0.5)
        sender = threading.Thread(target=create_message, args=(transport, client_name))
        sender.daemon = True
        sender.start()



        # while True:
        #     if client_type == 'send':
        #         try:
        #             send_message(transport, get_user_message(transport, CONFIGS), CONFIGS)
        #         except (ConnectionResetError, ConnectionError):
        #             SERVER_LOGGER.error(f'Соединение с срвером разорвано.')
        #             sys.exit(1)
        #     else:
        #         try:
        #             message = get_message(transport, CONFIGS)
        #             if CONFIGS['ACTION'] in message and CONFIGS['SENDER'] in message and CONFIGS['MESSAGE_TEXT'] in message:
        #                 print(f'{message[CONFIGS["MESSAGE_TEXT"]]} прислал {message[CONFIGS["SENDER"]]}')
        #             else:
        #                 print(f'{message} проверьте отправителя и получателья')
        #         except (ConnectionResetError, ConnectionError):
        #             SERVER_LOGGER.error(f'Соединение с срвером разорвано')
        #             sys.exit(1)


if __name__ == '__main__':
    main()

