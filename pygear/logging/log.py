import logging
from twisted.python import log

__logouter__ = True


# Logging levels
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
TRACE = CRITICAL + 10
SILENT = TRACE + 10

level_names = {
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "CRITICAL",
    SILENT: "SILENT",
}


def msg(message=None, _level=INFO, **kw):
    kw['logLevel'] = kw.pop('level', _level)
    kw.setdefault('system', 'miutils')
    if message is None:
        log.msg(**kw)
    else:
        log.msg(message, **kw)


def err(_stuff=None, _why=None, **kw):
    kw['logLevel'] = kw.pop('level', ERROR)
    kw.setdefault('system', 'miutils')
    log.err(_stuff, _why, **kw)


def debug(message=None, **kw):
    kw['logLevel'] = DEBUG
    kw.setdefault('system', 'miutils')
    if message is None:
        log.msg(**kw)
    else:
        log.msg(message, **kw)


def warn(message=None, **kw):
    kw['logLevel'] = WARNING
    kw.setdefault('system', 'miutils')
    if message is None:
        log.msg(**kw)
    else:
        log.msg(message, **kw)


def crt(message=None, **kw):
    kw['logLevel'] = CRITICAL
    kw.setdefault('system', 'miutils')
    if message is None:
        log.msg(**kw)
    else:
        log.msg(message, **kw)


def silent(message=None, **kw):
    kw['logLevel'] = SILENT
    kw.setdefault('system', 'miutils')
    if message is None:
        log.msg(**kw)
    else:
        log.msg(message, **kw)


def trace(message=None, **kw):
    kw['logLevel'] = TRACE
    kw.setdefault('system', 'miutils')
    if message is None:
        log.msg(**kw)
    else:
        log.msg(message, **kw)
