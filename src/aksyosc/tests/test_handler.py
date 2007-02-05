from unittest import TestCase, TestLoader
from aksyosc.handler import SamplerCallbackManager
from aksyosc.osc import OSCMessage

class RecordingSampler:
    def __init__(self, response=None):
        self.recorded = []
        self.response = response
    def execute_by_cmd_name(self, s, c, args):
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
        self.assertEquals(str(expected), str(response))

    def testDispatchInvalidAddress(self):
        message = OSCMessage()
        message.setAddress("/sample/play/invalid")
        # should not throw
        # TODO assert log contents
        self.handler.handle(message.getBinary())
        self.assertEquals([], self.sampler.recorded);
        
def test_suite():
    testloader = TestLoader()
    return testloader.loadTestsFromName('aksyosc.tests.test_handler')

