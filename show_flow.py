import os
import serialize
from urllib.parse import urlparse

reqs = []
l = os.listdir('Req')
l.sort()
for file in l:
    reqs.append(serialize.readbunchobj("./Req/" + file))

responses = []
l = os.listdir('Res')
l.sort()
for file in l:
    responses.append(serialize.readbunchobj("./Res/" + file))

for req in reqs:
    url = urlparse(req.pretty_url)
    print(url.netloc + url.path)