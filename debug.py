
ERROR = 1
WARNING = 2
INFO = 3
DEBUG = 4
POSITION = 10

trace_level = ERROR

def trace(niveau, message):
    if niveau <= trace_level:
        print(message)