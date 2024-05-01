import logging
import os
import yaml
from starlette.config import Config

config = Config(".env")

path_base = config.get("PATH_BASE", default='')
health_path = config.get('HEALTH_PATH', default='health')


host_db = config.get('HOST_DB', default='localhost')
port_db = config.get('PORT_DB', default='5432')
db_db = config.get('DB_DB', default='niver65')
user_db = config.get('USER_DB', default='postgres')
__db_psw = config.get('PSW_DB', default='123456')
__url_db = f'postgresql://{host_db}:{port_db}/{db_db}?user={user_db}&password={__db_psw}'

database_url = config.get('DATABASE_URL', default=f'{__url_db}')
env_exec = config.get(key='ENV_EXEC', default='dev')


def setup_logging(config_file=None):
    if not config_file:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_directory, 'set_logging.yaml')

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # Limpar handlers existentes
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configurando o logger raiz
    logging.root.setLevel(logging.NOTSET)


    # Criando um logger para os logs de erro
    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)

    # Definindo o destino dos logs de erro baseado na variável de ambiente
    log_error_dest = config.get('LOG_ERROR_DEST', 'console')

    if log_error_dest == 'console':
        error_handler = logging.StreamHandler()  # Saída para o console
    else:
        error_handler = logging.FileHandler(filename=config['logging']['filename'], mode='a')

    error_handler.setFormatter(logging.Formatter(config['logging']['format']))
    error_logger.addHandler(error_handler)

    # Criando um manipulador para logs de nível WARNING para exibição no console
    warning_handler = logging.StreamHandler()
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(logging.Formatter(config['logging']['format']))
    warning_logger = logging.getLogger('warning_logger')
    warning_logger.setLevel(logging.WARNING)
    warning_logger.addHandler(warning_handler)

    # Criando um manipulador para logs de nível INFO para exibição no console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(config['logging']['format']))
    info_logger = logging.getLogger('info_logger')
    info_logger.setLevel(logging.INFO)
    info_logger.addHandler(console_handler)

    # Ajustar para que o logger de warning não capture abaixo de WARNING
    warning_logger.propagate = False
    info_logger.propagate = False
