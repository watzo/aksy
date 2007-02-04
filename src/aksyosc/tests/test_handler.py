from unittest import TestCase, TestLoader
from aksyosc.handler import SamplerCallbackManager
from aksyosc.osc import OSCMessage

class RecordingSampler:
    def __init__(self):
        self.recorded = []
    def execute_by_cmd_name(self, s, c, args):
        self.recorded.append([s, c, args])
        
class SamplerCallbackManagerTest(TestCase):
    def setUp(self):
        self.sampler = RecordingSampler()
        self.handler = SamplerCallbackManager(self.sampler)
 
    def testDispatch(self):
        message = OSCMessage()
        message.setAddress("/sample/play")
        message.append("test.wav")
        self.handler.handle(message.getBinary())
        self.assertEquals([["sample", "play", ["test.wav"]]], self.sampler.recorded)
        
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

