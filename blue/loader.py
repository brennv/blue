from .logger import log
import os
import yaml


def jsonify(filepath):
    """ Load yaml. """
    with open(filepath, 'r') as f:
        data = yaml.load(f)
    log.debug('loaded yaml %s' % filepath)
    return data


def find_file(path, ext, index=0, sort='getctime'):  # unused
    """ Search files by extension, sort by time created and return indexed file. """
    files = [x for x in os.listdir(path) if x.endswith(ext)]
    files = sorted(files, key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
    new_file = os.path.join(path, files[index])  # TODO raise helpful error
    log.debug('loaded file %s' % new_file)
    return new_file
