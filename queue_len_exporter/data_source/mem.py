import psutil


def mem_percent():
    ret = psutil.virtual_memory().used / psutil.virtual_memory().total
    return ret
