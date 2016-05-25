import os.path

PROCESS_ID = '/monitoring/process_id.pid'
STACKTRACE = '/monitoring/stacktrace.txt'

EMPTY = ''


def read_file(path):
    with open(os.path.dirname(__file__) + '/..' + path, 'r') as f:
        contents = f.read()
        f.close()
        return contents


def write_to_file(path, string):
    with open(os.path.dirname(__file__) + '/..' + path, 'w') as f:
        f.seek(0)
        f.truncate()
        f.write(str(string))
        f.close()


def erase_contents(path):
    with open(os.path.dirname(__file__) + '/..' + path, 'w') as f:
        f.seek(0)
        f.truncate()
        f.close()


def is_empty(path):
    with open(os.path.dirname(__file__) + '/..' + path, 'r') as f:
        contents = f.read()
        f.close()
        if contents == '':
            return True
        return False
