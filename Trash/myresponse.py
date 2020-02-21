import mitmproxy
from mitmproxy import ctx

def response_hello_world(flow: mitmproxy.http.HTTPFlow):
    if flow.request.pretty_url.endswith("gitlab.com/users/sign_in"):
        flow.response = mitmproxy.http.HTTPResponse.make(
            200,
            "<html><body>hello world</body></html>",
            {"content-type":"text/html"},
        )