usingdir = '/sys/fs/cgroup/memory/memory.max_usage_in_bytes'
totaldir = '/sys/fs/cgroup/memory/memory.limit_in_bytes'

# deprecated


def ram():
    try:
        using = int(open(usingdir).read())
        total = int(open(totaldir).read())
    except FileNotFoundError:
        return 'Dados não encontrados'
    else:
        return f"{convert(using)}/{convert(total)}"


def using_ram():
    try:
        using = int(open(usingdir).read())
    except FileNotFoundError:
        return 'Dados não encontrados'
    else:
        return convert(using)


def total_ram():
    try:
        total = int(open(totaldir).read())
    except FileNotFoundError:
        return 'Dados não encontrados'
    else:
        return convert(total)


def convert(membytes):
    types = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    n = 0
    while membytes > 1024:
        membytes = membytes/1024
        n += 1
    return '{0:.2f}'.format(membytes).rstrip('0').rstrip('.') + types[n]