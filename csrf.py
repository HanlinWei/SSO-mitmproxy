import mitmproxy
from urllib.parse import urlparse

# change the access_token or code in request's query
# target should be access_token= or code=
def csrf_request(flow: mitmproxy.http.HTTPFlow, target, new_value):
    queries = urlparse(flow.request.pretty_url).query.split("&")
    access_token = ""
    for query in queries:
        if query.startswith(target) and len(query) > 20:
            access_token = query
            break
    if access_token:
        urls = flow.request.pretty_url.split(access_token)
        flow.request.url = urls[0] + target + new_value + urls[1]
        return flow.request.url
    else:
        return ""