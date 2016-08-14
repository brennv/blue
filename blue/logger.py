import logging


def logger(config='DEBUG', filename='app.log', mode='a'):  # TODO default to ERROR
    """ Configure log output. """
    if config == 'DEBUG':
        log_level = logging.DEBUG
        mode = 'w'  # overwrite logs
    if config == 'WARN':
        log_level = logging.WARN
    date_format = '%Y-%m-%d %H:%M:%S'  # .%(msecs)03d
    line_format = '%(asctime)s %(levelname)s %(process)s \
    %(filename)s:%(funcName)s:%(lineno)d %(message)s'
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter(line_format, date_format)
    # log to file
    logfile = logging.FileHandler(filename, mode=mode)
    logfile.setLevel(log_level)
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)
    # log to stdout
    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logging

log = logger()
