# HTTP lifecycle
import mitmproxy
import logger
import checker
import time
from state import State

log_file = "log/" + time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
cur_state = State("*")

def http_connect(flow: mitmproxy.http.HTTPFlow):
    """
        An HTTP CONNECT request was received. Setting a non 2xx response on
        the flow will return the response to the client abort the
        connection. CONNECT requests and responses do not generate the usual
        HTTP handler events. CONNECT requests are only valid in regular and
        upstream proxy modes.
    """

def requestheaders(flow: mitmproxy.http.HTTPFlow):
    """
        HTTP request headers were successfully read. At this point, the body
        is empty.
    """

def request(flow: mitmproxy.http.HTTPFlow):
    """
        The full HTTP request has been read.
    """
    global log_file
    host = checker.check_host(flow)
    if host:
        if checker.check_TLS(flow):
            logger.write(log_file, \
                "[TLS] " + flow.request.pretty_url)


def responseheaders(flow: mitmproxy.http.HTTPFlow):
    """
        HTTP response headers were successfully read. At this point, the body
        is empty.
    """

def response(flow: mitmproxy.http.HTTPFlow):
    """
        The full HTTP response has been read.
    """
    host = checker.check_host(flow)

    # check 307 vulnerability
    global log_file
    if host:
        if checker.check_307(flow):
            logger.write(log_file, \
                "[307] " + flow.request.pretty_url)

    # check state parameters in traffic
    global cur_state
    if host != cur_state.current_web and host:
        cur_state.set_current_web(host)
        logger.write_info(log_file, "current_web: " + cur_state.current_web)

    if cur_state.state > 0 and checker.contain_state(flow):
        if cur_state.renew_state(flow) != 2 and cur_state.state == 2:
            pass
        else:
            cur_state.confirm_state_para()
            logger.write_info(log_file, "found state= at state " + str(cur_state.state))

    if cur_state.state > 2 and cur_state.timeout() and not cur_state.state_para_checked:
        logger.write_info(log_file, str(cur_state.have_state_para) + str(cur_state.have_state_para=={1,2,3}))
        if not cur_state.check_state_para():
            logger.write(log_file, \
                "[STA] Bad!" + cur_state.current_web)
        else:
            logger.write(log_file, \
                "[STA] Nice! " + cur_state.current_web)

    new_state = cur_state.renew_state(flow)
    if new_state > -1:
        logger.write_info(log_file, "renew_state " + str(new_state))

    if cur_state.state == 3:
        pass

    logger.info(host)

def error(flow: mitmproxy.http.HTTPFlow):
    """
        An HTTP error has occurred, e.g. invalid server responses, or
        interrupted connections. This is distinct from a valid server HTTP
        error response, which is simply a response with an HTTP error code.
    """