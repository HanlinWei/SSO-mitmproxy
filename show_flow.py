import os
import serialize
from urllib.parse import urlparse

reqs = []
l = os.listdir('Req2')
l.sort()
for file in l:
    reqs.append(serialize.readbunchobj("./Req2/" + file))

responses = []
l = os.listdir('Res')
l.sort()
for file in l:
    responses.append(serialize.readbunchobj("./Res/" + file))

# for req in reqs:
#     url = urlparse(req.pretty_url)
#     print(req.pretty_url)
#     print("\n*********************\n")

print(reqs[0].pretty_url)
# print("\n*********************\n")
# print(responses[2].text)
