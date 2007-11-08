from aksy.devices.akai import sysex

import logging, struct, StringIO

REQ_START = 'Request: '
LEN_REQ_START = len(REQ_START)

RESP_START = 'Response: '
LEN_RESP_START = len(RESP_START)

LOG = logging.getLogger("aksy.devices.akai.replaying_connector")

def encode(byte_str):
    s = StringIO.StringIO(len(byte_str))
    for b in byte_str:
        s.write(struct.pack("1B", int(b, 16)))
    return s.getvalue()

class ReplayingConnector(object):
    """ A connector that replays aksy logs.
    If a request comes in, it looks up the corresponding response
    """
    def __init__(self, device_id, log_file):
        self.device_id = device_id
        f = open(log_file, 'r')
        try:
            self.requests = self.parse_log_file(f)
        finally:
            f.close()

    def execute(self, command, args):
        request = sysex.Request(command, args)
        result_bytes = self.execute_request(request)
        result = sysex.Reply(result_bytes, request.command)
        return result.get_return_value()

    def execute_alt_request(self, handle, commands, args, index = None):
        result_bytes = self.execute_request(sysex.AlternativeRequest(handle, commands, args, index))
        result = sysex.Reply(result_bytes, commands[0], True)
        return result.get_return_value()

    def execute_request(self, request):
        """Execute a request on the sampler.
        Returns the byte response.
        """
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("Request: %s", repr(request))

        result_bytes = self.requests[request.get_bytes()]
        
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug("Response: %s", (sysex.byte_repr(result_bytes)))
        return result_bytes
    def parse_log_file(self, f):
        requests = {}
        last_req = None

        for l in f.readlines():
            last_line = self.parse_list_str(l, REQ_START, LEN_REQ_START)
            if last_line is not None:
                last_req = last_line
                continue
            elif last_req is not None:
                cand_resp = self.parse_list_str(l, RESP_START, LEN_RESP_START)
                if cand_resp is None:
                    continue
                prev_resp = requests.get(last_req, None)
                if prev_resp is not None: 
                    continue
                    LOG.warning("multiple results for %s: %s, %s" %(last_req, prev_resp, cand_resp))
                
                requests[last_req] = cand_resp
        
        return requests

    def parse_list_str(self, line, marker, len_marker):
        start = line.find(marker)
        if start < 0:
            return None
        end = line.index(']', start + len_marker)
        return encode(eval(line[start+len_marker:end+1]))