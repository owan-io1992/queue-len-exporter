import psutil


def cpu_percent(interval):
    ret = psutil.cpu_percent(interval)

    return ret
