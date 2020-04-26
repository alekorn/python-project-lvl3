import logging.config

LOGGER_CONFIG = {
        'version': 1,
        # 'disable_existing_loggers': True,
        'formatters': {
            'file_formatter': {
                'format': '{asctime} | {levelname} | {message}',
                'style': '{'
                },
            'console_formatter': {
                'format': '{levelname}: {message}',
                'style': '{'
                }
            },
        'handlers': {
            'console_handler': {
                'class': 'logging.StreamHandler',
                # 'stream': 'sys.stderr',
                'level': 'WARNING',
                'formatter': 'console_formatter'
                },
            'file_handler': {
                'class': 'logging.FileHandler',
                'filename': 'mylog.log',  # TODO add page downloads path
                'mode': 'w',
                'level': 'DEBUG',
                'formatter': 'file_formatter'
                }
            },
        'loggers': {
            'my_logger': {
                'level': 'DEBUG',
                'handlers': ['file_handler', 'console_handler'],
                # 'propagate': False
                }
            },
        # 'filters': {},
        # 'root': {},
        # 'incrimental': True
        }


logging.config.dictConfig(LOGGER_CONFIG)
LOGGER = logging.getLogger('my_logger')
# LOGGER.setLevel('CRITICAL') # TEST
# logger.setLevel(args.logging_level.upper())
