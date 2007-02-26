from unittest import TestCase, TestLoader
from aksyosc.handler import SamplerCallbackManager
from aksyosc.osc import OSCMessage

class RecordingSampler:
    def __init__(self, response=None, exc=None):
        self.recorded = []
        self.exc = exc
        self.response = response
    def execute_by_cmd_name(self, s, c, args):
        if self.exc is not None:
            raise self.exc
        self.recorded.append([s, c, args])
        return self.response
        
class SamplerCallbackManagerTest(TestCase):
    def setUp(self):
        self.sampler = RecordingSampler((1,2,'a string'))
        self.handler = SamplerCallbackManager(self.sampler)
 
    def testDispatch(self):
        message = OSCMessage()
        message.setAddress("/sample/play")
        message.append("test.wav")
        response = self.handler.handle(message.getBinary())
        self.assertEquals([["sample", "play", ["test.wav"]]], self.sampler.recorded)
        expected = OSCMessage()
        expected.append(1)
        expected.append(2)
        expected.append('a string')
        self.assertEquals(str(expected), response)

    def testDispatchInvalidAddress(self):
        message = OSCMessage()
        message.setAddress("/sample/play/invalid")
        # should not throw
        resp = self.handler.handle(message.getBinary())
        self.assertEquals(resp, "\x00\x00\x00\x00,ss\x00Failed to execute "
        "command /sample/play/invalid\x00\x00Cause: Invalid address: "
        "'/sample/play/invalid', "
        "should have two components"
        "\x00\x00")
        self.assertEquals([], self.sampler.recorded);

    def testDispatchUnknownCommand(self):
        message = OSCMessage()
        message.setAddress("/sample/play")
        sampler = RecordingSampler((1,2,'a string'), AttributeError('a'))
        handler = SamplerCallbackManager(sampler)
        # should not throw
        resp = handler.handle(message.getBinary())
        self.assertEquals(resp, "\x00\x00\x00\x00,ss\x00Failed to execute "
        "command /sample/play\x00\x00Cause: a\x00\x00\x00\x00") 
        self.assertEquals([], self.sampler.recorded);
        
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyosc.tests.test_handler')

