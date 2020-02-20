from mitmproxy import ctx

def info(str):
    ctx.log.info(str)

def write(file, content):
    with open(file, 'a+') as f:
        f.write("\n" + content)

def write_info(file, content):
    with open(file, 'a+') as f:
        f.write("\n[INFO] " + content)

def write_file(file, content):
    with open(file, 'w+') as f:
        f.write(content)