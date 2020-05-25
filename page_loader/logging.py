import logging.config


class KnownError(Exception):
    pass


LOGGER_CONFIG = {
        'version': 1,
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
                'level': 'WARNING',
                'formatter': 'console_formatter'
                },
            'file_handler': {
                'class': 'logging.FileHandler',
                'filename': 'page-loader.log',
                'mode': 'w',
                'level': 'DEBUG',
                'formatter': 'file_formatter'
                }
            },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['file_handler', 'console_handler'],
                }
            }
        }


logging.config.dictConfig(LOGGER_CONFIG)
