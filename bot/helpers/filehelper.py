import os.path

PROCESS_ID = '/monitoring/process_id.pid'
STACKTRACE = '/monitoring/stacktrace.txt'

EMPTY = ''

# TODO: FILES ARE NOT THREAD-SAFE, FIX IT!
class FileHelper:
    def __init__(self):
        print ''

    def readFile(self, path):
        with open(os.path.dirname(__file__) + '/..' + path, 'r') as f:
            contents = f.read()
            f.close()
            return contents

    def writeToFile(self, path, string):
        with open(os.path.dirname(__file__) + '/..' + path, 'w') as f:
            f.seek(0)
            f.truncate()
            f.write(str(string))
            f.close()

    def eraseContents(self, path):
        with open(os.path.dirname(__file__) + '/..' + path, 'w') as f:
            f.seek(0)
            f.truncate()
            f.close()

    def isEmpty(self, path):
        with open(os.path.dirname(__file__) + '/..' + path, 'r') as f:
            contents = f.read()
            f.close()
            if contents == '':
                return True
            return False