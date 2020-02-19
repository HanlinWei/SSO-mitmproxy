import mitmproxy
from mitmproxy import ctx
import time
import datetime

simplified_url = {}
simplified_form = {}

""" 
test the parameters in url
1. try removing each parameters in url and see the change of response
"""
def test_url_parameters(flow: mitmproxy.http.HTTPFlow, pattern: str = "*"):
    global simplified_url
    # check legality
    if flow.request.pretty_url.find(pattern) == -1 and pattern != "*":
        return

    # do nothing to replay flow
    if "test_url_parameters" in flow.request.headers.keys():
        return

    origin_url = flow.request.pretty_url
    # if no query in url, return
    if origin_url.find("?") == -1:
        return

    # extract the parameters in url
    url = origin_url.split("?")
    assert len(url) == 2
    parameters = url[1].split("&")
    flow_id = str(hash(flow))
    simplified_url[flow_id] = Simplified_URL(flow, parameters)
    
    # remove one parameter in url and replay the request
    def test_single_parameter(val: str):
        fake_url = origin_url
        index = fake_url.find(val)
        if not fake_url.find("&", index) == -1:
            fake_url = fake_url[:index] + fake_url[index + len(val) + 1:]
        else:
            fake_url = fake_url[:index] + fake_url[index + len(val):]
        if fake_url.endswith("&"):
            fake_url = fake_url[:-1]
        # replay the flow with fake url
        fake_flow = flow.copy()
        fake_flow.request.headers["test_url_parameters"] = "true"
        fake_flow.request.headers["deleted"] = val
        fake_flow.request.headers["flow_id"] = flow_id
        fake_flow.request.url = fake_url
        replay(fake_flow)

    # try removing each parameters in url 
    # replay and see the change of response
    for i in range(2):
        for key in simplified_url[flow_id].parameters.keys():
            test_single_parameter(key)

def check_replay_flow(flow: mitmproxy.http.HTTPFlow, pattern: str = "*"):
    global simplified_url
    # check legality
    if flow.request.pretty_url.find(pattern) == -1 and pattern != "*":
        return

    if is_relpay_flow("test_url_parameters", flow, simplified_url):
        flow_id = flow.request.headers["flow_id"]
        if simplified_url[flow_id].finished:
            return
        finish = True
        for item in simplified_url[flow_id].parameters.items():
            if item[1][0] == False:
                finish = False
                break
        if finish:
            surl = simplified_url[flow_id].summary()
            ctx.log.info("simplified_url: " + surl)
            simplified_url[flow_id].finished = True
        return

    flow_id = str(hash(flow))
    ctx.log.info("origin_url: " + flow.request.pretty_url)
    # ctx.log.info("flow_id: " + flow_id)
    if flow_id in simplified_url.keys():
        simplified_url[flow_id].set_response(flow.response)

def replay(fake_flow: mitmproxy.http.HTTPFlow):
    fake_flow.live = False
    fake_flow.intercepted = False
    if "view" in ctx.master.addons:
        ctx.master.commands.call("view.flows.add", [fake_flow])
    ctx.master.commands.call("replay.client", [fake_flow])


def same_response(response1: mitmproxy.http.HTTPResponse, response2: mitmproxy.http.HTTPResponse):
    if response1.status_code != response2.status_code \
            or response1.text != response2.text \
            or response1.cookies != response2.cookies\
            or response1.headers != response2.headers:
        return False
    return True

# check and process replay flow
def is_relpay_flow(header_key: str, flow: mitmproxy.http.HTTPFlow, simplified_dict: dict):
    if header_key in flow.request.headers.keys():
        if simplified_dict[flow.request.headers["flow_id"]].judge_parameter(flow):
            # ctx.log.info("replay flow: " + flow.request.pretty_url.split("?")[0] \
            #     + "?" + flow.request.headers["flow_id"])
            pass
        return True
    return False

"""
Father class of Simplified_URL, Simplified_Form, Simplified_Cookies
"""
class Simplified_Parameters():
    def __init__(self, flow: mitmproxy.http.HTTPFlow, parameters: list):
        self.origin_flow = flow.copy()
        self.finished = False
        self.parameters = {}
        self.response: mitmproxy.http.HTTPResponse = None
        for val in parameters:
            self.parameters[val] = (False, True) 
            # First bool shows if this parameter is checked
            # second bool shows if this parameter influence the response

    def set_response(self, response: mitmproxy.http.HTTPResponse):
        self.response = response

    # judge if this parameter will influence the response
    def judge_parameter(self, fake_flow: mitmproxy.http.HTTPFlow):
        if not self.response:
            ctx.log.info("Haven't received response")
            return -1
        key = fake_flow.request.headers["deleted"]
        if self.parameters[key][0]:
            return 0 # this parameter has been checked
        self.parameters[key] = \
            (True, same_response(fake_flow.response, self.response))
        return 1 # this parameter hasn't been checked

    # output the simplified url without useless parameters
    def summary(self, origin_str):
        simplified = origin_str.split("?")[0] + "?"
        for item in self.parameters.items():
            if item[1][1]:
                simplified += item[0]
                simplified += "&"
        if simplified.endswith("&") or simplified.endswith("?"):
            simplified = simplified[:-1]
        return simplified

class Simplified_URL(Simplified_Parameters):
    def summary(self):
        return super(Simplified_URL, self).summary(self.origin_flow.request.pretty_url)

class Simplified_Form(Simplified_Parameters):
    def summary(self):
        return super(Simplified_URL, self).summary(self.origin_flow.request.text)