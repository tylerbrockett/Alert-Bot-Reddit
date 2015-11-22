import sys
import traceback


class ExceptionHelper:
    def __init__(self):
        print ''

    # This code curtesy of:
    # http://stackoverflow.com/questions/6086976/how-to-get-a-complete-exception-stack-trace-in-python
    def formatException(self, e):
        exception_list = traceback.format_stack()
        exception_list = exception_list[:-2]
        exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
        exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

        exception_str = "Traceback (most recent call last):\n"
        exception_str += "".join(exception_list)
        # Removing the last \n
        exception_str = exception_str[:-1]

        return exception_str

    def getStacktrace(self):
        # This line curtesy of
        # http://stackoverflow.com/questions/6086976/how-to-get-a-complete-exception-stack-trace-in-python
        e = traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
        return self.formatException(e)
