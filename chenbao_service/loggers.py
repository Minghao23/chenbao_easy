import os
import logging
import ConfigParser

root_dir = os.path.dirname(os.path.realpath(__file__))

LEVEL_TABLE = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}

DEFAULT_LOGGER_NAME = 'chenbao_service'


def get_logger(logger_name=DEFAULT_LOGGER_NAME):
    return logging.getLogger(logger_name)


def get_django_log_setting(logger_name=DEFAULT_LOGGER_NAME):

    setting = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s [%(filename)s:%(lineno)s][%(funcName)s] %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(root_dir, 'log', logger_name + '.log'),
                'maxBytes': 1024 * 1024 * 50,  # limit 50MB
                'backupCount': 20,
                'formatter': 'standard',
                'encoding': 'utf-8'
            }
        },
        'loggers': {
            # Uncomment 'django' domain to open Django default log, such as requests details...
            'django': {
                'handlers': ['console', 'file'],
                'propagate': True
            },
            logger_name: {
                'handlers': ['file'],
                'level': 'DEBUG'
            },
        }
    }
    return setting
