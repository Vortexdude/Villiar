

def read_os_release(file='/etc/os-release'):
    data = {}
    with open(file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if not line:
                continue
            key, value = line.split("=")
            value = value.strip('"').strip("\n").rstrip('"')
            data.update({key: value})
    return data
