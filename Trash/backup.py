import mitmproxy
from mitmproxy import ctx
from copy import deepcopy
import time

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

    # check if this is a replay flow
    if "test_url_parameters" in flow.request.headers.keys():
        if flow.request.headers["test_url_parameters"] == "true":
            # This is a replay flow. It needs to be test with its response
            simplified_url[flow.request.headers["flow_id"]].judge_parameter(flow)
            flow.intercept()
            time.sleep(4)
            flow.resume()
            return
    
    origin_url = flow.request.pretty_url
    # if no query in url, return
    if origin_url.find("?") == -1:
        return

    # block this flow
    flow.intercept()

    # extract the parameters in url
    url = origin_url.split("?")
    assert len(url) == 2
    parameters = url[1].split("&")
    flow_id = str(hash(flow))
    simplified_url[flow_id] = Simplified_URL(flow, parameters)
    # try removing each parameters in url 
    # replay and see the change of response
    for i, val in enumerate(parameters):
        # compose fake url
        fake_url = origin_url
        index = fake_url.find(val)
        if not fake_url.find("&", index) == -1:
            fake_url = fake_url[:index] + fake_url[index+len(val)+1:]
        else:
            fake_url = fake_url[:index] + fake_url[index+len(val):]
        if fake_url.endswith("&"):
            fake_url = fake_url[:-1]
        # ctx.log.info("fake_url: " + fake_url)
        # replay the flow with fake url
        fake_flow = flow.copy()
        fake_flow.request.headers["test_url_parameters"] = "true"
        fake_flow.request.headers["deleted"] = val
        fake_flow.request.headers["flow_id"] = flow_id
        fake_flow.request.url = fake_url
        replay(fake_flow)

    time.sleep(3)
    ctx.log.info("origin_url: " + origin_url)
    surl = simplified_url[flow_id].summary()
    ctx.log.info("simplified_url: " + surl)
    flow.resume() # release the block
    return surl

"""
test the necessity of each line in form of POST method
"""
def test_post_form(flow: mitmproxy.http.HTTPFlow, pattern: str = "*"):
    global simplified_form
    # check legality
    if flow.request.pretty_url.find(pattern) == -1 and pattern != "*":
        return

    if flow.request.method != "POST":
        return

    # check if this is a replay flow
    if "test_post_form" in flow.request.headers.keys():
        if flow.request.headers["test_post_form"] == "true":
            # This is a replay flow. It needs to be test with its response
            simplified_form[flow.request.headers["flow_id"]].judge_parameter(flow)
            flow.intercept()
            return

    origin_form = flow.request.text

    # block this flow
    flow.intercept()

    # extract the parameters in form
    parameters = origin_form.split("&")
    flow_id = str(hash(flow))
    simplified_form[flow_id] = Simplified_Form(flow, parameters)
    # try removing each parameters in form 
    # replay and see the change of response
    for i, val in enumerate(parameters):
        # compose fake form
        fake_form = origin_form
        index = fake_form.find(val)
        if not fake_form.find("&", index) == -1:
            fake_form = fake_form[:index] + fake_form[index+len(val)+1:]
        else:
            fake_form = fake_form[:index] + fake_form[index+len(val):]
        if fake_form.endswith("&"):
            fake_form = fake_form[:-1]
        ctx.log.info("fake_form: " + fake_form)
        # replay the flow with fake form
        fake_flow = flow.copy()
        fake_flow.request.headers["test_post_form"] = "true"
        fake_flow.request.headers["deleted"] = val
        fake_flow.request.headers["flow_id"] = flow_id
        fake_flow.request.text = fake_form
        replay(fake_flow)

    time.sleep(3)
    ctx.log.info("origin_form: " + origin_form)
    sform = simplified_form[flow_id].summary()
    ctx.log.info("simplified_form: " + sform)
    flow.resume() # release the block
    return sform

def replay(fake_flow: mitmproxy.http.HTTPFlow):
    fake_flow.live = False
    fake_flow.intercepted = False
    if "view" in ctx.master.addons:
        ctx.master.commands.call("view.flows.add", [fake_flow])
    ctx.master.commands.call("replay.client", [fake_flow])

def same_response(response1: mitmproxy.http.HTTPResponse, response2: mitmproxy.http.HTTPResponse):
    if response1.status_code != response2.status_code \
        or response1.text != response2.text \
        or response1.cookies != response2.cookies:
        return True
    return False

class Simplified_URL():
    def __init__(self, flow: mitmproxy.http.HTTPFlow, parameters: list):
        self.origin_flow = flow.copy()
        self.origin_url = flow.request.pretty_url
        self.origin_response = flow.response
        self.url_parameters = {}
        for val in parameters:
            self.url_parameters[val] = False

    # judge if this parameter will influence the response
    def judge_parameter(self, fake_flow: mitmproxy.http.HTTPFlow):
        if fake_flow.response.status_code != self.origin_response.status_code \
            or fake_flow.response.text != self.origin_response.text \
            or fake_flow.response.cookies != self.origin_response.cookies:
            self.url_parameters[fake_flow.request.headers["deleted"]] = True

    # output the simplified url without useless parameters
    def summary(self):
        short_url = self.origin_url.split("?")[0]
        for item in self.url_parameters.items():
            if item[1]:
                short_url += item[0]
                short_url += "&"
        if short_url.endswith("&"):
            short_url = short_url[:-1]
        return short_url

class Simplified_Form():
    def __init__(self, flow: mitmproxy.http.HTTPFlow, parameters: list):
        self.origin_flow = flow.copy()
        self.origin_form = flow.request.text
        self.origin_response = flow.response
        self.form_parameters = {}
        for val in parameters:
            self.form_parameters[val] = False

    # judge if this parameter will influence the response
    def judge_parameter(self, fake_flow: mitmproxy.http.HTTPFlow):
        self.form_parameters[fake_flow.request.headers["deleted"]] = \
            same_response(fake_flow.response, self.origin_flow.response)

    # output the simplified url without useless parameters
    def summary(self):
        short_url = self.origin_form.split("?")[0]
        for item in self.form_parameters.items():
            if item[1]:
                short_url += item[0]
                short_url += "&"
        if short_url.endswith("&"):
            short_url = short_url[:-1]
        return short_url