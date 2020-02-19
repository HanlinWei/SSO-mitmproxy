import requests
import serialize
import os
from copy import deepcopy

def format_MultiDictView(multidict):
    new_headers = {}
    for item in multidict.items():
        new_headers[item[0]] = item[1]
    return new_headers

def compare_response(mitm_res, requests_res):
    result = ""
    if not mitm_res.status_code == requests_res.status_code:
        result += ("\nstatus_code: " + str(mitm_res.status_code) + " " + \
            str(requests_res.status_code))
    if not requests_res.headers == format_MultiDictView(mitm_res.headers):
        result += "\nheaders"
    if not requests_res.text == mitm_res.text:
        result += "\ntext"
    return result

reqs = []
l = os.listdir('Req')
l.sort()
for file in l:
    reqs.append(serialize.readbunchobj("./Req/" + file))
    # print(reqs[-1].method + " " + reqs[-1].pretty_url)
    # print(reqs[-1].headers)
    # print(reqs[-1].text)

responses = []
l = os.listdir('Res')
l.sort()
for file in l:
    responses.append(serialize.readbunchobj("./Res/" + file))
    # print(str(responses[-1].status_code) + "\n" + responses[-1].text)

for i in range(3):
    print(reqs[i].method + " " + reqs[i].pretty_url)


# headers = format_MultiDictView(request.headers)
# cookies = format_MultiDictView(request.cookies)

proxies = {'http':'127.0.0.1:8080','https':'127.0.0.1:8080' }

# r = requests.get(reqs[-2].pretty_url, headers=format_MultiDictView(reqs[-2].headers) \
#         , proxies=proxies, verify=False)
# print(r.status_code)
# print(r.ok)
# print(r.text)


