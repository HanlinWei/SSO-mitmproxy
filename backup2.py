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

    if is_relpay_flow("test_url_parameters", flow, simplified_url):
        return

    origin_url = flow.request.pretty_url
    # if no query in url, return
    if origin_url.find("?") == -1:
        return

    # block this flow
    # flow.intercept()

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
    for i in range(3):
        ctx.log.info("testing")
        finish = True
        for item in simplified_url[flow_id].parameters.items():
            ctx.log.info("item: " + str(item[0]) + " " + str(item[1][0]) + " " + str(item[1][1]))
            if not item[1][0]:
                test_single_parameter(item[0])
                finish = False
        if finish:
            break
        time.sleep(2)

    ctx.log.info("origin_url: " + origin_url)
    surl = simplified_url[flow_id].summary()
    ctx.log.info("simplified_url: " + surl)
    # del simplified_url[flow_id]
    # flow.resume()  # release the block
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

    if is_relpay_flow("test_post_form", flow, simplified_form):
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
            fake_form = fake_form[:index] + fake_form[index + len(val) + 1:]
        else:
            fake_form = fake_form[:index] + fake_form[index + len(val):]
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

    time.sleep(6)
    ctx.log.info("origin_form: " + origin_form)
    sform = simplified_form[flow_id].summary()
    del simplified_form[flow_id]
    ctx.log.info("simplified_form: " + sform)
    flow.resume()  # release the block
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
            or response1.cookies != response2.cookies\
            or response1.headers != response2.headers:
        return True
    return False

# check and process replay flow
def is_relpay_flow(header_key: str, flow: mitmproxy.http.HTTPFlow, simplified_dict: dict):
    if header_key in flow.request.headers.keys():
        # This is a replay flow. It needs to be test with its response
        simplified_dict[flow.request.headers["flow_id"]].judge_parameter(flow)
        # flow.intercept()
        ctx.log.info("replay flow: " + flow.request.pretty_url.split("?")[0])
        return True
    return False

"""
Father class of Simplified_URL, Simplified_Form, Simplified_Cookies
"""
class Simplified_Parameters():
    def __init__(self, flow: mitmproxy.http.HTTPFlow, parameters: list):
        self.origin_flow = flow.copy()
        self.parameters = {}
        for val in parameters:
            self.parameters[val] = (False, True) 
            # First bool shows if this parameter is checked
            # second bool shows if this parameter influence the response

    # judge if this parameter will influence the response
    def judge_parameter(self, fake_flow: mitmproxy.http.HTTPFlow):
        key = fake_flow.request.headers["deleted"]
        if self.parameters[key][0]:
            return
        self.parameters[key] = \
            (True, same_response(fake_flow.response, self.origin_flow.response))

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